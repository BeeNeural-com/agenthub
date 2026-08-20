import {
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { readResourceFile } from "./loader.js";
import type { Resource } from "./types.js";

export const LOCKFILE_VERSION = 1;
export const LOCKFILE_NAME = "agenthub-cache-lock.json";
export const CACHE_PATH_ENV = "AGENTHUB_CACHE_PATH";

export interface CacheEntry {
  id: string;
  type: string;
  version: string;
  cachedAt: string;
  path: string;
  files: string[];
}

export interface CacheLockfile {
  lockfileVersion: number;
  generatedAt: string;
  cachePath: string;
  entries: CacheEntry[];
}

export interface CacheStatus {
  cachePath: string;
  lockfileVersion: number;
  generatedAt?: string;
  entryCount: number;
  entries: CacheEntry[];
}

function utcNowIso(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function entryRelPath(resourceType: string, resourceId: string, suffix: string): string {
  return `${resourceType}/${resourceId}/${suffix}`.replace(/\\/g, "/");
}

export function discoverCachePath(catalogRoot?: string): string {
  const env = process.env[CACHE_PATH_ENV]?.trim();
  if (env) {
    return resolve(env);
  }
  if (catalogRoot) {
    return resolve(catalogRoot, ".agenthub-cache");
  }
  return resolve(homedir(), ".agenthub-cache");
}

function emptyLock(cachePath: string): CacheLockfile {
  return {
    lockfileVersion: LOCKFILE_VERSION,
    generatedAt: utcNowIso(),
    cachePath,
    entries: [],
  };
}

function loadLock(lockPath: string, cachePath: string): CacheLockfile {
  if (!existsSync(lockPath)) {
    return emptyLock(cachePath);
  }

  try {
    const data = JSON.parse(readFileSync(lockPath, "utf8")) as Partial<CacheLockfile>;
    return {
      lockfileVersion: data.lockfileVersion ?? LOCKFILE_VERSION,
      generatedAt: data.generatedAt ?? utcNowIso(),
      cachePath,
      entries: Array.isArray(data.entries) ? data.entries : [],
    };
  } catch {
    return emptyLock(cachePath);
  }
}

function saveLock(lockPath: string, lock: CacheLockfile, cachePath: string): void {
  lock.generatedAt = utcNowIso();
  lock.cachePath = cachePath;
  writeFileSync(lockPath, `${JSON.stringify(lock, null, 2)}\n`, "utf8");
}

function findEntry(lock: CacheLockfile, resourceType: string, resourceId: string): CacheEntry | undefined {
  return lock.entries.find((entry) => entry.type === resourceType && entry.id === resourceId);
}

function upsertEntry(
  lock: CacheLockfile,
  resourceType: string,
  resourceId: string,
  version: string,
  bodyRel: string,
  files: string[],
): void {
  const now = utcNowIso();
  const existing = findEntry(lock, resourceType, resourceId);
  const payload: CacheEntry = {
    id: resourceId,
    type: resourceType,
    version,
    cachedAt: now,
    path: bodyRel,
    files: [...files].sort(),
  };

  if (existing) {
    Object.assign(existing, payload);
    return;
  }
  lock.entries.push(payload);
}

function isPathInside(base: string, target: string): boolean {
  const rel = relative(resolve(base), resolve(target));
  return rel === "" || (!rel.startsWith("..") && !isAbsolute(rel));
}

export class ResourceCache {
  readonly cachePath: string;
  readonly lockPath: string;
  private lock: CacheLockfile;

  constructor(catalogRoot?: string, cachePath?: string) {
    this.cachePath = resolve(cachePath ?? discoverCachePath(catalogRoot));
    this.lockPath = join(this.cachePath, LOCKFILE_NAME);
    mkdirSync(this.cachePath, { recursive: true });
    this.lock = loadLock(this.lockPath, this.cachePath);
  }

  getBody(resourceType: string, resourceId: string, version: string): string | null {
    const entry = findEntry(this.lock, resourceType, resourceId);
    if (!entry || entry.version !== version) {
      return null;
    }

    const target = resolve(this.cachePath, entry.path);
    if (!isPathInside(this.cachePath, target) || !existsSync(target)) {
      return null;
    }
    return readFileSync(target, "utf8");
  }

  putBody(
    resourceType: string,
    resourceId: string,
    version: string,
    body: string,
    files: string[] = [],
  ): void {
    const bodyRel = entryRelPath(resourceType, resourceId, "body.md");
    const target = join(this.cachePath, bodyRel);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, body, "utf8");
    upsertEntry(this.lock, resourceType, resourceId, version, bodyRel, files);
    saveLock(this.lockPath, this.lock, this.cachePath);
  }

  getFile(resourceType: string, resourceId: string, path: string, version: string): string | null {
    const entry = findEntry(this.lock, resourceType, resourceId);
    if (!entry || entry.version !== version) {
      return null;
    }

    const normalized = path.replace(/\\/g, "/");
    if (!entry.files.some((file) => file.replace(/\\/g, "/") === normalized)) {
      return null;
    }

    const rel = entryRelPath(resourceType, resourceId, `files/${normalized}`);
    const target = resolve(this.cachePath, rel);
    if (!isPathInside(this.cachePath, target) || !existsSync(target)) {
      return null;
    }
    return readFileSync(target, "utf8");
  }

  putFile(
    resourceType: string,
    resourceId: string,
    path: string,
    version: string,
    content: string,
    files: string[] = [],
  ): void {
    const normalized = path.replace(/\\/g, "/");
    const rel = entryRelPath(resourceType, resourceId, `files/${normalized}`);
    const target = join(this.cachePath, rel);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, content, "utf8");

    const entry = findEntry(this.lock, resourceType, resourceId);
    const knownFiles = new Set(files.map((file) => file.replace(/\\/g, "/")));
    if (entry) {
      for (const file of entry.files) {
        knownFiles.add(file.replace(/\\/g, "/"));
      }
    }
    knownFiles.add(normalized);

    const bodyRel = entry?.path ?? entryRelPath(resourceType, resourceId, "body.md");
    upsertEntry(this.lock, resourceType, resourceId, version, bodyRel, [...knownFiles]);
    saveLock(this.lockPath, this.lock, this.cachePath);
  }

  getOrFetchBody(resource: Resource): string {
    const cached = this.getBody(resource.resourceType, resource.id, resource.version);
    if (cached !== null) {
      return cached;
    }
    this.putBody(resource.resourceType, resource.id, resource.version, resource.body, resource.files);
    return resource.body;
  }

  getOrFetchFile(resource: Resource, path: string): string | null {
    const cached = this.getFile(resource.resourceType, resource.id, path, resource.version);
    if (cached !== null) {
      return cached;
    }
    const content = readResourceFile(resource, path);
    if (content === null) {
      return null;
    }
    this.putFile(resource.resourceType, resource.id, path, resource.version, content, resource.files);
    return content;
  }

  clear(): void {
    if (existsSync(this.cachePath)) {
      rmSync(this.cachePath, { recursive: true, force: true });
    }
    mkdirSync(this.cachePath, { recursive: true });
    this.lock = emptyLock(this.cachePath);
    saveLock(this.lockPath, this.lock, this.cachePath);
  }

  status(): CacheStatus {
    return {
      cachePath: this.cachePath,
      lockfileVersion: this.lock.lockfileVersion,
      generatedAt: this.lock.generatedAt,
      entryCount: this.lock.entries.length,
      entries: this.lock.entries,
    };
  }
}
