# agenthub-mcp

MCP server for Agent Hub — connect Cursor, Claude Code, Copilot, or any MCP client to skills, agents, rules, and prompts.

> **Getting started:** see [doc/deployment-guide.md](../../../doc/deployment-guide.md) §4 and §7.

## Quick start

```bash
pip install agenthub agenthub-mcp

agenthub install --bundle r-and-d --target .agenthub --source /path/to/repo
export AGENTHUB_CATALOG_PATH=./.agenthub

agenthub connect --catalog .agenthub --output .cursor/mcp.json
agenthub-mcp --stdio
```

Stdio smoke test: `python examples/test-mcp-stdio.py` (from repo root).

## Install

```bash
pip install agenthub agenthub-mcp
# or from this repo:
pip install -e packages/python/agenthub -e packages/python/agenthub-mcp
```

## Download catalog

Use the `agenthub` CLI:

```bash
agenthub install --bundle r-and-d --target ./.agenthub --source /path/to/agenthub-repo
```

## Connect — coding agent

```bash
export AGENTHUB_CATALOG_PATH=./.agenthub
agenthub connect --catalog ./.agenthub --output .cursor/mcp.json
agenthub-mcp --stdio
```

## Connect — application (no MCP)

```python
from agenthub import Catalog

catalog = Catalog(catalog_path="./.agenthub")
skill = catalog.get_skill("feasibility-study")
```

## Environment

| Variable | Purpose |
|----------|---------|
| `AGENTHUB_CATALOG_PATH` | Installed catalog dir (`.agenthub/`) |
| `AGENTHUB_CACHE_PATH` | Fetch cache dir (default: `<catalog>/.agenthub-cache/`) |
| `AGENTHUB_BUNDLE` | Comma-separated bundle ids |
| `AGENTHUB_TOOL_DESC_MODE` | `active` (default) or `passive` |

If `AGENTHUB_BUNDLE` is unset, bundles are read from `agenthub-lock.json` after install.

## Modular architecture

This server reads the same on-disk catalog as the Python SDK — install with `agenthub install`, point `AGENTHUB_CATALOG_PATH` at the result. No catalog is bundled inside the wheel.

For the npm/TypeScript MCP server, see [packages/npm/mcp](../../../packages/npm/mcp/README.md).
