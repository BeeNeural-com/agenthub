import {
  ResourceCache,
  discoverCatalogRoot,
  loadBundles,
  loadCatalog,
  type BundleInfo,
  type CatalogData,
  type Resource,
} from "@agenthub-mcp/mcp";

export interface ResourceMeta {
  id: string;
  name: string;
  description: string;
  tags: string[];
  version: string;
  resourceType: Resource["resourceType"];
  source: string;
}

export class Catalog {
  readonly root: string;
  readonly bundles: string[] | undefined;
  private readonly data: CatalogData;
  private readonly cache: ResourceCache;

  constructor(catalogPath?: string, bundles?: string[]) {
    this.root = discoverCatalogRoot(catalogPath);
    this.bundles = bundles;
    this.data = loadCatalog({ catalogRoot: this.root, bundles });
    this.cache = new ResourceCache(this.root);
  }

  listBundles(): BundleInfo[] {
    return loadBundles(this.root);
  }

  listSkills(): ResourceMeta[] {
    return Object.values(this.data.skill).map(toMeta);
  }

  listAgents(): ResourceMeta[] {
    return Object.values(this.data.agent).map(toMeta);
  }

  listRules(): ResourceMeta[] {
    return Object.values(this.data.rule).map(toMeta);
  }

  listPrompts(): ResourceMeta[] {
    return Object.values(this.data.prompt).map(toMeta);
  }

  get(resourceId: string, resourceType?: Resource["resourceType"]): Resource | undefined {
    const types = resourceType ? [resourceType] : (["skill", "agent", "rule", "prompt"] as const);
    for (const type of types) {
      const resource = this.data[type][resourceId];
      if (resource) {
        return { ...resource, body: this.cache.getOrFetchBody(resource) };
      }
    }
    return undefined;
  }

  getSkill(skillId: string): Resource | undefined {
    return this.get(skillId, "skill");
  }

  getAgent(agentId: string): Resource | undefined {
    return this.get(agentId, "agent");
  }

  getRule(ruleId: string): Resource | undefined {
    return this.get(ruleId, "rule");
  }

  getPrompt(promptId: string): Resource | undefined {
    return this.get(promptId, "prompt");
  }

  readFile(resourceId: string, path: string, resourceType?: Resource["resourceType"]): string | null {
    const resource = this.get(resourceId, resourceType);
    if (!resource) {
      return null;
    }
    return this.cache.getOrFetchFile(resource, path);
  }
}

function toMeta(resource: Resource): ResourceMeta {
  return {
    id: resource.id,
    name: resource.name,
    description: resource.description,
    tags: resource.tags,
    version: resource.version,
    resourceType: resource.resourceType,
    source: resource.source,
  };
}

export type { BundleInfo, CatalogData, Resource, ResourceType } from "@agenthub-mcp/mcp";
