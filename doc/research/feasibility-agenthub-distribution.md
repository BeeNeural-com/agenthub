# Feasibility Study: Agent Hub Universal Distribution

**Date:** 2026-08-20  
**Author:** Agent Hub R&D  
**Status:** approved  
**Recommendation:** **Proceed** with dual SDK + MCP CLI (Option C)

---

## Executive summary

Building Agent Hub as a downloadable product (full catalog, bundle, or single skill) connected to coding agents via MCP and to applications via Python SDK is **technically feasible** with existing `loader.py` and MCP POC. Estimated effort: **3 weeks** to MVP on PyPI. Economic and operational feasibility are strong for internal CARIAD deployment; external open-source distribution needs license review.

---

## Problem statement

- Engineers cannot `pip install agenthub` or download one skill for a RAG pipeline
- MCP server requires git clone + venv
- No lockfile or install path for applications

**If we do nothing:** Agent Hub stays a repo-only POC; R&D and SWE content unreachable outside git checkout.

---

## Technical feasibility

| Aspect | Assessment | Evidence |
|--------|------------|----------|
| Catalog loader | ✅ Feasible | `loader.py` loads 49 skills, 21 agents today |
| Single-skill install | ✅ Feasible | Folder-copy + lockfile implemented in SDK prototype |
| MCP stdio | ✅ Proven | `demo.py` L0 PASS |
| MCP HTTP | ⚠️ Partial | MCP Python SDK supports `mcp run --transport streamable-http` |
| npm distribution | ✅ Feasible | Standard `npx` + bin pattern per MCP docs |
| RAG export | ✅ Feasible | `as_rag_documents()` prototype |
| Windows | ⚠️ Risk | Smart App Control blocks pydantic; SDK-only mode mitigates |

---

## Economic feasibility

| Item | Estimate |
|------|----------|
| MVP (Python pip + MCP) | 2–3 dev-weeks |
| npm wrapper + docs | 3–5 days |
| TypeScript SDK | 1–2 weeks (should) |
| Hosted HTTP MCP | 2–4 weeks ops + dev (could) |
| Ongoing maintenance | 0.25 FTE catalog + releases |

**Opportunity cost:** Reuses agenthub-reg catalog pipeline; avoids rebuilding content in each IDE.

---

## Operational feasibility

- Team has Python MCP expertise from `packages/python/agenthub-mcp` (formerly `mcp-poc`)
- Content authors already use `global/` + `bundles/` structure
- CI can bundle catalog into wheel on release

---

## Recommendation

**Proceed** — ship Python `agenthub` + `agenthub-mcp` first; npm wrapper second; HTTP third.

**Conditions:**
1. Fix Windows path normalization in MCP file fetch ✅
2. Document SDK-only path for RAG (no MCP subprocess)
3. Pin `mcp<2` until migration guide exists

**Next step:** Publish internal alpha wheel; dogfood with `agenthub install --bundle r-and-d`
