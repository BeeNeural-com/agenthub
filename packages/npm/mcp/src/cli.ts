#!/usr/bin/env node
import { discoverCatalogRoot } from "./loader.js";
import { runStdioServer } from "./server.js";

function printError(message: string): void {
  console.error(`Error: ${message}`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  let catalogPath: string | undefined;
  let useStdio = false;
  let useServe = false;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--stdio") {
      useStdio = true;
      continue;
    }
    if (arg === "--serve") {
      useServe = true;
      continue;
    }
    if (arg === "--catalog") {
      catalogPath = args[i + 1];
      if (!catalogPath) {
        printError("--catalog requires a path argument.");
        process.exit(1);
      }
      i += 1;
      continue;
    }
    if (arg === "--help" || arg === "-h") {
      console.error(`agenthub-mcp — Agent Hub MCP server

Usage:
  agenthub-mcp --stdio [--catalog <path>]

Options:
  --stdio            Run stdio MCP transport (default when no other mode is given)
  --catalog <path>   Catalog directory (overrides AGENTHUB_CATALOG_PATH)
  --serve            HTTP MCP server (planned for v0.2)
  -h, --help         Show this help

Environment:
  AGENTHUB_CATALOG_PATH        Installed catalog directory (.agenthub/)
  AGENTHUB_BUNDLE              Comma-separated bundle ids
  AGENTHUB_TOOL_DESC_MODE      active (default) or passive
`);
      process.exit(0);
    }

    printError(`Unknown argument: ${arg}`);
    process.exit(1);
  }

  if (useServe) {
    console.error("HTTP transport (--serve) is planned for v0.2. Use --stdio for now.");
    process.exit(1);
  }

  if (!useStdio && args.length === 0) {
    useStdio = true;
  }

  if (!useStdio) {
    printError("No transport selected. Use --stdio.");
    process.exit(1);
  }

  let catalogRoot: string;
  try {
    catalogRoot = discoverCatalogRoot(catalogPath);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  }

  await runStdioServer(catalogRoot);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
