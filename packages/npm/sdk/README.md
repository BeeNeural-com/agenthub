# @agenthub-mcp/sdk

Programmatic catalog access for Agent Hub resources in Node/TypeScript.

## Install

```bash
npm install @agenthub-mcp/sdk
```

Local dev (from repo):

```powershell
cd packages/npm/mcp; npm install; npm run build
cd ../sdk; npm install; npm run build
```

## Usage

```typescript
import { Catalog } from "@agenthub-mcp/sdk";

const catalog = new Catalog("C:\\path\\to\\.agenthub");
const skill = catalog.getSkill("feasibility-study");
const agents = catalog.listAgents();
```

Set `AGENTHUB_CATALOG_PATH` or pass the catalog path to the constructor. Bundle selection follows the same rules as `@agenthub-mcp/mcp` (`AGENTHUB_BUNDLE` or `agenthub-lock.json`).
