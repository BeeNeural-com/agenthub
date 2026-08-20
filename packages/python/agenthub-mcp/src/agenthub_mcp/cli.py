"""CLI for Agent Hub MCP server."""
from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="agenthub-mcp", description="Agent Hub MCP server")
    parser.add_argument("--stdio", action="store_true", help="Run stdio MCP transport (default)")
    parser.add_argument("--serve", action="store_true", help="Run HTTP MCP server (future)")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port when using --serve")
    args = parser.parse_args()

    if args.serve:
        print("HTTP transport (--serve) is planned for v0.2. Use --stdio for now.", file=sys.stderr)
        sys.exit(1)

    from agenthub_mcp.server import run_stdio

    run_stdio()


if __name__ == "__main__":
    main()
