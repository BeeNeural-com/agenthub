"""Agent Hub MCP server — skills, agents, rules, prompts for coding agents."""
from __future__ import annotations

import os
import sys

from agenthub._cache import ResourceCache
from agenthub._loader import (
    Resource,
    discover_catalog_root,
    load_bundles,
    load_catalog,
    read_lockfile_bundles,
)
from mcp.server.fastmcp import FastMCP

TOOL_DESC_MODE = os.environ.get("AGENTHUB_TOOL_DESC_MODE", "active").lower()
ACTIVE = TOOL_DESC_MODE == "active"

_ROOT = discover_catalog_root()
_CATALOG = load_catalog(_ROOT)
SKILLS = _CATALOG["skill"]
AGENTS = _CATALOG["agent"]
RULES = _CATALOG["rule"]
PROMPTS = _CATALOG["prompt"]
BUNDLES = load_bundles(_ROOT)
_CACHE = ResourceCache(_ROOT)

_SERVER_INSTRUCTIONS = """Agent Hub is your R&D department — reusable skills, role agents,
rules, and prompts for research, design, implementation, and validation.

Before starting any task:
1. Call list_skills to check for a matching workflow or methodology
2. Call list_agents if the task needs a specialist role (research, architecture, testing, etc.)
3. Call list_rules for coding, research, or planning standards that apply
4. Call list_prompts for structured task kickoffs
5. Follow retrieved guidance; fetch supporting files only when needed"""

mcp = FastMCP("agenthub", instructions=_SERVER_INSTRUCTIONS)


def _active_bundles_label() -> str:
    raw = os.environ.get("AGENTHUB_BUNDLE", "")
    if raw.strip():
        return raw
    locked = read_lockfile_bundles(_ROOT)
    if locked:
        return ",".join(locked)
    return "(global only)"


def _format_index(resources: dict[str, Resource], label: str, get_tool: str) -> str:
    if not resources:
        return f"No {label} found."
    lines = []
    for r in resources.values():
        desc = r.description or "(no description available)"
        src = f" [{r.source}]" if r.source != "global" else ""
        lines.append(f"- {r.id} — {r.name}{src}\n  {desc}")
    return (
        f"{len(resources)} Agent Hub {label} available. "
        f"Use {get_tool} for full instructions.\n\n" + "\n".join(lines)
    )


def _get_resource(resources: dict[str, Resource], resource_id: str, label: str) -> str:
    resource = resources.get(resource_id)
    if not resource:
        known = ", ".join(resources) or "none"
        return f"No {label} with id {resource_id!r}. Available: {known}"
    header = f"# {resource.name} (v{resource.version})\n\n"
    if resource.files:
        tool = f"get_{label}_file" if label != "prompt" else "get_prompt_file"
        header += (
            f"Supporting files (fetch with {tool} if needed): "
            + ", ".join(resource.files)
            + "\n\n---\n\n"
        )
    body = _CACHE.get_or_fetch_body(resource)
    return header + body


def _get_resource_file(resources: dict[str, Resource], resource_id: str, path: str, label: str) -> str:
    resource = resources.get(resource_id)
    if not resource:
        return f"No {label} with id {resource_id!r}."
    normalized = path.replace("\\", "/")
    files_norm = [f.replace("\\", "/") for f in resource.files]
    if normalized not in files_norm:
        return f"No file {path!r} in {resource_id!r}. Available: {', '.join(resource.files) or 'none'}"
    content = _CACHE.get_or_fetch_file(resource, path)
    if content is None:
        return f"Cannot read {path!r}."
    return content


_LIST_SKILLS_DESC = (
    "List Agent Hub skills. Call BEFORE starting research, writing, planning, or engineering "
    "tasks to check whether a house-standard workflow covers it. Returns id, name, description."
    if ACTIVE
    else "List available Agent Hub skills. Returns id, name and description."
)


@mcp.tool(description=_LIST_SKILLS_DESC)
def list_skills() -> str:
    return _format_index(SKILLS, "skills", "get_skill")


@mcp.tool()
def get_skill(skill_id: str) -> str:
    return _get_resource(SKILLS, skill_id, "skill")


@mcp.tool()
def get_skill_file(skill_id: str, path: str) -> str:
    return _get_resource_file(SKILLS, skill_id, path, "skill")


_LIST_AGENTS_DESC = (
    "List Agent Hub role agents (research analyst, architect, engineer, tester, etc.). "
    "Call when a task needs a specialist role definition and delegation workflow."
    if ACTIVE
    else "List available Agent Hub role agents."
)


@mcp.tool(description=_LIST_AGENTS_DESC)
def list_agents() -> str:
    return _format_index(AGENTS, "agents", "get_agent")


@mcp.tool()
def get_agent(agent_id: str) -> str:
    return _get_resource(AGENTS, agent_id, "agent")


@mcp.tool()
def get_agent_file(agent_id: str, path: str) -> str:
    return _get_resource_file(AGENTS, agent_id, path, "agent")


_LIST_RULES_DESC = (
    "List Agent Hub rules and standards (engineering, research methodology, conventions). "
    "Call before writing code, documents, or research artifacts."
    if ACTIVE
    else "List available Agent Hub rules."
)


@mcp.tool(description=_LIST_RULES_DESC)
def list_rules() -> str:
    return _format_index(RULES, "rules", "get_rule")


@mcp.tool()
def get_rule(rule_id: str) -> str:
    return _get_resource(RULES, rule_id, "rule")


@mcp.tool()
def get_rule_file(rule_id: str, path: str) -> str:
    return _get_resource_file(RULES, rule_id, path, "rule")


_LIST_PROMPTS_DESC = (
    "List Agent Hub structured prompts for kickoffs and planning tasks. "
    "Call when starting epics, research threads, or synthesis sessions."
    if ACTIVE
    else "List available Agent Hub prompts."
)


@mcp.tool(description=_LIST_PROMPTS_DESC)
def list_prompts() -> str:
    return _format_index(PROMPTS, "prompts", "get_prompt")


@mcp.tool()
def get_prompt(prompt_id: str) -> str:
    return _get_resource(PROMPTS, prompt_id, "prompt")


@mcp.tool()
def get_prompt_file(prompt_id: str, path: str) -> str:
    return _get_resource_file(PROMPTS, prompt_id, path, "prompt")


@mcp.tool()
def list_bundles() -> str:
    if not BUNDLES:
        return "No bundles found."
    lines = []
    for b in BUNDLES:
        desc = b.description or "(no description)"
        lines.append(
            f"- {b.id} — {b.name}\n  {desc}\n"
            f"  skills: {b.skill_count}, agents: {b.agent_count}, "
            f"rules: {b.rule_count}, prompts: {b.prompt_count}"
        )
    configured = _active_bundles_label()
    return f"{len(BUNDLES)} bundles available (active: {configured}).\n\n" + "\n".join(lines)


def _register_resource(resource: Resource, uri_prefix: str, prompt_prefix: str) -> None:
    def read_body() -> str:
        return resource.body

    mcp.resource(
        f"{uri_prefix}://{resource.id}/content",
        name=f"{resource.name} ({resource.resource_type})",
        description=resource.description or f"Agent Hub {resource.resource_type}: {resource.id}",
        mime_type="text/markdown",
    )(read_body)

    def use_resource() -> str:
        return (
            f"Apply the Agent Hub {resource.resource_type} '{resource.name}' to the current task. "
            f"Follow these instructions:\n\n{resource.body}"
        )

    mcp.prompt(
        name=f"{prompt_prefix}-{resource.id}",
        description=resource.description or f"Use the {resource.id} {resource.resource_type}",
    )(use_resource)


for _skill in SKILLS.values():
    _register_resource(_skill, "skill", "use")
for _agent in AGENTS.values():
    _register_resource(_agent, "agent", "use-agent")
for _rule in RULES.values():
    _register_resource(_rule, "rule", "use-rule")
for _prompt in PROMPTS.values():
    _register_resource(_prompt, "prompt", "use-prompt")


def run_stdio() -> None:
    print(
        f"[agenthub-mcp] catalog={_ROOT} | "
        f"{len(SKILLS)} skills, {len(AGENTS)} agents, "
        f"{len(RULES)} rules, {len(PROMPTS)} prompts "
        f"(tool_desc_mode={TOOL_DESC_MODE})",
        file=sys.stderr,
    )
    mcp.run()
