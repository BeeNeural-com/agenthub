# Agent Hub Product Requirements

**Source research:** [agenthub-universal-mcp-sdk.md](./agenthub-universal-mcp-sdk.md)  
**Date:** 2026-08-20  
**Status:** approved for implementation  
**Traceability:** Pipeline A (research → requirements) via `research-to-requirements` skill

---

## Problem statement

Users must be able to **download** Agent Hub content at three granularities and **connect** it to either a **coding agent** (MCP) or an **application** (SDK/RAG) without cloning the full git repo.

---

## Functional requirements

### Download & install

| ID | Type | Statement | Priority | Research trace |
|----|------|-----------|----------|----------------|
| req-dl-001 | functional | The system shall allow installing the **entire Agent Hub catalog** to a local directory via CLI (`agenthub install --full`). | must | [research:agenthub-universal-mcp-sdk:§10.1] |
| req-dl-002 | functional | The system shall allow installing a **single bundle** (e.g. `r-and-d`) plus global resources via `agenthub install --bundle <id>`. | must | [research:agenthub-universal-mcp-sdk:§10.1] |
| req-dl-003 | functional | The system shall allow installing a **single resource** (skill, agent, rule, or prompt) via `agenthub install --skill <id>` (and `--agent`, `--rule`, `--prompt`). | must | [research:agenthub-universal-mcp-sdk:§10.1] |
| req-dl-004 | functional | Every install shall write `agenthub-lock.json` listing installed bundles and file paths. | must | [research:agenthub-universal-mcp-sdk:§10.2] |
| req-dl-005 | functional | Installed catalog shall be loadable via `AGENTHUB_CATALOG_PATH` without git checkout. | must | [research:agenthub-universal-mcp-sdk:§10.2] |

### Connect — coding agents (MCP)

| ID | Type | Statement | Priority | Research trace |
|----|------|-----------|----------|----------------|
| req-mcp-001 | functional | The system shall expose MCP tools: list/get for skills, agents, rules, prompts (+ file fetch, list_bundles). | must | [research:agenthub-universal-mcp-sdk:§3.5] |
| req-mcp-002 | functional | MCP server shall support **stdio** transport for Cursor, Claude Code, Copilot. | must | [research:agenthub-universal-mcp-sdk:§3.1] |
| req-mcp-003 | functional | CLI shall generate `.cursor/mcp.json` via `agenthub connect --output <path>`. | must | [research:agenthub-universal-mcp-sdk:§10.3] |
| req-mcp-004 | functional | MCP server shall support **streamable-http** via `agenthub-mcp serve --port <n>`. | should | [research:agenthub-universal-mcp-sdk:§5-P2] |
| req-mcp-005 | non-functional | MCP tool descriptions shall use progressive disclosure (index cheap, body on demand). | must | [research:agenthub-universal-mcp-sdk:§4.1] |

### Connect — applications (SDK / RAG)

| ID | Type | Statement | Priority | Research trace |
|----|------|-----------|----------|----------------|
| req-sdk-001 | functional | Python SDK shall provide `Catalog` with `list_*`, `get`, `search`, `read_file`. | must | [research:agenthub-universal-mcp-sdk:§3.2] |
| req-sdk-002 | functional | SDK shall export `as_rag_documents()` for vector DB indexing. | must | [research:agenthub-universal-mcp-sdk:§3.2] |
| req-sdk-003 | functional | CLI shall export JSONL via `agenthub export-rag --output <file>`. | must | [research:agenthub-universal-mcp-sdk:§10.4] |
| req-sdk-004 | functional | TypeScript `@agenthub-mcp/sdk` shall mirror Python Catalog API. | should | [research:agenthub-universal-mcp-sdk:§5-P1] |
| req-sdk-005 | non-functional | SDK embed mode shall not require MCP subprocess or pydantic MCP server deps. | must | [research:agenthub-universal-mcp-sdk:§4.1] |

### Distribution

| ID | Type | Statement | Priority | Research trace |
|----|------|-----------|----------|----------------|
| req-dist-001 | functional | Publish `agenthub` and `agenthub-mcp` on PyPI; `@agenthub-mcp/mcp` on npm. | must | [research:agenthub-universal-mcp-sdk:§5-P0] |
| req-dist-002 | constraint | Pin `mcp>=1.2,<2` until FastMCP migration path is documented. | must | [research:agenthub-universal-mcp-sdk:§7] |
| req-dist-003 | functional | Support env `AGENTHUB_BUNDLE` for bundle selection at runtime. | must | [research:agenthub-universal-mcp-sdk:§6] |

### Access control (deployment gate) — **deferred**

| ID | Type | Statement | Priority | Status |
|----|------|-----------|----------|--------|
| req-auth-001 | functional | SDK and MCP server shall require non-empty `AGENTHUB_ACCESS_KEY` before any catalog operation. | must | **deferred** — gating disabled in v0.1 |
| req-auth-002 | functional | When `AGENTHUB_ACCESS_KEY_SHA256` is set, the access key shall be verified against that SHA-256 hex digest. | must | **deferred** |
| req-auth-003 | functional | `agenthub connect` shall propagate access-key env vars into generated MCP config. | must | **deferred** |

### Modular architecture

| ID | Type | Statement | Priority | Research trace |
|----|------|-----------|----------|----------------|
| req-arch-001 | non-functional | SDK and MCP server shall load catalog from disk via `AGENTHUB_CATALOG_PATH`; neither shall embed catalog content in the package wheel in v0.1. | must | [deployment-guide:§1] |
| req-arch-002 | non-functional | Catalog install (`agenthub install`) and runtime load shall be decoupled — updating catalog shall not require package reinstall. | must | [deployment-guide:§1] |

---

## User journeys

Access-key gating is deferred (see [deployment guide §2](../deployment-guide.md#2-access-key-deferred)).

### Journey 1: Developer — full Agent Hub in Cursor

```bash
agenthub install --full --target ~/.agenthub --source /path/to/agenthub-repo
agenthub connect --catalog ~/.agenthub --output ~/.cursor/mcp.json
# Restart Cursor → agenthub MCP live with all skills
```

### Journey 2: Team — R&D bundle only

```bash
agenthub install --bundle r-and-d --target ./.agenthub --source /path/to/agenthub-repo
export AGENTHUB_CATALOG_PATH=./.agenthub
agenthub-mcp --stdio
```

### Journey 3: App — single skill in RAG pipeline

```bash
agenthub install --skill feasibility-study --target ./kb --source /path/to/agenthub-repo
python -c "
from agenthub import Catalog
cat = Catalog(catalog_path='./kb')
docs = cat.as_rag_documents(resource_types=('skill',))
"
```

### Journey 4: Custom agent — MCP HTTP

```bash
agenthub-mcp serve --port 8080 --catalog ./.agenthub   # planned v0.2
# App uses MCP Client SDK → http://localhost:8080/mcp
```

### Journey 5: Fellow developer validation

See [deployment guide §8](../deployment-guide.md#8-fellow-developer-test-plan-minimal-reproducible) for the 10-step reproducible checklist including stdio smoke test and key-gating verification.

---

## Out of scope (v0.1)

- OAuth enterprise auth
- Remote catalog CDN (use local install first)
- TypeScript native MCP server (npm wrapper only for v0.1)
- MCP registry publish (v0.2)

---

## Recommended epics

1. **Epic: Download & lockfile** — req-dl-* (CLI install modes) ✅ prototype in `packages/python/agenthub`
2. **Epic: MCP universal server** — req-mcp-* (stdio + publish)
3. **Epic: Embed SDK & RAG export** — req-sdk-* ✅ prototype Catalog + export-rag
4. **Epic: npm/pip distribution** — req-dist-* ✅ CI in `.github/workflows/ci.yml`
5. **Epic: Deployment docs & access gate** — req-auth-*, req-arch-* ✅ [deployment-guide.md](../deployment-guide.md)
