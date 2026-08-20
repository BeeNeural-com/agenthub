export type ResourceType = "skill" | "agent" | "rule" | "prompt";

export interface Resource {
  id: string;
  name: string;
  description: string;
  tags: string[];
  version: string;
  body: string;
  folder: string;
  resourceType: ResourceType;
  source: string;
  files: string[];
}

export interface BundleInfo {
  id: string;
  name: string;
  description: string;
  skillCount: number;
  agentCount: number;
  ruleCount: number;
  promptCount: number;
}

export interface CatalogData {
  skill: Record<string, Resource>;
  agent: Record<string, Resource>;
  rule: Record<string, Resource>;
  prompt: Record<string, Resource>;
}

export interface LoadCatalogOptions {
  catalogRoot: string;
  bundles?: string[];
}

export const ENTRY_FILES: Record<ResourceType, readonly string[]> = {
  skill: ["SKILL.md"],
  agent: [".agent.md"],
  rule: [".instructions.md", ".md"],
  prompt: [".prompt.md"],
};

export const RESOURCE_TYPES: readonly ResourceType[] = ["skill", "agent", "rule", "prompt"];

export const SUBDIRS: Record<ResourceType, string> = {
  skill: "skills",
  agent: "agents",
  rule: "rules",
  prompt: "prompts",
};
