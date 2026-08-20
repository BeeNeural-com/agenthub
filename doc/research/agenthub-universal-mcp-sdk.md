# Research Report: Agent Hub as Universal MCP Server & Embeddable SDK

**Author:** Agent Hub R&D (via Cursor)  
**Date:** 2026-08-20  
**Version:** 2.0  
**Status:** final — R&D complete  
**Confidence:** High on architecture and download/connect model; Medium on market sizing

---

## Executive summary

Agent Hub should ship as a **three-layer product**, not a single MCP script:

1. **MCP server (stdio + HTTP)** — drop-in for any coding agent (Cursor, Claude Code, Copilot, Cline, Continue, custom agents)
2. **Client SDK (npm + pip)** — programmatic access for RAG pipelines, agent frameworks, and app backends without requiring MCP host support
3. **Resource catalog package** — versioned skills/agents/rules/prompts as installable data, decoupled from server runtime

The former `mcp-poc/server.py` (now `packages/python/agenthub-mcp`) proved the protocol surface works (49 skills, 21 agents, 32 rules, 4 prompts in the expanded build). The gap is **distribution, transport, and embeddability** — not MCP protocol design.

**Recommendation:** **Proceed.** Ship granular download (full / bundle / single skill) plus dual connect (MCP for coding agents, SDK for applications). Python packages `agenthub` + `agenthub-mcp` are implemented in `packages/python/`.

**Related deliverables:**
- **[Deployment & developer guide](../deployment-guide.md)** — install, access key, MCP config, test checklist
- [Feasibility study](./feasibility-agenthub-distribution.md) — **Proceed**
- [Trade study: download models](./trade-study-download-models.md) — Hybrid granular install wins
- [Product requirements](./agenthub-product-requirements.md) — 20 requirements, 4 user journeys

---

## 1. Background and motivation

### Problem

Today's Agent Hub MCP is:
- Bound to a git checkout (`REPO_ROOT = parent.parent`)
- Python-only, venv-dependent
- stdio-only
- Not publishable as `npx agenthub-mcp` or `pip install agenthub-mcp`
- Not consumable by RAG systems that want skill *content* without running an MCP subprocess

### Goal

Make Agent Hub usable in **two consumption modes**:

| Mode | Consumer | Interface |
|------|----------|-----------|
| **A. Coding agent** | Cursor, Claude Code, Copilot, Windsurf | MCP stdio or HTTP in `mcp.json` |
| **B. Application embed** | RAG apps, LangChain/LlamaIndex agents, custom backends | Python/TS library: load catalog, search, fetch bodies |

Both modes should share one catalog, one versioning scheme, one update channel.

### User download model (new — trade study winner)

Users install Agent Hub at **three granularities**:

| Granularity | CLI | Use case |
|-------------|-----|----------|
| **Full catalog** | `agenthub install --full` | Enterprise platform team, full R&D + SWE |
| **Bundle** | `agenthub install --bundle r-and-d` | Department gets R&D skills + agents only |
| **Single resource** | `agenthub install --skill feasibility-study` | One skill in a RAG KB or sidecar |

Install writes `.agenthub/` (or custom path) + `agenthub-lock.json`. Runtime uses `AGENTHUB_CATALOG_PATH` — no git clone.

### User connect model (new)

| Consumer | How they connect | Interface |
|----------|------------------|-----------|
| **Cursor / Claude / Copilot** | `agenthub connect` → MCP stdio | `mcp.json` |
| **Custom coding agent** | `uvx agenthub-mcp --stdio` or HTTP | MCP Client SDK |
| **RAG application** | `pip install agenthub` | `Catalog.as_rag_documents()` |
| **LangChain / agent framework** | SDK search as tool OR MCP Client | Python/TS API |
| **Airgapped** | `agenthub install --full` then local MCP | No network after install |

### What already exists in this repo

| Asset | Maturity | Relevance |
|-------|----------|-----------|
| `packages/python/agenthub` loader | Working | Generic resource loader — foundation for SDK |
| `packages/python/agenthub-mcp` | Working | 13 MCP tools, progressive disclosure |
| `global/` + `bundles/` | Rich content | 49+ skills, agents, rules |
| Legacy HTTP POC notes (removed) | Design only | Former REST model — different from MCP stdio; useful for hosted catalog ideas |
| `agenthub-reg` / `agenthub-cli` (external) | Referenced in README | Catalog scanner + installer — potential integration point |

---

## 2. Methodology

Research conducted using Agent Hub R&D workflow:

1. **Technology scouting** — MCP SDK docs, npm publish patterns, embed frameworks (mcp-use, official SDKs)
2. **Codebase analysis** — current loader, server, bundle structure
3. **Competitive landscape** — how published MCP servers ship (npx, uvx, HTTP)
4. **Feasibility framing** — TRL assessment and architecture trade study

Sources: [MCP TypeScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [MCP server build guide](https://modelcontextprotocol.io/docs/develop/build-server), [npm MCP publish guide](https://www.aihero.dev/publish-your-mcp-server-to-npm), [mcp-use Python framework](https://github.com/mcp-use/mcp-use), current repo `packages/python/agenthub-mcp`.

---

## 3. Findings

### 3.1 MCP ecosystem: five distribution patterns (2026)

Industry has converged on layered shipping:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: Hosted HTTP MCP (remote URL in mcp.json)          │
│  Layer 4: OAuth / Bearer auth (enterprise)                  │
│  Layer 3: npm npx / pip uvx / pip install (stdio CLI)       │
│  Layer 2: .mcpb one-click installer (Claude Desktop)        │
│  Layer 1: Local script / git clone (dev only)               │
└─────────────────────────────────────────────────────────────┘
```

**For Agent Hub, Layers 3 + 5 are the target.** Layer 1 is what you have today.

Published MCP servers use:

```json
// npm pattern (Cursor, Claude, VS Code)
{
  "mcpServers": {
    "agenthub": {
      "command": "npx",
      "args": ["-y", "@agenthub/mcp@latest"]
    }
  }
}
```

```json
// Python pattern
{
  "mcpServers": {
    "agenthub": {
      "command": "uvx",
      "args": ["agenthub-mcp", "--stdio"]
    }
  }
}
```

```json
// HTTP pattern (production, RAG backends, cloud agents)
{
  "mcpServers": {
    "agenthub": {
      "url": "https://mcp.agenthub.example/mcp",
      "headers": { "Authorization": "Bearer ${env:AGENTHUB_TOKEN}" }
    }
  }
}
```

### 3.2 Embed-without-MCP: the RAG use case

Many agentic applications **do not run an MCP host**. They need:

- Skill/agent content as **documents** for retrieval
- Structured metadata (id, tags, description) for routing
- Optional tool-call wrappers if the app has its own tool loop

The official MCP Python SDK now exposes a **`Client` in ~10 lines** for HTTP, but RAG pipelines often skip MCP entirely and load markdown directly.

**Implication:** Ship **`agenthub` library** (not just MCP server) with:

```python
from agenthub import Catalog

catalog = Catalog(bundles=["r-and-d", "sw-engineering-ai-augmented"])
skills = catalog.search("feasibility study", type="skill")
body = catalog.get("feasibility-study").body
```

```typescript
import { Catalog } from "@agenthub/sdk";

const catalog = new Catalog({ bundles: ["r-and-d"] });
const skills = await catalog.search("feasibility study", { type: "skill" });
const body = await catalog.get("feasibility-study").body;
```

This is **lower latency** than subprocess MCP for RAG indexing and avoids Windows Smart App Control / pydantic DLL issues entirely in embed mode.

### 3.3 Current codebase: what's reusable vs must change

| Component | Reusable | Must change |
|-----------|----------|-------------|
| `loader.py` | ✅ 90% | Package-relative paths, not `REPO_ROOT` git assumption |
| `server.py` tool definitions | ✅ 80% | Extract to shared module; add HTTP transport |
| `global/` + `bundles/` content | ✅ 100% | Ship as package data or remote catalog |
| Progressive disclosure design | ✅ 100% | Keep — critical at 49+ skills scale |
| Legacy `agenthub-poc/` FastAPI HTTP (removed) | ⚠️ Partial | Wrong abstraction (REST download vs MCP HTTP) — don't merge blindly |

**Critical bug already fixed in expanded build:** `get_skill_file` used `SKILLS_ROOT / skill_id` instead of `skill.folder` — loader now tracks `folder` correctly.

### 3.4 Technology scouting matrix

| Option | Technical fit | Maturity | TCO | Agent compatibility | Embed/RAG fit | **Score** |
|--------|---------------|----------|-----|---------------------|---------------|-----------|
| **A. Python MCP only (pip)** | High | TRL 6 | Low | Good (Cursor, Claude) | Poor | 3.8 |
| **B. npm wrapper + Python core** | High | TRL 5 | Medium | Excellent (npx universal) | Poor | 4.0 |
| **C. Dual SDK (Py + TS) + shared catalog** | High | TRL 4 | Medium | Excellent | **Excellent** | **4.6** |
| **D. HTTP-only hosted MCP** | High | TRL 3 | High (ops) | Excellent | Good | 3.5 |
| **E. REST catalog only (no MCP)** | Medium | TRL 4 | Low | Poor | Excellent | 3.2 |

**Winner: Option C** — dual SDK + MCP server CLI wrappers + optional HTTP.

Option D becomes a deployment target for Option C, not a replacement.

### 3.5 Proposed target architecture

```
agenthub/                          # monorepo
├── packages/
│   ├── catalog/                   # JSON + markdown tarball, versioned
│   │   ├── global/
│   │   └── bundles/
│   ├── python/
│   │   ├── agenthub/              # pip: agenthub — Catalog SDK
│   │   └── agenthub-mcp/          # pip: agenthub-mcp — MCP server CLI
│   └── typescript/
│       ├── @agenthub/sdk/         # npm: programmatic catalog
│       └── @agenthub/mcp/         # npm: npx MCP server (spawns py or native TS)
├── packages/python/agenthub-mcp/  # MCP server (migrated from mcp-poc)
└── .cursor/mcp.json
```

#### Surface 1: MCP server (coding agents)

**Tools (keep all 13):**
- `list_skills`, `get_skill`, `get_skill_file`
- `list_agents`, `get_agent`, `get_agent_file`
- `list_rules`, `get_rule`, `get_rule_file`
- `list_prompts`, `get_prompt`, `get_prompt_file`
- `list_bundles`

**Transports:**
1. `stdio` — default for local agents
2. `streamable-http` — `agenthub-mcp serve --port 8080` for cloud/RAG/agent frameworks using MCP Client

**CLI:**
```bash
# Python
uvx agenthub-mcp --stdio
uvx agenthub-mcp serve --port 8080

# npm (wrapper or native TS port)
npx -y @agenthub/mcp
```

#### Surface 2: Embed SDK (RAG / agentic apps)

**Python (`pip install agenthub`):**
```python
from agenthub import Catalog

catalog = Catalog()  # loads bundled catalog from package data
index = catalog.list_skills()           # cheap metadata
doc = catalog.get_skill("literature-review")  # full body
chunks = catalog.as_rag_documents()     # List[{id, text, metadata}] for vector DB
```

**TypeScript (`npm install @agenthub/sdk`):**
```typescript
import { Catalog } from "@agenthub/sdk";
const catalog = new Catalog();
const chunks = await catalog.asRagDocuments({ bundles: ["r-and-d"] });
```

**RAG integration patterns:**

| Pattern | How Agent Hub fits |
|---------|-------------------|
| **Naive RAG** | Index all skill bodies + descriptions into vector DB via `as_rag_documents()` |
| **Router RAG** | Index descriptions only; retrieve full body on match (mirrors MCP progressive disclosure) |
| **Agentic RAG** | Expose `catalog.search()` as a tool in LangChain/LlamaIndex/mcp-use agent |
| **MCP-native agent** | Use `@modelcontextprotocol/sdk` Client pointing at stdio or HTTP server |

#### Surface 3: Remote catalog (optional, aligns with agenthub-reg)

For teams that don't want 50MB of skills in every install:

```python
catalog = Catalog(remote="https://catalog.agenthub.example/v1")
```

Uses existing `catalog.json` pipeline from agenthub-reg / agenthub-site. Local package becomes a cache layer.

---

## 4. Analysis and discussion

### 4.1 Why both MCP *and* SDK?

MCP solves **agent host integration** (Cursor discovers tools, approval flows, deferred loading). SDK solves **application integration** (your Flask app, RAG pipeline, or custom agent loop doesn't want a subprocess per request).

Trying to force RAG apps through stdio MCP adds:
- Process spawn overhead
- Platform-specific Python/venv issues (Smart App Control blocking pydantic on Windows)
- Complexity for apps that only need markdown content

The catalog content is the **shared asset**; MCP and SDK are **two transports** over the same data.

### 4.2 npm *and* pip: not redundant

| Ecosystem | Why needed |
|-----------|------------|
| **pip / uvx** | FastMCP server is Python; data science / ML RAG stacks are Python-heavy |
| **npm / npx** | Cursor, Claude Desktop, VS Code default to `npx` patterns; Node agents (mcp-use TS) |

**Pragmatic approach:** Author server in Python (reuse `loader.py` + FastMCP). npm package is a thin launcher:

```javascript
// @agenthub/mcp/bin/agenthub-mcp.js
import { spawn } from "child_process";
spawn("uvx", ["agenthub-mcp", "--stdio"], { stdio: "inherit" });
```

Long-term: TypeScript native server for zero Python dependency in Node-only environments.

### 4.3 TRL assessment

| Component | Current TRL | Target TRL | Gap |
|-----------|-------------|------------|-----|
| MCP stdio server | 6 (demo validated) | 8 | Packaging, tests, CI |
| Multi-bundle loader | 6 | 8 | Package-relative paths |
| MCP HTTP transport | 2 | 7 | Implement `serve` command |
| pip package | 1 | 8 | pyproject.toml, package_data |
| npm package | 1 | 7 | bin wrapper + optional TS port |
| Embed SDK | 2 | 8 | Extract loader, RAG helpers |
| Remote catalog | 3 (agenthub-reg exists) | 7 | Wire catalog.json fetch |

### 4.4 Competitive positioning

Agent Hub is **not** a generic MCP tool server (filesystem, git, browser). It's a **domain-specific knowledge server** — closer to:

- Internal Cursor skills / rules
- Custom GPT knowledge bases
- Enterprise prompt libraries

Differentiation:
- **Progressive disclosure** (index → fetch) — token-efficient at scale
- **Typed resources** (skills, agents, rules, prompts) — not flat documents
- **Bundles** (R&D, SWE, custom) — departmental deployment
- **Dual MCP + SDK** — only platform that serves both coding agents and RAG backends from one catalog

---

## 5. Recommendations (prioritized)

### P0 — Must have for "works anywhere"

1. **Extract `loader.py` → `agenthub` Python package** with package-data catalog
2. **Publish `agenthub-mcp` CLI** — `uvx agenthub-mcp --stdio`
3. **Publish `@agenthub/mcp` npm wrapper** — `npx -y @agenthub/mcp`
4. **Single config env vars:** `AGENTHUB_BUNDLE`, `AGENTHUB_CATALOG_PATH`, `AGENTHUB_TOOL_DESC_MODE`
5. **MCP registry metadata** — `mcpName` in package.json for discoverability

### P1 — Embeddable SDK for RAG/agent apps

6. **`Catalog.as_rag_documents()`** — emit chunks with metadata for vector indexing
7. **`Catalog.search(query, type, tags)`** — lightweight routing without vectors
8. **TypeScript `@agenthub/sdk`** — mirror Python API
9. **Integration examples:** LangChain, LlamaIndex, mcp-use, raw OpenAI tools

### P2 — Production deployment

10. **HTTP transport** — `agenthub-mcp serve --port 8080`
11. **Remote catalog sync** — pull from agenthub-reg / catalog.json
12. **Auth** — Bearer token for HTTP; OAuth for enterprise
13. **Version pinning** — `npx @agenthub/mcp@1.2.3`, lockfile in apps

### P3 — Ecosystem

14. **Custom bundle CLI** — `agenthub bundle create my-team/`
15. **MCP Apps extension** — interactive skill browser UI
16. **VS Code extension** — one-click bundle install

---

## 6. Proposed package API sketch

### Python MCP CLI (`pyproject.toml`)

```toml
[project]
name = "agenthub-mcp"
version = "0.1.0"
dependencies = ["agenthub", "mcp>=1.2,<2"]

[project.scripts]
agenthub-mcp = "agenthub_mcp.cli:main"

[tool.setuptools.package-data]
agenthub = ["catalog/**/*"]
```

### Python SDK

```python
# agenthub/catalog.py
class Catalog:
    def __init__(self, bundles=None, catalog_path=None, remote=None): ...
    def list_skills(self) -> list[ResourceMeta]: ...
    def get_skill(self, skill_id: str) -> Resource: ...
    def search(self, query: str, *, type=None, tags=None, limit=10) -> list[ResourceMeta]: ...
    def as_rag_documents(self, *, bundles=None, types=("skill",)) -> list[RagDocument]: ...
```

### npm

```json
{
  "name": "@agenthub/mcp",
  "bin": { "agenthub-mcp": "./dist/cli.js" },
  "mcpName": "io.agenthub/mcp"
}
```

---

## 7. Risks and open questions

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Catalog size bloat in npm/pip packages | Medium | Split bundles; remote catalog; lazy download |
| Python/Node dual maintenance | Medium | Shared catalog JSON; codegen types from manifest schema |
| MCP spec churn (SDK v2, FastMCP standalone) | Medium | Pin `mcp>=1.2,<2`; migration guide when v2 stabilizes |
| Windows deployment (Smart App Control) | High | npm wrapper with embedded runtime; HTTP mode; pure TS port |
| Duplicate agent IDs across bundles | Low | Already handled — global wins, log warning |
| Legal/licensing of bundled content | Low | CARIAD SE license already in README |

**Open questions:**
1. Should catalog updates ship independently of server (`agenthub-catalog` package)?
2. Host public HTTP MCP or only private enterprise?
3. Integrate with existing `agenthub-cli install` or replace it?
4. TypeScript native server vs Python-only for v1?

---

## 8. Suggested implementation sequence (single sprint)

Since you asked for complete delivery, this is the **minimum shippable universal product**:

```
Week 1: Python packages
  ├── agenthub/          (loader + Catalog SDK + as_rag_documents)
  └── agenthub-mcp/      (server.py migrated, CLI entry point, package_data)

Week 2: Distribution
  ├── PyPI publish agenthub + agenthub-mcp
  ├── npm @agenthub/mcp wrapper
  └── MCP registry publish

Week 3: HTTP + TS SDK
  ├── agenthub-mcp serve (streamable-http)
  ├── @agenthub/sdk (TypeScript Catalog)
  └── Examples: LangChain RAG + Cursor mcp.json
```

---

## 9. Immediate next action

R&D is **complete**. For day-to-day deployment, use the **[Deployment & developer guide](../deployment-guide.md)**.

Implementation lives in:

| Package | Path | Status |
|---------|------|--------|
| `agenthub` SDK + CLI | `packages/python/agenthub/` | ✅ tested |
| `agenthub-mcp` MCP server (Python) | `packages/python/agenthub-mcp/` | ✅ stdio |
| `@agenthub/mcp` MCP server (npm) | `packages/npm/mcp/` | ✅ stdio |
| Deployment guide | `doc/deployment-guide.md` | ✅ |
| Quickstart | `examples/download-and-connect.md` | ✅ |
| Stdio smoke test | `examples/test-mcp-stdio.py` | ✅ |

```bash
# From repo root (dev) — see deployment guide for full checklist
pip install -e packages/python/agenthub -e packages/python/agenthub-mcp
export AGENTHUB_CATALOG_PATH=$PWD

agenthub install --bundle r-and-d --target .agenthub --source $PWD
agenthub list skills
agenthub connect --catalog .agenthub --output .cursor/mcp.json
python examples/test-mcp-stdio.py
```

**Implementation epics:** see [agenthub-product-requirements.md](./agenthub-product-requirements.md).

---

## 10. Download & connect specification (final)

### 10.1 Install CLI

```bash
agenthub install --full [--target PATH]           # entire catalog
agenthub install --bundle r-and-d [--target PATH] # bundle + global
agenthub install --skill <id> [--target PATH]     # single skill
agenthub install --agent <id>                     # single agent
agenthub install --rule <id>                      # single rule
agenthub install --prompt <id>                    # single prompt
```

### 10.2 Lockfile (`agenthub-lock.json`)

```json
{
  "lockfileVersion": 1,
  "generatedAt": "2026-08-20T...",
  "bundles": ["r-and-d"],
  "resources": ["global/skills/...", "bundles/r-and-d/skills/..."],
  "catalogPath": "/path/to/.agenthub"
}
```

### 10.3 Connect — coding agent

```bash
agenthub connect --catalog ~/.agenthub --output .cursor/mcp.json
```

Generated config:

```json
{
  "mcpServers": {
    "agenthub": {
      "type": "stdio",
      "command": "uvx",
      "args": ["agenthub-mcp", "--stdio"],
      "env": {
        "AGENTHUB_CATALOG_PATH": "/home/user/.agenthub",
        "AGENTHUB_BUNDLE": "r-and-d"
      }
    }
  }
}
```

### 10.4 Connect — application / RAG

```python
from agenthub import Catalog

# After: agenthub install --bundle r-and-d --target ./kb
catalog = Catalog(catalog_path="./kb")

# Router RAG: index descriptions only
for meta in catalog.list_skills():
    vector_db.upsert(meta.id, meta.description, meta=meta.__dict__)

# On match: fetch full body
skill = catalog.get_skill("feasibility-study")
agent.run(system=skill.body)

# Bulk export
docs = catalog.as_rag_documents(resource_types=("skill", "agent"))
```

```bash
agenthub export-rag --output skills.jsonl --type skill --bundles r-and-d
```

### 10.5 Connect — MCP Client in application

```python
from mcp import Client

async with Client("http://localhost:8080/mcp") as client:
    tools = await client.list_tools()
    result = await client.call_tool("get_skill", {"skill_id": "literature-review"})
```

### 10.6 Deployment access key (deferred)

Access-key gating (`AGENTHUB_ACCESS_KEY`) was designed for team rollout but is **disabled in v0.1**. Stub modules (`_auth.py`, `auth.ts`) remain for future enforcement. See [deployment-guide.md §2](../deployment-guide.md#2-access-key-deferred).

| Variable | Required (v0.1) | Behavior when re-enabled |
|----------|-----------------|--------------------------|
| `AGENTHUB_ACCESS_KEY` | No | Non-empty string; missing → `AccessKeyError`, exit 1 |
| `AGENTHUB_ACCESS_KEY_SHA256` | No | When set, key must match SHA-256 hex digest |

### 10.7 Modular decoupling (runtime contract)

```
agenthub install  →  .agenthub/ + agenthub-lock.json   (data layer)
                              ↓ AGENTHUB_CATALOG_PATH
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
  agenthub.Catalog (SDK)                   agenthub-mcp / @agenthub/mcp
  no MCP subprocess                        stdio MCP for coding agents
```

Neither the SDK nor the MCP server bundles catalog markdown at build time in v0.1. Both read the same on-disk tree. Update catalog by re-running `agenthub install` or swapping `AGENTHUB_CATALOG_PATH` — no package reinstall required.

---

## 11. R&D pipeline completion checklist

| Stage | Skill used | Deliverable | Status |
|-------|------------|-------------|--------|
| Scouting | technology-scouting | §3.1–3.4 distribution patterns | ✅ |
| Literature | literature-review | MCP SDK docs, npm patterns | ✅ |
| Trade study | trade-study | [trade-study-download-models.md](./trade-study-download-models.md) | ✅ |
| Feasibility | feasibility-study | [feasibility-agenthub-distribution.md](./feasibility-agenthub-distribution.md) | ✅ **Proceed** |
| Research report | research-report | This document v2.0 | ✅ final |
| Requirements | research-to-requirements | [agenthub-product-requirements.md](./agenthub-product-requirements.md) | ✅ |
| Prototype | prototype-spike | `packages/python/agenthub/` + `agenthub-mcp/` | ✅ tested |
| Quickstart | research-to-requirements | `examples/download-and-connect.md` | ✅ |
| Deployment guide | research-to-requirements | `doc/deployment-guide.md` | ✅ |
| CI workflow | prototype-spike | `.github/workflows/ci.yml` | ✅ |

---

## References

1. [MCP TypeScript SDK (@modelcontextprotocol/sdk)](https://www.npmjs.com/package/@modelcontextprotocol/sdk) — npm distribution, client/server APIs  
2. [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — FastMCP, Client, HTTP transport  
3. [Build MCP Server (official guide)](https://modelcontextprotocol.io/docs/develop/build-server) — stdio, npm bin pattern  
4. [Publish MCP to npm](https://www.aihero.dev/publish-your-mcp-server-to-npm) — npx distribution  
5. [mcp-use framework](https://github.com/mcp-use/mcp-use) — Python agent + client + server unified framework  
6. Current repo: `packages/python/agenthub`, `packages/python/agenthub-mcp`, `bundles/r-and-d/`
