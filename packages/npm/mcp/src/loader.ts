import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";
import type { BundleInfo, CatalogData, LoadCatalogOptions, Resource, ResourceType } from "./types.js";
import { ENTRY_FILES, RESOURCE_TYPES, SUBDIRS } from "./types.js";

function splitFrontmatter(text: string): { frontmatter: Record<string, unknown>; body: string } {
  if (!text.startsWith("---")) {
    return { frontmatter: {}, body: text };
  }

  const parts = text.split("---", 3);
  if (parts.length < 3) {
    return { frontmatter: {}, body: text };
  }

  try {
    const parsed = parseYaml(parts[1]);
    return {
      frontmatter: parsed && typeof parsed === "object" ? (parsed as Record<string, unknown>) : {},
      body: parts[2].replace(/^\n/, ""),
    };
  } catch {
    return { frontmatter: {}, body: text };
  }
}

function readManifest(folder: string): Record<string, unknown> {
  const manifestPath = join(folder, "manifest.yaml");
  if (!existsSync(manifestPath)) {
    return {};
  }

  try {
    const parsed = parseYaml(readFileSync(manifestPath, "utf8"));
    return parsed && typeof parsed === "object" ? (parsed as Record<string, unknown>) : {};
  } catch {
    return {};
  }
}

function findEntryFile(folder: string, resourceType: ResourceType): string | null {
  for (const pattern of ENTRY_FILES[resourceType]) {
    if (pattern.startsWith(".")) {
      for (const name of readdirSync(folder).sort()) {
        if (name.endsWith(pattern) && name !== "manifest.yaml" && name !== "README.md") {
          return join(folder, name);
        }
      }
    } else {
      const candidate = join(folder, pattern);
      if (existsSync(candidate)) {
        return candidate;
      }
    }
  }
  return null;
}

function collectSupportingFiles(folder: string, entry: string): string[] {
  const files: string[] = [];

  function walk(current: string): void {
    for (const name of readdirSync(current, { withFileTypes: true })) {
      const fullPath = join(current, name.name);
      if (name.isDirectory()) {
        walk(fullPath);
        continue;
      }
      if (fullPath === entry || name.name === "manifest.yaml" || name.name === "README.md") {
        continue;
      }
      files.push(relative(folder, fullPath).replace(/\\/g, "/"));
    }
  }

  walk(folder);
  return files.sort();
}

function asString(value: unknown, fallback = ""): string {
  return typeof value === "string" ? value : fallback;
}

function asStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((item): item is string => typeof item === "string");
}

export function loadResourcesFromRoot(
  root: string,
  resourceType: ResourceType,
  source: string,
): Record<string, Resource> {
  const resources: Record<string, Resource> = {};
  if (!existsSync(root)) {
    return resources;
  }

  for (const name of readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort()) {
    const folder = join(root, name);
    const entry = findEntryFile(folder, resourceType);
    if (!entry) {
      continue;
    }

    const manifest = readManifest(folder);
    const { frontmatter, body } = splitFrontmatter(readFileSync(entry, "utf8"));
    const description = (asString(frontmatter.description) || asString(manifest.description)).trim();
    const resourceId = asString(manifest.id, name);

    resources[resourceId] = {
      id: resourceId,
      name: asString(frontmatter.name, asString(manifest.name, name)),
      description,
      tags: asStringArray(manifest.tags).length
        ? asStringArray(manifest.tags)
        : asStringArray(frontmatter.tags),
      version: asString(manifest.version, asString(frontmatter.version, "0.0.0")),
      body: body.trim(),
      folder,
      resourceType,
      source,
      files: collectSupportingFiles(folder, entry),
    };
  }

  return resources;
}

export function mergeResources(...layers: Array<Record<string, Resource>>): Record<string, Resource> {
  const merged: Record<string, Resource> = {};
  for (const layer of layers) {
    for (const [id, resource] of Object.entries(layer)) {
      if (!(id in merged)) {
        merged[id] = resource;
      }
    }
  }
  return merged;
}

export function readLockfileBundles(catalogRoot: string): string[] {
  const lockPath = join(catalogRoot, "agenthub-lock.json");
  if (!existsSync(lockPath)) {
    return [];
  }

  try {
    const data = JSON.parse(readFileSync(lockPath, "utf8")) as { bundles?: unknown };
    const bundles = data.bundles;
    if (!Array.isArray(bundles)) {
      return [];
    }
    return bundles.filter((bundle): bundle is string => typeof bundle === "string" && bundle.trim().length > 0);
  } catch {
    return [];
  }
}

export function discoverCatalogRoot(explicit?: string): string {
  if (explicit) {
    return resolve(explicit);
  }

  const env = process.env.AGENTHUB_CATALOG_PATH?.trim();
  if (env) {
    return resolve(env);
  }

  const here = dirname(fileURLToPath(import.meta.url));
  let candidate = resolve(here);
  while (true) {
    if (existsSync(join(candidate, "global", "skills"))) {
      return candidate;
    }
    const parent = dirname(candidate);
    if (parent === candidate) {
      break;
    }
    candidate = parent;
  }

  throw new Error(
    "Agent Hub catalog not found. Set AGENTHUB_CATALOG_PATH, pass --catalog <path>, or install resources with `agenthub install`.",
  );
}

export function resolveBundleNames(catalogRoot: string, bundles?: string[]): string[] {
  if (bundles && bundles.length > 0) {
    return bundles;
  }

  const envBundles = process.env.AGENTHUB_BUNDLE?.split(",")
    .map((bundle) => bundle.trim())
    .filter(Boolean);
  if (envBundles && envBundles.length > 0) {
    return envBundles;
  }

  return readLockfileBundles(catalogRoot);
}

export function loadCatalog(options: LoadCatalogOptions): CatalogData {
  const catalogRoot = resolve(options.catalogRoot);
  const bundleNames = resolveBundleNames(catalogRoot, options.bundles);
  const result = {} as CatalogData;

  for (const resourceType of RESOURCE_TYPES) {
    const subdir = SUBDIRS[resourceType];
    const globalRoot = join(catalogRoot, "global", subdir);
    const layers = [loadResourcesFromRoot(globalRoot, resourceType, "global")];

    for (const bundle of bundleNames) {
      const bundleRoot = join(catalogRoot, "bundles", bundle, subdir);
      layers.push(loadResourcesFromRoot(bundleRoot, resourceType, `bundle:${bundle}`));
    }

    result[resourceType] = mergeResources(...layers);
  }

  return result;
}

export function readResourceFile(resource: Resource, path: string): string | null {
  const normalized = path.replace(/\\/g, "/");
  const matched = resource.files.find((file) => file.replace(/\\/g, "/") === normalized);
  if (!matched) {
    return null;
  }

  const folder = resolve(resource.folder);
  const target = resolve(folder, matched);
  const rel = relative(folder, target);
  if (rel.startsWith("..") || isAbsolute(rel)) {
    return null;
  }
  if (!existsSync(target)) {
    return null;
  }

  return readFileSync(target, "utf8");
}

function countSubdirs(folder: string): number {
  if (!existsSync(folder)) {
    return 0;
  }
  return readdirSync(folder, { withFileTypes: true }).filter((entry) => entry.isDirectory()).length;
}

export function loadBundles(catalogRoot: string): BundleInfo[] {
  const bundlesDir = join(catalogRoot, "bundles");
  if (!existsSync(bundlesDir)) {
    return [];
  }

  return readdirSync(bundlesDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort()
    .map((folderName) => {
      const folder = join(bundlesDir, folderName);
      const manifest = readManifest(folder);
      return {
        id: asString(manifest.id, folderName),
        name: asString(manifest.name, folderName),
        description: asString(manifest.description).trim(),
        skillCount: countSubdirs(join(folder, "skills")),
        agentCount: countSubdirs(join(folder, "agents")),
        ruleCount: countSubdirs(join(folder, "rules")),
        promptCount: countSubdirs(join(folder, "prompts")),
      };
    });
}

export function activeBundlesLabel(catalogRoot: string): string {
  const env = process.env.AGENTHUB_BUNDLE?.trim();
  if (env) {
    return env;
  }
  const locked = readLockfileBundles(catalogRoot);
  if (locked.length > 0) {
    return locked.join(",");
  }
  return "(global only)";
}
