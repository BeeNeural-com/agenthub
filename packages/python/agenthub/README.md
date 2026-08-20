# agenthub (Python SDK)

Install, search, and connect Agent Hub skills to coding agents and applications.

> **Getting started:** [doc/deployment-guide.md](../../doc/deployment-guide.md) §4 · [examples/download-and-connect.md](../../examples/download-and-connect.md)

Public catalog/packages: https://github.com/BeeNeural-com/agenthub — **no full clone required**, no GitHub token.

## Quick start (no clone)

```powershell
pip install agenthub agenthub-mcp
# Fallback if PyPI not published yet:
# pip install "agenthub @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
# pip install "agenthub-mcp @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"

agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json
```

## Install modes

```bash
# From public GitHub (downloads global/ + bundles/ only — no token)
agenthub install --full --target ~/.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub install --bundle web-development --target ~/.agenthub --source github:BeeNeural-com/agenthub
agenthub install --skill feasibility-study --target ./kb --source https://github.com/BeeNeural-com/agenthub

# Maintainer: local checkout
agenthub install --full --target ./.agenthub --source /path/to/checkout
```

## Connect to coding agent

```bash
agenthub connect --catalog ~/.agenthub --output .cursor/mcp.json
agenthub-mcp --stdio   # from agenthub-mcp package on PATH
```

## Connect to application / RAG

```python
from agenthub import Catalog

catalog = Catalog(catalog_path="~/.agenthub")
hits = catalog.search("feasibility study")
skill = catalog.get_skill("feasibility-study")
docs = catalog.as_rag_documents(resource_types=("skill",))
```

```bash
agenthub export-rag --output skills.jsonl --type skill
```

## CLI reference

| Command | Purpose |
|---------|---------|
| `agenthub install` | Download full / bundle / single resource (local path or GitHub URL) |
| `agenthub list skills` | List installed catalog |
| `agenthub search <query>` | Find resources by keyword |
| `agenthub get <id>` | Print resource body |
| `agenthub connect` | Write MCP config (`agenthub-mcp` + `AGENTHUB_CATALOG_PATH`) |
| `agenthub export-rag` | JSONL for vector DBs |
| `agenthub cache status` | Show MCP fetch cache lock file |
| `agenthub cache clear` | Clear cached resource bodies |

## Auth (optional)

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` or `AGENTHUB_GITHUB_TOKEN` | Optional for private forks or higher GitHub API rate limits |

Public `BeeNeural-com/agenthub` installs need no token.

## Architecture note

The SDK loads catalog from disk (`AGENTHUB_CATALOG_PATH`). It does not embed catalog content — same tree as the MCP server reads.
