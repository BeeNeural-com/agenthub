"""Generate MCP connection configs for coding agents."""
from __future__ import annotations

import json
import os
from pathlib import Path

from agenthub._cache import CACHE_PATH_ENV
from agenthub._loader import read_lockfile_bundles


def _resolve_bundles(catalog_path: str | Path | None, bundles: list[str] | None) -> list[str] | None:
    if bundles:
        return bundles
    if catalog_path:
        locked = read_lockfile_bundles(Path(catalog_path).expanduser())
        if locked:
            return locked
    return None


def mcp_config_stdio(
    *,
    catalog_path: str | Path | None = None,
    bundles: list[str] | None = None,
    command: str | None = None,
    server_script: str | Path | None = None,
    runtime: str = "python",
) -> dict:
    """Return mcp.json fragment for stdio MCP (Cursor, Claude Code, Copilot)."""
    env: dict[str, str] = {}
    if catalog_path:
        env["AGENTHUB_CATALOG_PATH"] = str(Path(catalog_path).expanduser().resolve())
    resolved = _resolve_bundles(catalog_path, bundles)
    if resolved:
        env["AGENTHUB_BUNDLE"] = ",".join(resolved)
    cache_path = os.environ.get(CACHE_PATH_ENV)
    if cache_path and cache_path.strip():
        env[CACHE_PATH_ENV] = cache_path.strip()

    if command:
        cmd = command
        args: list[str] = ["--stdio"]
    elif server_script:
        script = Path(server_script).resolve()
        cmd = "python"
        args = [str(script)]
    elif runtime == "npm":
        cmd = "npx"
        args = ["@agenthub/mcp", "--stdio"]
    else:
        cmd = "agenthub-mcp"
        args = ["--stdio"]

    entry: dict = {"type": "stdio", "command": cmd, "args": args}
    if env:
        entry["env"] = env
    return {"mcpServers": {"agenthub": entry}}


def mcp_config_http(
    url: str,
    *,
    token_env: str = "AGENTHUB_TOKEN",
) -> dict:
    """Return mcp.json fragment for remote HTTP MCP."""
    return {
        "mcpServers": {
            "agenthub": {
                "url": url,
                "headers": {"Authorization": f"Bearer ${{env:{token_env}}}"},
            }
        }
    }


def write_mcp_config(path: str | Path, config: dict) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return target
