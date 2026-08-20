import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { ResourceCache } from "./cache.js";
import {
  activeBundlesLabel,
  loadBundles,
  loadCatalog,
} from "./loader.js";
import type { CatalogData, Resource } from "./types.js";

const SERVER_INSTRUCTIONS = `Agent Hub is your R&D department — reusable skills, role agents,
rules, and prompts for research, design, implementation, and validation.

Before starting any task:
1. Call list_skills to check for a matching workflow or methodology
2. Call list_agents if the task needs a specialist role (research, architecture, testing, etc.)
3. Call list_rules for coding, research, or planning standards that apply
4. Call list_prompts for structured task kickoffs
5. Follow retrieved guidance; fetch supporting files only when needed`;

const TOOL_DESC_MODE = (process.env.AGENTHUB_TOOL_DESC_MODE ?? "active").toLowerCase();
const ACTIVE = TOOL_DESC_MODE === "active";

function formatIndex(resources: Record<string, Resource>, label: string, getTool: string): string {
  const entries = Object.values(resources);
  if (entries.length === 0) {
    return `No ${label} found.`;
  }

  const lines = entries.map((resource) => {
    const desc = resource.description || "(no description available)";
    const src = resource.source !== "global" ? ` [${resource.source}]` : "";
    return `- ${resource.id} — ${resource.name}${src}\n  ${desc}`;
  });

  return (
    `${entries.length} Agent Hub ${label} available. Use ${getTool} for full instructions.\n\n` +
    lines.join("\n")
  );
}

function getResource(
  resources: Record<string, Resource>,
  resourceId: string,
  label: string,
  cache: ResourceCache,
): string {
  const resource = resources[resourceId];
  if (!resource) {
    const known = Object.keys(resources).join(", ") || "none";
    return `No ${label} with id '${resourceId}'. Available: ${known}`;
  }

  let header = `# ${resource.name} (v${resource.version})\n\n`;
  if (resource.files.length > 0) {
    const tool = label === "prompt" ? "get_prompt_file" : `get_${label}_file`;
    header += `Supporting files (fetch with ${tool} if needed): ${resource.files.join(", ")}\n\n---\n\n`;
  }
  return header + cache.getOrFetchBody(resource);
}

function getResourceFile(
  resources: Record<string, Resource>,
  resourceId: string,
  path: string,
  label: string,
  cache: ResourceCache,
): string {
  const resource = resources[resourceId];
  if (!resource) {
    return `No ${label} with id '${resourceId}'.`;
  }

  const normalized = path.replace(/\\/g, "/");
  const filesNorm = resource.files.map((file) => file.replace(/\\/g, "/"));
  if (!filesNorm.includes(normalized)) {
    return `No file '${path}' in '${resourceId}'. Available: ${resource.files.join(", ") || "none"}`;
  }

  const content = cache.getOrFetchFile(resource, path);
  if (content === null) {
    return `Cannot read '${path}'.`;
  }
  return content;
}

export function createMcpServer(catalogRoot: string, catalog?: CatalogData): McpServer {
  const root = catalogRoot;
  const data =
    catalog ??
    loadCatalog({
      catalogRoot: root,
    });
  const bundles = loadBundles(root);
  const activeLabel = activeBundlesLabel(root);
  const cache = new ResourceCache(root);

  const server = new McpServer(
    {
      name: "agenthub",
      version: "0.1.0",
    },
    {
      instructions: SERVER_INSTRUCTIONS,
    },
  );

  const listSkillsDesc = ACTIVE
    ? "List Agent Hub skills. Call BEFORE starting research, writing, planning, or engineering tasks to check whether a house-standard workflow covers it. Returns id, name, description."
    : "List available Agent Hub skills. Returns id, name and description.";

  const listAgentsDesc = ACTIVE
    ? "List Agent Hub role agents (research analyst, architect, engineer, tester, etc.). Call when a task needs a specialist role definition and delegation workflow."
    : "List available Agent Hub role agents.";

  const listRulesDesc = ACTIVE
    ? "List Agent Hub rules and standards (engineering, research methodology, conventions). Call before writing code, documents, or research artifacts."
    : "List available Agent Hub rules.";

  const listPromptsDesc = ACTIVE
    ? "List Agent Hub structured prompts for kickoffs and planning tasks. Call when starting epics, research threads, or synthesis sessions."
    : "List available Agent Hub prompts.";

  server.tool("list_skills", listSkillsDesc, {}, async () => ({
    content: [{ type: "text", text: formatIndex(data.skill, "skills", "get_skill") }],
  }));

  server.tool(
    "get_skill",
    "Get full instructions for an Agent Hub skill by id.",
    { skill_id: z.string().describe("Skill id from list_skills") },
    async ({ skill_id }) => ({
      content: [{ type: "text", text: getResource(data.skill, skill_id, "skill", cache) }],
    }),
  );

  server.tool(
    "get_skill_file",
    "Get a supporting file from an Agent Hub skill folder.",
    {
      skill_id: z.string().describe("Skill id"),
      path: z.string().describe("Relative path within the skill folder"),
    },
    async ({ skill_id, path }) => ({
      content: [{ type: "text", text: getResourceFile(data.skill, skill_id, path, "skill", cache) }],
    }),
  );

  server.tool("list_agents", listAgentsDesc, {}, async () => ({
    content: [{ type: "text", text: formatIndex(data.agent, "agents", "get_agent") }],
  }));

  server.tool(
    "get_agent",
    "Get full instructions for an Agent Hub role agent by id.",
    { agent_id: z.string().describe("Agent id from list_agents") },
    async ({ agent_id }) => ({
      content: [{ type: "text", text: getResource(data.agent, agent_id, "agent", cache) }],
    }),
  );

  server.tool(
    "get_agent_file",
    "Get a supporting file from an Agent Hub agent folder.",
    {
      agent_id: z.string().describe("Agent id"),
      path: z.string().describe("Relative path within the agent folder"),
    },
    async ({ agent_id, path }) => ({
      content: [{ type: "text", text: getResourceFile(data.agent, agent_id, path, "agent", cache) }],
    }),
  );

  server.tool("list_rules", listRulesDesc, {}, async () => ({
    content: [{ type: "text", text: formatIndex(data.rule, "rules", "get_rule") }],
  }));

  server.tool(
    "get_rule",
    "Get full instructions for an Agent Hub rule by id.",
    { rule_id: z.string().describe("Rule id from list_rules") },
    async ({ rule_id }) => ({
      content: [{ type: "text", text: getResource(data.rule, rule_id, "rule", cache) }],
    }),
  );

  server.tool(
    "get_rule_file",
    "Get a supporting file from an Agent Hub rule folder.",
    {
      rule_id: z.string().describe("Rule id"),
      path: z.string().describe("Relative path within the rule folder"),
    },
    async ({ rule_id, path }) => ({
      content: [{ type: "text", text: getResourceFile(data.rule, rule_id, path, "rule", cache) }],
    }),
  );

  server.tool("list_prompts", listPromptsDesc, {}, async () => ({
    content: [{ type: "text", text: formatIndex(data.prompt, "prompts", "get_prompt") }],
  }));

  server.tool(
    "get_prompt",
    "Get full instructions for an Agent Hub prompt by id.",
    { prompt_id: z.string().describe("Prompt id from list_prompts") },
    async ({ prompt_id }) => ({
      content: [{ type: "text", text: getResource(data.prompt, prompt_id, "prompt", cache) }],
    }),
  );

  server.tool(
    "get_prompt_file",
    "Get a supporting file from an Agent Hub prompt folder.",
    {
      prompt_id: z.string().describe("Prompt id"),
      path: z.string().describe("Relative path within the prompt folder"),
    },
    async ({ prompt_id, path }) => ({
      content: [{ type: "text", text: getResourceFile(data.prompt, prompt_id, path, "prompt", cache) }],
    }),
  );

  server.tool("list_bundles", "List available Agent Hub bundles and active bundle selection.", {}, async () => {
    if (bundles.length === 0) {
      return { content: [{ type: "text", text: "No bundles found." }] };
    }

    const lines = bundles.map(
      (bundle) =>
        `- ${bundle.id} — ${bundle.name}\n  ${bundle.description || "(no description)"}\n` +
        `  skills: ${bundle.skillCount}, agents: ${bundle.agentCount}, ` +
        `rules: ${bundle.ruleCount}, prompts: ${bundle.promptCount}`,
    );

    return {
      content: [
        {
          type: "text",
          text: `${bundles.length} bundles available (active: ${activeLabel}).\n\n${lines.join("\n")}`,
        },
      ],
    };
  });

  for (const skill of Object.values(data.skill)) {
    registerResource(server, skill, "skill", "use");
  }
  for (const agent of Object.values(data.agent)) {
    registerResource(server, agent, "agent", "use-agent");
  }
  for (const rule of Object.values(data.rule)) {
    registerResource(server, rule, "rule", "use-rule");
  }
  for (const prompt of Object.values(data.prompt)) {
    registerResource(server, prompt, "prompt", "use-prompt");
  }

  return server;
}

function registerResource(
  server: McpServer,
  resource: Resource,
  resourceType: string,
  promptPrefix: string,
): void {
  server.resource(
    `${resourceType}-${resource.id}`,
    `${resourceType}://${resource.id}/content`,
    {
      description: resource.description || `Agent Hub ${resourceType}: ${resource.id}`,
      mimeType: "text/markdown",
    },
    async () => ({
      contents: [
        {
          uri: `${resourceType}://${resource.id}/content`,
          mimeType: "text/markdown",
          text: resource.body,
        },
      ],
    }),
  );

  server.prompt(
    `${promptPrefix}-${resource.id}`,
    resource.description || `Use the ${resource.id} ${resourceType}`,
    async () => ({
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text:
              `Apply the Agent Hub ${resourceType} '${resource.name}' to the current task. ` +
              `Follow these instructions:\n\n${resource.body}`,
          },
        },
      ],
    }),
  );
}

export async function runStdioServer(catalogRoot: string): Promise<void> {
  const catalog = loadCatalog({ catalogRoot });
  const server = createMcpServer(catalogRoot, catalog);

  console.error(
    `[agenthub-mcp] catalog=${catalogRoot} | ` +
      `${Object.keys(catalog.skill).length} skills, ${Object.keys(catalog.agent).length} agents, ` +
      `${Object.keys(catalog.rule).length} rules, ${Object.keys(catalog.prompt).length} prompts ` +
      `(tool_desc_mode=${TOOL_DESC_MODE})`,
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);
}
