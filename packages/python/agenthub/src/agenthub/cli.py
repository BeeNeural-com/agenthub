"""Agent Hub CLI — install, search, connect."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from agenthub.catalog import Catalog
from agenthub.connect import mcp_config_stdio, write_mcp_config
from agenthub._cache import ResourceCache
from agenthub._loader import discover_catalog_root
from agenthub.install import install


def main() -> None:
    parser = argparse.ArgumentParser(prog="agenthub", description="Agent Hub catalog CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # install
    p_install = sub.add_parser("install", help="Download catalog resources locally")
    p_install.add_argument("--target", default=".agenthub", help="Install directory")
    p_install.add_argument("--full", action="store_true", help="Install entire catalog")
    p_install.add_argument("--bundle", help="Install one bundle (+ global)")
    p_install.add_argument("--skill", help="Install single skill")
    p_install.add_argument("--agent", help="Install single agent")
    p_install.add_argument("--rule", help="Install single rule")
    p_install.add_argument("--prompt", help="Install single prompt")
    p_install.add_argument(
        "--source",
        help=(
            "Catalog source: local path, GitHub URL, or github:owner/repo[@ref]. "
            "Default private repo: https://github.com/BeeNeural-com/agenthub "
            "(set GITHUB_TOKEN / AGENTHUB_GITHUB_TOKEN for private fetch)"
        ),
    )

    # search
    p_search = sub.add_parser("search", help="Search catalog")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--type", choices=["skill", "agent", "rule", "prompt"])
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--bundles", help="Comma-separated bundle list")

    # list
    p_list = sub.add_parser("list", help="List resources")
    p_list.add_argument("kind", choices=["skills", "agents", "rules", "prompts", "bundles"])
    p_list.add_argument("--bundles", help="Comma-separated bundle list")

    # get
    p_get = sub.add_parser("get", help="Fetch one resource body")
    p_get.add_argument("resource_id")
    p_get.add_argument("--type", choices=["skill", "agent", "rule", "prompt"], default="skill")

    # connect
    p_connect = sub.add_parser("connect", help="Write MCP config for coding agents")
    p_connect.add_argument("--output", default=".cursor/mcp.json")
    p_connect.add_argument("--catalog", help="Catalog path")
    p_connect.add_argument("--bundles", help="Comma-separated bundles")
    p_connect.add_argument("--script", help="Path to server.py (dev mode)")
    p_connect.add_argument(
        "--runtime",
        choices=["python", "npm"],
        default="python",
        help="MCP server runtime: pip agenthub-mcp (default) or npm @agenthub/mcp",
    )

    # export-rag
    p_rag = sub.add_parser("export-rag", help="Export RAG JSONL documents")
    p_rag.add_argument("--output", default="agenthub-rag.jsonl")
    p_rag.add_argument("--type", action="append", choices=["skill", "agent", "rule", "prompt"])
    p_rag.add_argument("--bundles", help="Comma-separated bundles")

    # cache
    p_cache = sub.add_parser("cache", help="Manage MCP fetch cache")
    cache_sub = p_cache.add_subparsers(dest="cache_cmd", required=True)
    cache_parent = argparse.ArgumentParser(add_help=False)
    cache_parent.add_argument("--catalog", help="Catalog path (for default cache location)")
    cache_sub.add_parser(
        "clear",
        parents=[cache_parent],
        help="Clear cached resource bodies and lock file",
    )
    cache_sub.add_parser(
        "status",
        parents=[cache_parent],
        help="Show cache lock file summary",
    )

    args = parser.parse_args()
    bundles = [b.strip() for b in args.bundles.split(",")] if getattr(args, "bundles", None) else None

    try:
        if args.cmd == "install":
            result = install(
                args.target,
                source_catalog=args.source,
                full=args.full,
                bundle=args.bundle,
                skill=args.skill,
                agent=args.agent,
                rule=args.rule,
                prompt=args.prompt,
            )
            print(
                json.dumps(
                    {
                        "target": str(result.target),
                        "count": len(result.installed),
                        "source": result.source,
                    },
                    indent=2,
                )
            )
        elif args.cmd == "search":
            cat = Catalog(bundles=bundles)
            hits = cat.search(args.query, resource_type=args.type, limit=args.limit)
            print(json.dumps([h.__dict__ for h in hits], indent=2))
        elif args.cmd == "list":
            cat = Catalog(bundles=bundles)
            if args.kind == "skills":
                items = cat.list_skills()
            elif args.kind == "agents":
                items = cat.list_agents()
            elif args.kind == "rules":
                items = cat.list_rules()
            elif args.kind == "prompts":
                items = cat.list_prompts()
            else:
                items = cat.list_bundles()
                print(json.dumps([b.__dict__ for b in items], indent=2))
                return
            print(json.dumps([i.__dict__ for i in items], indent=2))
        elif args.cmd == "get":
            cat = Catalog(bundles=bundles)
            res = cat.get(args.resource_id, args.type)
            if not res:
                print(f"Not found: {args.resource_id}", file=sys.stderr)
                sys.exit(1)
            print(res.body)
        elif args.cmd == "connect":
            catalog = args.catalog or os.environ.get("AGENTHUB_CATALOG_PATH") or "~/.agenthub"
            cfg = mcp_config_stdio(
                catalog_path=catalog,
                bundles=bundles,
                server_script=args.script,
                runtime=args.runtime,
            )
            path = write_mcp_config(args.output, cfg)
            print(f"Wrote {path}")
        elif args.cmd == "export-rag":
            cat = Catalog(bundles=bundles)
            types = tuple(args.type) if args.type else ("skill", "agent", "rule", "prompt")
            docs = cat.as_rag_documents(resource_types=types)
            out = Path(args.output)
            with out.open("w", encoding="utf-8") as f:
                for doc in docs:
                    f.write(json.dumps({"id": doc.id, "text": doc.text, "metadata": doc.metadata}) + "\n")
            print(f"Exported {len(docs)} documents to {out}")
        elif args.cmd == "cache":
            root: Path | None = None
            if args.catalog:
                root = discover_catalog_root(Path(args.catalog))
            elif not os.environ.get("AGENTHUB_CACHE_PATH", "").strip():
                try:
                    root = discover_catalog_root()
                except FileNotFoundError:
                    root = None
            cache = ResourceCache(root)
            if args.cache_cmd == "clear":
                cache.clear()
                print(f"Cleared cache at {cache.cache_path}")
            else:
                print(json.dumps(cache.status(), indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
