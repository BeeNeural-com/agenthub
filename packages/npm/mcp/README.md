# @agenthub-mcp/mcp

MCP server for Agent Hub — connect Cursor, Claude Code, Copilot, or any MCP client to skills, agents, rules, and prompts.

> **Getting started:** see [doc/deployment-guide.md](../../../doc/deployment-guide.md) §5.

## Quick start

```powershell
# 1. Install catalog via Python CLI
pip install agenthub
agenthub install --bundle r-and-d --target .\.agenthub --source C:\path\to\agenthub-repo

# 2. Run TypeScript MCP server
cd packages\npm\mcp && npm install && npm run build
$env:AGENTHUB_CATALOG_PATH = "C:\path\to\.agenthub"
npx agenthub-mcp --stdio
```

## Install

```bash
npm install -g @agenthub-mcp/mcp
# or: npx @agenthub-mcp/mcp --stdio
# or from this repo:
cd packages/npm/mcp && npm install && npm run build
```

## Download catalog

Use the Python CLI (or copy from repo) to install a catalog:

```bash
pip install agenthub
agenthub install --bundle r-and-d --target ./.agenthub --source /path/to/agenthub-repo
```

This writes `.agenthub/` plus `agenthub-lock.json`.

## Run locally (PowerShell)

From repo root after building the package:

```powershell
cd packages/npm/mcp
npm install
npm run build

$env:AGENTHUB_CATALOG_PATH = "C:\path\to\.agenthub"
node .\dist\cli.js --stdio
```

Or use the bin entry:

```powershell
$env:AGENTHUB_CATALOG_PATH = "C:\path\to\.agenthub"
npx agenthub-mcp --stdio
```

## Connect in `mcp.json`

```json
{
  "mcpServers": {
    "agenthub": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@agenthub-mcp/mcp", "--stdio"],
      "env": {
        "AGENTHUB_CATALOG_PATH": ".agenthub"
      }
    }
  }
}
```

Global install alternative:

```bash
npm install -g @agenthub-mcp/mcp
# then command: agenthub-mcp  (Windows may need the full path to the bin)
```

If `AGENTHUB_BUNDLE` is unset, bundles are read from `agenthub-lock.json` in the catalog root.

## CLI

```text
agenthub-mcp --stdio [--catalog <path>]
```

| Flag | Description |
|------|-------------|
| `--stdio` | Run stdio MCP transport (default) |
| `--catalog <path>` | Catalog directory (overrides `AGENTHUB_CATALOG_PATH`) |

## Environment

| Variable | Required | Purpose |
|----------|----------|---------|
| `AGENTHUB_CATALOG_PATH` | Yes* | Installed catalog dir (`.agenthub/`) |
| `AGENTHUB_CACHE_PATH` | No | Fetch cache dir (default: `<catalog>/.agenthub-cache/`) |
| `AGENTHUB_BUNDLE` | No | Comma-separated bundle ids |
| `AGENTHUB_TOOL_DESC_MODE` | No | `active` (default) or `passive` |

\*Or pass `--catalog <path>` on the CLI.

## MCP tools

Same surface as the Python server:

- `list_skills`, `get_skill`, `get_skill_file`
- `list_agents`, `get_agent`, `get_agent_file`
- `list_rules`, `get_rule`, `get_rule_file`
- `list_prompts`, `get_prompt`, `get_prompt_file`
- `list_bundles`

`get_*` handlers cache bodies and supporting files locally (`agenthub-cache-lock.json` under `.agenthub-cache/` by default). Set `AGENTHUB_CACHE_PATH` to override.

## Test

```powershell
cd packages/npm/mcp
npm test
```
