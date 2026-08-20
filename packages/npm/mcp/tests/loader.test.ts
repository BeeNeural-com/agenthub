import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { verifyAccessKey } from "../src/auth.js";
import {
  loadCatalog,
  readLockfileBundles,
  readResourceFile,
  resolveBundleNames,
} from "../src/loader.js";

const fixtureRoot = join(fileURLToPath(new URL("./fixtures/catalog", import.meta.url)));

const originalEnv = { ...process.env };

afterEach(() => {
  process.env = { ...originalEnv };
});

describe("catalog loader", () => {
  it("loads global skills and bundle resources from lockfile bundles", () => {
    delete process.env.AGENTHUB_BUNDLE;
    const catalog = loadCatalog({ catalogRoot: fixtureRoot });

    expect(Object.keys(catalog.skill)).toContain("demo-skill");
    expect(catalog.skill["demo-skill"]?.name).toBe("Demo Skill");
    expect(catalog.skill["demo-skill"]?.files).toContain("references/template.md");
    expect(Object.keys(catalog.agent)).toContain("research-analyst");
    expect(catalog.agent["research-analyst"]?.source).toBe("bundle:r-and-d");
  });

  it("prefers AGENTHUB_BUNDLE over lockfile bundles", () => {
    process.env.AGENTHUB_BUNDLE = "";
    delete process.env.AGENTHUB_BUNDLE;

    const fromLock = resolveBundleNames(fixtureRoot);
    expect(fromLock).toEqual(["r-and-d"]);

    process.env.AGENTHUB_BUNDLE = "missing-bundle";
    const fromEnv = resolveBundleNames(fixtureRoot);
    expect(fromEnv).toEqual(["missing-bundle"]);
  });

  it("reads supporting files safely", () => {
    const catalog = loadCatalog({ catalogRoot: fixtureRoot });
    const skill = catalog.skill["demo-skill"];
    expect(skill).toBeDefined();

    const content = readResourceFile(skill!, "references/template.md");
    expect(content).toContain("Supporting template");

    expect(readResourceFile(skill!, "../outside.md")).toBeNull();
  });

  it("reads bundle ids from agenthub-lock.json", () => {
    expect(readLockfileBundles(fixtureRoot)).toEqual(["r-and-d"]);
  });
});

describe("access key gating (deferred)", () => {
  it("verifyAccessKey is a no-op without AGENTHUB_ACCESS_KEY", () => {
    delete process.env.AGENTHUB_ACCESS_KEY;
    expect(() => verifyAccessKey()).not.toThrow();
  });

  it("verifyAccessKey is a no-op when key is set", () => {
    process.env.AGENTHUB_ACCESS_KEY = "test-key";
    process.env.AGENTHUB_ACCESS_KEY_SHA256 = "deadbeef";
    expect(() => verifyAccessKey()).not.toThrow();
  });
});
