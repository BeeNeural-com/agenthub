# Agent Hub — Download & Connect (no full clone)

> **Architecture:** public marketing/docs site (GitHub Pages) + **private** MCP/catalog repo [`BeeNeural-com/agenthub`](https://github.com/BeeNeural-com/agenthub).  
> End users never clone the private codebase.  
> **Full guide:** [doc/deployment-guide.md](../doc/deployment-guide.md)

## Flow

1. Visit the **public** Pages site → copy MCP setup / follow install steps  
2. `pip install` thin packages from **private** git (token or SSH)  
3. `agenthub install --source https://github.com/BeeNeural-com/agenthub` → catalog into `~/.agenthub`  
4. `agenthub connect` → Cursor uses `agenthub-mcp` on PATH + local catalog  
5. Restart Cursor

---

## PowerShell (Windows) — primary path

```powershell
# 1) Token with read access to private BeeNeural-com/agenthub
$env:GITHUB_TOKEN = "ghp_xxxxxxxx"   # or $env:AGENTHUB_GITHUB_TOKEN

# 2) Venv + packages from private git (subdirectory only — not a full clone)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "agenthub @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
pip install "agenthub-mcp @ git+https://x-access-token:$env:GITHUB_TOKEN@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"

# 3) Download catalog only (global/ + bundles/) into user home
agenthub install --full --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub

# Optional: one bundle instead of --full
# agenthub install --bundle web-development --target $HOME\.agenthub --source https://github.com/BeeNeural-com/agenthub

# 4) Write .cursor/mcp.json (agenthub-mcp on PATH + absolute catalog path)
agenthub connect --catalog $HOME\.agenthub --output .cursor\mcp.json

# 5) Restart Cursor — agenthub MCP should show 13 tools
```

**SSH alternative** (no token in pip URL; still set `GITHUB_TOKEN` for `agenthub install` zipball fetch):

```powershell
pip install "agenthub @ git+ssh://git@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub"
pip install "agenthub-mcp @ git+ssh://git@github.com/BeeNeural-com/agenthub.git@main#subdirectory=packages/python/agenthub-mcp"
```

---

## What gets downloaded

| Artifact | How | Where |
|----------|-----|--------|
| `agenthub` + `agenthub-mcp` | pip from git `#subdirectory=` | site-packages / PATH |
| Catalog (`global/` + `bundles/`) | GitHub zipball via `agenthub install --source` | `~/.agenthub` (or `.\.agenthub`) |
| Fetch cache | MCP/SDK `get_*` | `~/.agenthub/.agenthub-cache/` or `AGENTHUB_CACHE_PATH` |

Packages do **not** embed the catalog. MCP reads `AGENTHUB_CATALOG_PATH`.

---

## MCP config shape (after connect)

```json
{
  "mcpServers": {
    "agenthub": {
      "type": "stdio",
      "command": "agenthub-mcp",
      "args": ["--stdio"],
      "env": {
        "AGENTHUB_CATALOG_PATH": "C:\\Users\\YOU\\.agenthub"
      }
    }
  }
}
```

No clone paths. No venv-inside-repo binaries.

---

## Verify

```powershell
$env:AGENTHUB_CATALOG_PATH = "$HOME\.agenthub"
agenthub list skills
agenthub search "threat model"
```

---

## Maintainers (optional local checkout)

Developers who **do** clone the private repo can still use a local path:

```powershell
agenthub install --full --target .\.agenthub --source .
agenthub connect --catalog .\.agenthub --output .cursor\mcp.json
```

---

## Related

- Public site: [docs/index.html](../docs/index.html) → section **Connect without cloning**
- [Deployment guide](../doc/deployment-guide.md)
- Private repo: https://github.com/BeeNeural-com/agenthub
