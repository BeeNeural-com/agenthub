# Trade Study: Agent Hub Download & Connection Models

**Date:** 2026-08-20  
**Decision:** Hybrid model — granular install + dual connect (MCP + SDK)

---

## Alternatives

| ID | Model |
|----|-------|
| A | Git clone only (status quo) |
| B | Full catalog pip wheel only |
| C | **Granular install (full / bundle / single) + MCP + SDK** |
| D | HTTP hosted MCP only (no local install) |
| E | SDK-only (no MCP server) |

---

## Criteria and weights

| Criterion | Weight |
|-----------|--------|
| Coding agent compatibility | 20% |
| Application/RAG embed | 20% |
| Download granularity | 15% |
| Time to market | 15% |
| Ops complexity | 10% |
| Offline/airgap | 10% |
| Token efficiency | 10% |

---

## Scores (1–5)

| Criterion | A | B | **C** | D | E |
|-----------|---|---|-------|---|---|
| Coding agent compatibility | 3 | 4 | **5** | 5 | 2 |
| Application/RAG embed | 2 | 3 | **5** | 3 | 5 |
| Download granularity | 1 | 2 | **5** | 3 | 3 |
| Time to market | 5 | 4 | **4** | 2 | 4 |
| Ops complexity | 5 | 4 | **3** | 2 | 5 |
| Offline/airgap | 2 | 4 | **5** | 1 | 4 |
| Token efficiency | 3 | 4 | **5** | 4 | 4 |
| **Weighted total** | 2.9 | 3.5 | **4.4** | 2.9 | 3.8 |

---

## Sensitivity

If **application embed** weight increases to 30%, C still wins (4.5 vs E 4.1) because C includes SDK without sacrificing MCP.

If **ops complexity** dominates, E wins — but fails coding agent requirement.

---

## Recommendation

**Selected: C — Granular install + dual connect**

Users choose install scope:

```bash
agenthub install --full              # everything
agenthub install --bundle r-and-d    # department bundle
agenthub install --skill feasibility-study   # one skill
```

Users choose connect mode:

| Mode | Command / API |
|------|----------------|
| **Coding agent** | `agenthub connect` → MCP stdio |
| **Application** | `from agenthub import Catalog` |
| **RAG** | `agenthub export-rag` or `catalog.as_rag_documents()` |
| **Remote agent** | `agenthub-mcp serve` → HTTP MCP Client |

---

## Conditions to revisit

- If catalog exceeds 100MB, split `agenthub-catalog` wheel from server package
- If MCP v2 stable, reassess FastMCP standalone migration
