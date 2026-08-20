import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { LOCKFILE_NAME, ResourceCache } from "../src/cache.js";
import type { Resource } from "../src/types.js";

const fixtureRoot = join(fileURLToPath(new URL("./fixtures/catalog", import.meta.url)));

const originalEnv = { ...process.env };
let tempCacheDir: string | undefined;

afterEach(() => {
  process.env = { ...originalEnv };
  if (tempCacheDir) {
    rmSync(tempCacheDir, { recursive: true, force: true });
    tempCacheDir = undefined;
  }
});

function sampleResource(version = "1.0.0"): Resource {
  return {
    id: "demo-skill",
    name: "Demo Skill",
    description: "Demo",
    tags: [],
    version,
    body: "Demo body for cache test.",
    folder: join(fixtureRoot, "global", "skills", "demo-skill"),
    resourceType: "skill",
    source: "global",
    files: ["references/template.md"],
  };
}

describe("resource cache", () => {
  it("writes lock file on miss and serves cached body on hit", () => {
    tempCacheDir = mkdtempSync(join(tmpdir(), "agenthub-cache-"));
    process.env.AGENTHUB_CACHE_PATH = tempCacheDir;

    const cache = new ResourceCache(fixtureRoot, tempCacheDir);
    const resource = sampleResource();

    expect(cache.getBody("skill", "demo-skill", resource.version)).toBeNull();
    expect(cache.getOrFetchBody(resource)).toBe(resource.body);
    expect(cache.getBody("skill", "demo-skill", resource.version)).toBe(resource.body);

    const lock = JSON.parse(readFileSync(join(tempCacheDir, LOCKFILE_NAME), "utf8")) as {
      entries: Array<{ id: string; version: string }>;
    };
    expect(lock.entries).toHaveLength(1);
    expect(lock.entries[0]?.id).toBe("demo-skill");
  });

  it("invalidates cache when resource version changes", () => {
    tempCacheDir = mkdtempSync(join(tmpdir(), "agenthub-cache-"));
    process.env.AGENTHUB_CACHE_PATH = tempCacheDir;

    const cache = new ResourceCache(fixtureRoot, tempCacheDir);
    cache.getOrFetchBody(sampleResource("1.0.0"));

    expect(cache.getBody("skill", "demo-skill", "2.0.0")).toBeNull();
    expect(cache.getOrFetchBody(sampleResource("2.0.0"))).toBe("Demo body for cache test.");
  });
});
