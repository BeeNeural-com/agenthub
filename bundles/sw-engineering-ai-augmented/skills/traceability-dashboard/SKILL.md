---
name: traceability-dashboard
description: "Use when generating or reviewing human-readable KPI dashboards for ASPICE V-Model traceability and quality summarization. Provides KPI definitions, page sections, data-model guidance, and visual/reporting patterns for static HTML dashboards built from traceability artifacts and checker outputs."
---

# Traceability Dashboard Skill

This skill defines how to convert ASPICE V-Model traceability and quality evidence into a human-readable dashboard. It is intended for workflows that generate static HTML or similar report pages from normalized traceability data, checker results, and execution evidence.

---

## Overview

A traceability dashboard is a reporting surface, not an authoring artifact. It reads existing requirements, architecture, detailed design, verification, and audit evidence and presents a consolidated picture of chain health, KPI status, and prioritized follow-up actions.

The dashboard must serve two goals at the same time:
- Give engineers a fast path to broken links, missing evidence, and failing verification chains.
- Give reviewers a compact, defensible summary of coverage, traceability, and unresolved risk.

---

## Reference / API

### Core Entity Types

| Entity | Description |
|---|---|
| `req` | Software requirement node from SWE.1 |
| `arch-elem` | Static architecture element from SWE.2 |
| `arch-iface` | Interface contract from SWE.2 |
| `arch-seq` | Dynamic behavior sequence from SWE.2 |
| `elaboration` | SWE.3 design implementation link derived from `@elaborates` |
| `unit-verification` | SWE.4 unit-test coverage node derived from `@covers` or equivalent |
| `integration-verification` | SWE.5 verification node derived from `verifies:` / `@arch` |
| `qualification-verification` | SWE.6 verification node derived from `verifies:` / `@req` |
| `review-finding` | Optional audit finding from review or checker reports |
| `todo` | Derived remediation action |

### Required KPI Fields

Every KPI card should expose these fields:

| Field | Meaning |
|---|---|
| `id` | Stable machine-readable identifier |
| `label` | Human-readable card title |
| `value` | Current metric value |
| `unit` | `%`, `count`, or textual state |
| `status` | `good`, `warning`, or `critical` |
| `formula` | Short explanation of how the metric is computed |
| `evidence_count` | Number of underlying artifacts contributing to the metric |
| `details_href` | Optional deep-link target inside the report |

### Recommended KPI Set

| KPI | Formula |
|---|---|
| `req-allocation` | Requirements allocated to at least one `arch-elem` / total requirements |
| `design-elaboration` | `arch-elem` IDs elaborated in SWE.3 / total `arch-elem` IDs |
| `unit-coverage` | `arch-elem` IDs covered by unit verification / total `arch-elem` IDs |
| `integration-coverage` | `arch-seq` + `arch-iface` IDs verified by SWE.5 / total `arch-seq` + `arch-iface` IDs |
| `qualification-coverage` | `req` IDs verified by SWE.6 / total requirements |
| `chain-completeness` | Requirements with no downstream gaps / total requirements |

### Required Page Sections

| Section | Purpose |
|---|---|
| KPI hero | Fast status scan for the most important metrics |
| Heat-map | Level-by-level health summary |
| Chain status | Direct-link status across V-Model pairs |
| Broken chains | Requirement-centric view of multi-level gaps |
| Gap inventory | Concrete missing IDs grouped by category |
| Action queue | Prioritized TODO list |
| Artifact inventory | Counts and source locations for parsed evidence |

---

## Lifecycle & Usage Pattern

1. Collect source artifacts from SWE.1 to SWE.6.
2. Normalize IDs, links, and evidence into a single machine-readable snapshot.
3. Compute KPIs and derived gap categories from the snapshot.
4. Render a static HTML dashboard from the computed model.
5. Publish the snapshot and page together so the numbers remain explainable.

### Rendering Rules

- The page must remain useful when some inputs are missing.
- Missing evidence must be rendered as an explicit state, never silently treated as success.
- Every severity color must also include a text label.
- Tables must be sortable or grouped in a way that keeps CRITICAL items visible first.
- Executive summaries may be added later, but the engineering detail must not be hidden behind multiple navigation layers.

---

## Examples

### Example KPI definition

```json
{
  "id": "chain-completeness",
  "label": "End-to-End Chain Completeness",
  "value": 82.5,
  "unit": "%",
  "status": "warning",
  "formula": "requirements with architecture, design, unit, integration, and qualification evidence divided by all requirements",
  "evidence_count": 132,
  "details_href": "#broken-chains"
}
```

### Example broken-chain row

```json
{
  "req_id": "req:<component>-<topic>-<aspect>",
  "architecture": true,
  "design": true,
  "unit": false,
  "integration": false,
  "qualification": true,
  "gap_count": 2,
  "risk": "critical"
}
```

### Example action item

```json
{
  "severity": "critical",
  "owner": "<downstream-role>",
  "summary": "Add SWE.5 verification for arch:<component>-<sequence>",
  "evidence": ["arch:<component>-<sequence>", "req:<component>-<topic>-<aspect>"]
}
```

---

## Best Practices / Anti-patterns

| Do | Avoid |
|---|---|
| Keep the dashboard data-driven so KPIs can change without rewriting the layout | Hard-coding KPI card text into HTML templates with no underlying model |
| Show both summary and drill-down paths | Displaying only percentages with no missing-ID inventory |
| Compute chain completeness from explicit link evidence | Inferring end-to-end health from a single level only |
| Treat missing inputs as an explicit report state | Quietly omitting sections when an input file is absent |
| Preserve the exact artifact IDs in the data layer | Replacing IDs with prose and making drill-down impossible |

---

## Domain Glossary

| Term | Meaning |
|---|---|
| `chain completeness` | The extent to which a requirement or design item is linked through all expected downstream levels |
| `broken chain` | An item with multiple missing downstream links or blocked levels |
| `gap inventory` | The categorized list of specific missing IDs and evidence |
| `dashboard snapshot` | The normalized JSON-like model used to render the page |
| `evidence count` | The number of parsed artifacts or results contributing to a metric |
