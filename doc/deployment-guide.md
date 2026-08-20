# Agent Hub — Deployment & Developer Guide

**Status:** working product (v0.1)  
**Audience:** developers installing Agent Hub for coding agents (MCP) or applications (SDK)  
**Companion research:** [agenthub-universal-mcp-sdk.md](./research/agenthub-universal-mcp-sdk.md) · [product requirements](./research/agenthub-product-requirements.md)

This is the single operational guide for getting Agent Hub running end-to-end: install packages, download catalog content, wire MCP, and verify with a minimal checklist.

---

## 1. Modular architecture (decoupled by design)

Agent Hub is intentionally split into **three independent layers** that share one on-disk catalog:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 1 — Catalog (data only)                                          │
│  global/ + bundles/  →  copied to  .agenthub/  +  agenthub-lock.json   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │  AGENTHUB_CATALOG_PATH (filesystem)
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌───────────────────────────┐     ┌───────────────────────────┐
│  Layer 2 — SDK            │     │  Layer 3 — MCP server     │
│  pip: agenthub            │     │  pip: agenthub-mcp        │
│  npm: @agenthub/sdk       │     │  npm: @agenthub/mcp       │
│  Catalog, install, search │     │  stdio MCP for IDEs       │
└───────────────────────────┘     └───────────────────────────┘
```

**Key principle:** the SDK and MCP server **do not embed catalog content**. Both read the **same directory** pointed to by `AGENTHUB_CATALOG_PATH`. You can:

- Install catalog once with `agenthub install`
- Use the Python SDK in a RAG pipeline without starting MCP
- Point Cursor at the same catalog via `agenthub-mcp --stdio`
- Swap or update the catalog directory without reinstalling packages

The Python MCP server (`agenthub-mcp`) and the TypeScript MCP server (`@agenthub/mcp`) expose the **same 13 tools** over the same catalog layout.

---

## 2. Access key (deferred)

Access-key gating (`AGENTHUB_ACCESS_KEY`) was planned for team rollout but is **disabled in v0.1**. SDK, MCP, install, and cache operations run without a key. Stub modules (`_auth.py`, `auth.ts`) remain for future enforcement.

When enabled in a later release, keys will be distributed via your team's secret store — never commit keys to git.

---

## 3. Repository layout (publishing from GitHub)

```
agenthub/                          # monorepo root
├── global/                        # catalog: global skills, agents, rules, prompts
├── bundles/                       # catalog: per-department bundles (e.g. r-and-d/)
├── packages/
│   ├── python/
│   │   ├── agenthub/              # PyPI: agenthub (SDK + install CLI)
│   │   └── agenthub-mcp/          # PyPI: agenthub-mcp (MCP server)
│   └── npm/
│       ├── mcp/                   # npm: @agenthub/mcp (TypeScript MCP server)
│       └── sdk/                   # npm: @agenthub/sdk (Catalog API)
├── examples/
│   ├── download-and-connect.md    # quickstart walkthrough
│   └── test-mcp-stdio.py          # stdio MCP smoke test
├── doc/
│   └── deployment-guide.md        # this file
└── .github/workflows/ci.yml       # package tests on push/PR
```

**Publishing targets:**

| Package | Registry | Path |
|---------|----------|------|
| `agenthub` | PyPI | `packages/python/agenthub/` |
| `agenthub-mcp` | PyPI | `packages/python/agenthub-mcp/` |
| `@agenthub/mcp` | npm | `packages/npm/mcp/` |
| `@agenthub/sdk` | npm | `packages/npm/sdk/` |

Catalog content (`global/`, `bundles/`) ships via `agenthub install --source` from GitHub (or a local checkout for maintainers) — not inside the Python/npm wheels in v0.1.

**Publishing split:** host `docs/` on a **public** Pages repo; keep this monorepo (**packages + catalog**) private at `BeeNeural-com/agenthub`.

---

## 4. Getting started — Python (`agenthub` + `agenthub-mcp`)

### 4.0 Recommended: no full clone (private BeeNeural-com/agenthub)

Public docs site → private packages/catalog. Users need a GitHub token (or SSH for pip) with read access.

```powershell
$env:GITHUB_TOKEN = "ghp_xxxxxxxx"   # also accepted: AGENTHUB_GITHUB_TOKEN

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "agenthub @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
pip install "agenthub-mcp @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"

agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json
# Restart Cursor — command is agenthub-mcp on PATH; catalog is ~/.agenthub only
```

`agenthub install --source https://github.com/...` downloads a GitHub zipball and extracts **only** `global/` + `bundles/` into the target (cached under `~/.agenthub-cache/github-sources/`).

### 4.1 Install from local checkout (maintainers)

From repo root:

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\pip install -e packages/python/agenthub -e packages/python/agenthub-mcp
```

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/python/agenthub -e packages/python/agenthub-mcp
```

### 4.2 Install from PyPI (when published)

```bash
pip install agenthub agenthub-mcp
```

### 4.3 Set catalog source

```powershell
# Remote (no clone) — preferred for end users
agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub

# Or local checkout (maintainers)
agenthub install --full --target .agenthub --source .
```

Env aliases for remote source: `AGENTHUB_CATALOG_SOURCE` / `AGENTHUB_CATALOG_URL` (e.g. `github:BeeNeural-com/agenthub`).

After install, point MCP/SDK at the **target** directory (`~/.agenthub`), not the private monorepo.

### 4.4 Download catalog (granular install)

Pick one granularity:

```powershell
# Full catalog (global + all bundles) from private GitHub
agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub

# One bundle + global
agenthub install --bundle web-development --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub

# Single resource (RAG sidecar)
agenthub install --skill feasibility-study --target ./kb --source https://github.com/BeeNeural-com/agenthub
```

Each install writes `agenthub-lock.json` listing bundles, copied paths, and source.

**Expected output (bundle install):**

```json
{
  "target": "C:\\path\\to\\.agenthub",
  "count": 142
}
```

### 4.5 SDK usage (no MCP subprocess)

```powershell
$env:AGENTHUB_CATALOG_PATH = ".\.agenthub"
```

```python
from agenthub import Catalog

catalog = Catalog(catalog_path=".agenthub")
print(len(catalog.list_skills()), "skills")
skill = catalog.get_skill("feasibility-study")
docs = catalog.as_rag_documents(resource_types=("skill",))
```

CLI equivalents:

```powershell
agenthub list skills
agenthub search "feasibility" --bundles r-and-d
agenthub export-rag --output skills.jsonl --type skill --bundles r-and-d
```

See [packages/python/agenthub/README.md](../packages/python/agenthub/README.md) for the full CLI table.

---

## 5. Getting started — npm (`@agenthub/mcp`)

The npm package is a **standalone TypeScript MCP server** for coding agents that prefer `npx` (Cursor, Claude Desktop, VS Code).

### 5.1 Install from git (dev)

```powershell
cd packages/npm/mcp
npm install
npm run build
```

### 5.2 Install from npm (when published)

```bash
npm install -g @agenthub/mcp
# or use without global install:
npx -y @agenthub/mcp --stdio
```

### 5.3 Run (requires catalog)

Catalog must already exist (install via Python `agenthub install`):

```powershell
$env:AGENTHUB_CATALOG_PATH = "C:\path\to\.agenthub"
npx @agenthub/mcp --stdio
```

See [packages/npm/mcp/README.md](../packages/npm/mcp/README.md) for `mcp.json` examples.

### 5.4 Node embed SDK (`@agenthub/sdk`)

```powershell
cd packages/npm/sdk
npm install
npm run build
```

```typescript
import { Catalog } from "@agenthub/sdk";

const catalog = new Catalog("./.agenthub");
const skill = catalog.getSkill("feasibility-study");
```

Catalog **install** and **export-rag** remain on the Python CLI (`agenthub`). The Node SDK is for reading an already-installed catalog.

---

## 6. Generate MCP config (`.cursor/mcp.json`)

```powershell
$env:AGENTHUB_CATALOG_PATH = ".\.agenthub"
agenthub connect --catalog .\.agenthub --output .cursor\mcp.json
```

**npm MCP runtime** (generates `npx @agenthub/mcp --stdio`):

```powershell
agenthub connect --catalog .\.agenthub --runtime npm --output .cursor\mcp.json
```

**Dev mode** (editable install from this repo, then use the installed binary):

```powershell
pip install -e packages\python\agenthub -e packages\python\agenthub-mcp
agenthub connect --catalog .\.agenthub --output .cursor\mcp.json
```

**Generated config (Python server, production-style):**

```json
{
  "mcpServers": {
    "agenthub": {
      "type": "stdio",
      "command": "agenthub-mcp",
      "args": ["--stdio"],
      "env": {
        "AGENTHUB_CATALOG_PATH": "C:\\path\\to\\.agenthub",
        "AGENTHUB_BUNDLE": "r-and-d"
      }
    }
  }
}
```

**npm variant** (from `--runtime npm`): `"command": "npx"`, `"args": ["@agenthub/mcp", "--stdio"]` with the same `env` block.

Restart your IDE after writing `mcp.json`.

---

## 7. Run MCP server and verify

### 7.1 Direct server start

```powershell
$env:AGENTHUB_CATALOG_PATH = ".\.agenthub"
agenthub-mcp --stdio
```

Server blocks on stdio (no HTTP in v0.1). Use the smoke test script to validate tool listing.

### 7.2 Stdio smoke test (`examples/test-mcp-stdio.py`)

Requires `agenthub-mcp` on PATH and `mcp` Python package (installed with `agenthub-mcp`):

```powershell
$env:AGENTHUB_CATALOG_PATH = ".\.agenthub"
python examples\test-mcp-stdio.py
```

**Expected output:**

```
OK: 13 tools
  - get_agent
  - get_agent_file
  ...
  - list_skills
```

### 7.3 Verify catalog load

```powershell
$env:AGENTHUB_CATALOG_PATH = ".\.agenthub"
agenthub list skills
# JSON array of skill metadata
```

---

## 8. Fellow developer test plan (minimal reproducible)

Share this checklist — **no full private clone required**.

| Step | Command | Expected |
|------|---------|----------|
| 1. Token | `$env:GITHUB_TOKEN = "ghp_..."` | Read access to `BeeNeural-com/agenthub` |
| 2. Install packages | `pip install "agenthub @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"` (+ `agenthub-mcp` same way) | `agenthub --help` works |
| 3. Install catalog | `agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub` | JSON with `"count" > 0` |
| 4. List skills | `$env:AGENTHUB_CATALOG_PATH = "$HOME\.agenthub"; agenthub list skills` | JSON array of skill metadata |
| 5. Generate MCP config | `agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json` | `Wrote .cursor\mcp.json`; `command` is `agenthub-mcp` |
| 6. IDE | Restart Cursor | `list_skills` visible in MCP panel |

**Maintainer optional:** clone + `pip install -e` + `--source .` still supported.

**Pass criteria:** steps 1–5 succeed without a local clone of the private monorepo.

---

## 9. GitHub deployment & CI

### 9.1 Release workflow (high level)

1. **Tag** a release (`v0.1.0`) on `main`.
2. **CI** (`.github/workflows/ci.yml`) runs Python unit tests and npm build/test on every push/PR.
3. **Publish Python** — on tag, build wheels from `packages/python/agenthub` and `packages/python/agenthub-mcp`; upload to PyPI (or internal index).
4. **Publish npm** — on tag, `npm publish` from `packages/npm/mcp` (requires `NPM_TOKEN` secret).
5. **Distribute catalog** via git checkout or future catalog tarball.

### 9.2 Suggested GitHub Actions secrets

| Secret | Used for |
|--------|----------|
| `PYPI_API_TOKEN` | Python package publish |
| `NPM_TOKEN` | npm package publish |

### 9.3 Local CI parity

```powershell
```powershell
$env:AGENTHUB_CATALOG_PATH = "packages\python\agenthub\tests\fixtures\sample-catalog"
python -m unittest discover -s packages/python/agenthub/tests -p "test_*.py"
python -m unittest discover -s packages/python/agenthub-mcp/tests -p "test_*.py"
cd packages/npm/mcp && npm install && npm run build && npm test
```

### 9.4 Testing with fellow developers from GitHub

**Option A — no clone (recommended for end users):**

```powershell
$env:GITHUB_TOKEN = "ghp_..."
pip install "agenthub @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
pip install "agenthub-mcp @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"
agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub
agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json
```

**Option B — maintainer editable install:**

```bash
git clone https://github.com/BeeNeural-com/agenthub.git
cd agenthub
pip install -e packages/python/agenthub -e packages/python/agenthub-mcp
agenthub install --full --target ~/.agenthub --source .
export AGENTHUB_CATALOG_PATH=~/.agenthub
agenthub connect --catalog ~/.agenthub --output ~/.cursor/mcp.json
```

**Option C — after PyPI publish:**

```bash
pip install agenthub agenthub-mcp
agenthub install --full --target ~/.agenthub --source https://github.com/BeeNeural-com/agenthub
```

Host the **public** Pages site from a separate public repo (or public Pages on docs only). Keep this monorepo **private**.

---

## 10. MCP fetch cache

MCP `get_*` / `get_*_file` tools and SDK `Catalog.get*` / `read_file` cache fetched bodies and supporting files on disk. `list_*` tools stay metadata-only and do not populate the cache.

| Variable | Default | Purpose |
|----------|---------|---------|
| `AGENTHUB_CACHE_PATH` | `<catalog>/.agenthub-cache/` | Directory for cached files and `agenthub-cache-lock.json` |

**Behavior:**

1. On `get_*`, the server checks the lock file and on-disk entry.
2. If the cached version matches the catalog manifest, the cached body/file is returned.
3. On miss or version change, content is read from the catalog, written to cache, and the lock file is updated.

**CLI (Python SDK):**

```powershell
agenthub cache status --catalog .\.agenthub
agenthub cache clear --catalog .\.agenthub
```

The cache directory is gitignored (`.agenthub-cache/`). Safe to delete at any time; entries rebuild on next fetch.

---

## 11. Environment reference

| Variable | Used by | Purpose |
|----------|---------|---------|
| `AGENTHUB_CATALOG_PATH` | SDK, MCP | Installed catalog directory (`~/.agenthub`) |
| `AGENTHUB_CATALOG_SOURCE` / `AGENTHUB_CATALOG_URL` | `agenthub install` | Remote source when `--source` omitted (`github:BeeNeural-com/agenthub` or HTTPS URL) |
| `GITHUB_TOKEN` / `AGENTHUB_GITHUB_TOKEN` | `agenthub install` remote fetch | Auth for private GitHub zipball |
| `AGENTHUB_BUNDLE` | MCP | Comma-separated bundle filter (else lockfile). **Full company preset:** `document-processing,product-management,devops-sre,software-engineering-general,web-development,ai-operations,data-analytics,security,marketing,sales,customer-success,finance,human-resources,operations,program-management,legal-compliance,strategy-executive,communications,procurement-supply-chain,r-and-d,sw-engineering-ai-augmented` |
| `AGENTHUB_CACHE_PATH` | SDK, MCP | Fetch cache directory (default: `<catalog>/.agenthub-cache/`) |
| `AGENTHUB_TOOL_DESC_MODE` | MCP | `active` (default) or `passive` tool descriptions |

---

## 12. Related documentation

| Document | Purpose |
|----------|---------|
| [examples/download-and-connect.md](../examples/download-and-connect.md) | Short quickstart walkthrough |
| [agenthub-universal-mcp-sdk.md](./research/agenthub-universal-mcp-sdk.md) | Architecture research & API design |
| [agenthub-product-requirements.md](./research/agenthub-product-requirements.md) | Formal requirements traceability |
| [packages/python/agenthub/README.md](../packages/python/agenthub/README.md) | Python SDK CLI reference |
| [packages/python/agenthub-mcp/README.md](../packages/python/agenthub-mcp/README.md) | Python MCP server reference |
| [packages/npm/mcp/README.md](../packages/npm/mcp/README.md) | npm MCP server reference |
