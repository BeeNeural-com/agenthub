#!/usr/bin/env python3
"""Minimal stdio MCP smoke test — verify agenthub-mcp lists tools.

Usage:
  export AGENTHUB_CATALOG_PATH=./.agenthub
  python examples/test-mcp-stdio.py

Requires: pip install agenthub-mcp  (brings in mcp SDK)
"""
from __future__ import annotations

import asyncio
import os
import shutil
import sys
from pathlib import Path


def _resolve_mcp_command() -> tuple[str, list[str]]:
    """Prefer AGENTHUB_MCP_COMMAND, then PATH, then same-dir as this Python."""
    override = os.environ.get("AGENTHUB_MCP_COMMAND", "").strip()
    if override:
        return override, ["--stdio"]

    on_path = shutil.which("agenthub-mcp")
    if on_path:
        return on_path, ["--stdio"]

    scripts = Path(sys.executable).resolve().parent
    for name in ("agenthub-mcp.exe", "agenthub-mcp"):
        candidate = scripts / name
        if candidate.is_file():
            return str(candidate), ["--stdio"]

    # Module fallback (works after pip install -e)
    return sys.executable, ["-m", "agenthub_mcp.cli", "--stdio"]


async def main() -> int:
    if not os.environ.get("AGENTHUB_CATALOG_PATH", "").strip():
        print("Set AGENTHUB_CATALOG_PATH to your installed catalog (e.g. ./.agenthub).", file=sys.stderr)
        return 1

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    command, args = _resolve_mcp_command()
    print(f"Using: {command} {' '.join(args)}", file=sys.stderr)
    params = StdioServerParameters(
        command=command,
        args=args,
        env=os.environ.copy(),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            names = sorted(tool.name for tool in result.tools)
            print(f"OK: {len(names)} tools")
            for name in names:
                print(f"  - {name}")
            if "list_skills" not in names:
                print("FAIL: list_skills not in tool list", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
