# Agent Hub — npm packages

| Package | Path | Install (dev) | Purpose |
|---------|------|---------------|---------|
| `@agenthub/mcp` | `mcp/` | `cd mcp && npm install && npm run build` | MCP server CLI (`agenthub-mcp --stdio`) |
| `@agenthub/sdk` | `sdk/` | `cd sdk && npm install && npm run build` | TypeScript `Catalog` for apps/RAG |

Both packages read the same on-disk catalog as the Python SDK (`AGENTHUB_CATALOG_PATH` or `--catalog`).

See [examples/download-and-connect.md](../../examples/download-and-connect.md) for full workflow.
