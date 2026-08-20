# Agent Hub

Modular catalog of **skills**, **agents**, **rules**, and **prompts** across 21 department bundles — for coding assistants, RAG pipelines, and agentic workflows via Python/npm SDKs and MCP.

**Website:** [docs/index.html](docs/index.html) — public GitHub Pages host; packages/catalog live on public [`BeeNeural-com/agenthub`](https://github.com/BeeNeural-com/agenthub).

## What it is

Agent Hub is a **filesystem catalog** (`global/` + `bundles/`) of reusable Markdown resources with YAML frontmatter. Install a subset or the full catalog with the Python CLI, then expose it to coding agents through **MCP** (`agenthub-mcp` or `@agenthub-mcp/mcp`) or embed it in applications with the **Python/npm SDK**. Fetched resource bodies are cached on disk (`.agenthub-cache/`) for faster repeat access.

**Status:** v0.1 working product — SDK, MCP, install, connect, and cache run without access-key gating.

## Repository layout

| Path | Purpose |
|------|---------|
| `global/` | Shared catalog: skills, agents, rules, prompts, hooks |
| `bundles/` | 21 department/product bundles (see inventory below) |
| `packages/python/agenthub/` | Python SDK + CLI (`agenthub install`, `connect`, `search`, cache) |
| `packages/python/agenthub-mcp/` | Python MCP server (`agenthub-mcp --stdio`, 13 tools) |
| `packages/npm/mcp/` | TypeScript MCP server (`@agenthub-mcp/mcp`) |
| `packages/npm/sdk/` | TypeScript catalog SDK (`@agenthub-mcp/sdk`) |
| `doc/` | Deployment guide and architecture research |
| `examples/` | Download/connect quickstart and MCP stdio smoke test |
| `scripts/` | Catalog generation and bundle maintenance utilities |
| `.github/workflows/ci.yml` | Python and npm package CI |

## Bundle inventory

21 bundles · **141 bundle skills** + **6 global skills** when the full catalog is installed.

| Bundle | Skills | Purpose |
|--------|--------|---------|
| `sw-engineering-ai-augmented` | 32 | ASPICE-aligned automotive C++ software engineering |
| `web-development` | 16 | Full-stack web: Node, React, Next, Vue, Angular, UI/UX |
| `r-and-d` | 13 | Research, feasibility, experimentation, IP, engineering handoff |
| `software-engineering-general` | 8 | Language-agnostic TDD, architecture, API design, RFCs |
| `product-management` | 7 | Discovery, PRDs, roadmaps, prioritization, sprint planning |
| `devops-sre` | 7 | CI/CD, deployments, incidents, SLOs, monitoring |
| `marketing` | 6 | Campaigns, SEO, content, email, landing pages |
| `sales` | 6 | Discovery, outreach, battlecards, lead qualification |
| `ai-operations` | 5 | Prompt engineering, RAG, LLM risk, multi-agent workflows |
| `data-analytics` | 5 | SQL, EDA, dashboards, KPI definition |
| `customer-success` | 5 | Support triage, KB articles, QBR, churn analysis |
| `document-processing` | 4 | DOCX, XLSX, PPTX, PDF authoring and extraction |
| `security` | 4 | Threat modeling, OWASP review, vulnerability triage |
| `finance` | 4 | Budgeting, forecasting, variance, unit economics |
| `human-resources` | 4 | Job descriptions, interviews, onboarding |
| `operations` | 4 | SOPs, process optimization, business cases, status reports |
| `program-management` | 3 | RAID logs, stakeholder analysis, program status |
| `strategy-executive` | 3 | Strategic planning, SWOT, competitive landscape |
| `procurement-supply-chain` | 2 | RFP drafting and vendor evaluation |
| `legal-compliance` | 2 | Contract checklists and NDA triage (operational support) |
| `communications` | 1 | Internal org announcements and change messaging |

Global meta skill: `skill-authoring`. Filter visible bundles with `AGENTHUB_BUNDLE` (comma-separated) — see [deployment guide](doc/deployment-guide.md).

## Architecture split

| Surface | Repo | Audience |
|---------|------|----------|
| Marketing / docs site (`docs/`) | **Public** GitHub Pages | Anyone |
| Packages + catalog + MCP | **Public** [`BeeNeural-com/agenthub`](https://github.com/BeeNeural-com/agenthub) | Anyone |

End users **do not need a full clone**. Prefer `pip install agenthub agenthub-mcp` (PyPI), or public git subdirectories; then `agenthub install --source` to download only `global/` + `bundles/` into `~/.agenthub`. No GitHub token required.

## Quick start (no full clone)

**PowerShell** — public repo, no token:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install agenthub agenthub-mcp
# Fallback if PyPI not published yet:
# pip install "agenthub @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
# pip install "agenthub-mcp @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"

agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json
# Restart Cursor
```

### Maintainer / local checkout (optional)

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -e packages\python\agenthub -e packages\python\agenthub-mcp

agenthub install --full --target .agenthub --source .
agenthub connect --catalog .\.agenthub --output .cursor\mcp.json
```

**bash (no-clone)**

```bash
pip install agenthub agenthub-mcp
# Fallback:
# pip install "agenthub @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
# pip install "agenthub-mcp @ git+https://github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"
agenthub install --full --target ~/.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub connect --catalog ~/.agenthub --output .cursor/mcp.json
```

### Optional: npm MCP runtime

```powershell
# After @agenthub-mcp/mcp is published or installed from public git subdirectory
agenthub connect --catalog $HOME\.agenthub --runtime npm --output .cursor\mcp.json
```

Details: [examples/download-and-connect.md](examples/download-and-connect.md) · [doc/deployment-guide.md](doc/deployment-guide.md)

## MCP in Cursor

Generate `.cursor/mcp.json` with `agenthub connect`, then restart Cursor. The **agenthub** server exposes 13 tools (`list_skills`, `get_skill`, `list_agents`, …).

**Department subset (multi-bundle MCP filter):**

```json
"env": {
  "AGENTHUB_CATALOG_PATH": "C:\\path\\to\\.agenthub",
  "AGENTHUB_BUNDLE": "web-development,software-engineering-general,product-management,security"
}
```

**Full company preset (all 21 bundles):**

```
document-processing,product-management,devops-sre,software-engineering-general,web-development,ai-operations,data-analytics,security,marketing,sales,customer-success,finance,human-resources,operations,program-management,legal-compliance,strategy-executive,communications,procurement-supply-chain,r-and-d,sw-engineering-ai-augmented
```

See [`.cursor/mcp.json`](.cursor/mcp.json) for a dev checkout example.

## Fetch cache

MCP `get_*` / `get_*_file` tools and SDK reads cache resource bodies under `<catalog>/.agenthub-cache/` (override with `AGENTHUB_CACHE_PATH`). `list_*` tools stay metadata-only.

```powershell
agenthub cache status --catalog .\.agenthub
agenthub cache clear --catalog .\.agenthub
```

Safe to delete `.agenthub-cache/` at any time; entries rebuild on next fetch. Embed without MCP: `Catalog(catalog_path=".agenthub")` — see [Python SDK README](packages/python/agenthub/README.md).

## Documentation

| Document | Purpose |
|----------|---------|
| [doc/deployment-guide.md](doc/deployment-guide.md) | End-to-end install, MCP, CI, environment reference |
| [examples/download-and-connect.md](examples/download-and-connect.md) | Short download & connect walkthrough |
| [doc/research/](doc/research/) | Architecture, requirements, skills expansion, distribution models |
| [packages/python/agenthub/README.md](packages/python/agenthub/README.md) | Python CLI reference |
| [packages/npm/mcp/README.md](packages/npm/mcp/README.md) | npm MCP server reference |

## Contributing

1. Add or edit resources under `global/` or `bundles/<bundle-id>/` (skills, agents, rules, prompts with `manifest.yaml` + body files).
2. Use [Conventional Commits](https://www.conventionalcommits.org/).
3. Open a PR; CI runs Python and npm package tests (`.github/workflows/ci.yml`).

### Resource frontmatter

```yaml
---
name: My Resource Name
description: One-line summary shown in catalog listings.
tags:
  - relevant-tag
---
```

## License

CARIAD SE
