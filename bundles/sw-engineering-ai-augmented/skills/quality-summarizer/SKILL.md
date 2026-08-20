---
name: quality-summarizer
description: "V-Model quality aggregation logic: V-Model Checker Map, cross-level ID registry construction, broken-chain reconstruction rules, heat-map computation formula, and the complete 5-section consolidated quality report template. Use when synthesising outputs from all six Coverage Checkers and six Traceability Checkers into a single quality picture."
---

# SWP V-Model Quality Summarizer Skill

This skill is component-agnostic and reusable across projects. It defines the aggregation logic, synthesis steps, heat-map formula, and report template for producing a consolidated V-Model quality summary from all 12 per-level checker reports.

---

## V-Model Checker Map

| Level | Coverage Checker | Traceability Checker | Review Agent (optional) |
|---|---|---|---|
| **SWE.1** | `SWE.1 Coverage Checker` | `SWE.1 Traceability Checker` | `SWE.1 Review` |
| **SWE.2** | `SWE.2 Coverage Checker` | `SWE.2 Traceability Checker` | `SWE.2 Review` |
| **SWE.3** | `SWE.3 Coverage Checker` | `SWE.3 Traceability Checker` | `SWE.3 Review` |
| **SWE.4** | `SWE.4 Coverage Checker` | `SWE.4 Traceability Checker` | `SWE.4 Review` |
| **SWE.5** | `SWE.5 Coverage Checker` | `SWE.5 Traceability Checker` | `SWE.5 Review` |
| **SWE.6** | `SWE.6 Coverage Checker` | `SWE.6 Traceability Checker` | `SWE.6 Review` |

**Mandatory input**: 12 checker reports (6 Coverage + 6 Traceability). **Optional input**: up to 6 Review reports.

If fewer than 12 checker reports are available, stop and report which are missing. Do not produce a final heat-map until all 12 are present.

---

## Direct-Connection Scope Per Traceability Checker

| Checker | Left connection | Right connection |
|---|---|---|
| **SWE.1 Traceability** | Upstream → SWE.1 (`:covers:`) | SWE.1 → SWE.2 (`:covers:` allocation) |
| **SWE.2 Traceability** | SWE.1 ↔ SWE.2 bidirectional | SWE.2 → SWE.5 structural readiness |
| **SWE.3 Traceability** | SWE.2 ↔ SWE.3 (`@elaborates`) | SWE.3 → SWE.1 (`@req`) + SWE.4 readiness |
| **SWE.4 Traceability** | SWE.3 ↔ SWE.4 (`@covers`) | — |
| **SWE.5 Traceability** | SWE.2 ↔ SWE.5 (`verifies: arch:`) | — |
| **SWE.6 Traceability** | SWE.1 ↔ SWE.6 (`verifies: req:`/`@req`) | — |

---

## Critical Rules

- **Never modify source, architecture, or test files.**
- **Never re-run the per-level checks yourself.** Only synthesise what the checker reports contain.
- **An ID failing at multiple levels has compounded risk.** Escalate to the top of the to-do list.
- **Propagate severity upward.** A CRITICAL at SWE.1 blocks all downstream levels — mark them as BLOCKED in the heat-map.

---

## Synthesis Logic

### Step 1 — Collect reports

For each of the 12 checker reports, extract:
- Summary table (counts per status)
- CRITICAL findings (list of IDs)
- WARNING findings (list of IDs)
- TODO items (list)

### Step 2 — Build the cross-level ID registry

Collect all IDs mentioned across all reports:
- `req:` IDs — appear in SWE.1, SWE.2, SWE.5, SWE.6
- `arch:` IDs — appear in SWE.2, SWE.5
- TCASE IDs (`itest-*` / `qtest-*`) — appear in SWE.5, SWE.6 spec files

For each `req:` ID, build a cross-level status vector:

| req: ID | SWE.1 (complete?) | SWE.2 (allocated?) | SWE.3 (designed+built?) | SWE.4 (unit tested?) | SWE.5 (traced?) | SWE.6 (tested?) |
|---|---|---|---|---|---|---|
| req:foo-001 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |

### Step 3 — Reconstruct multi-level chains

Individual traceability checkers verify only their direct connections. The Summarizer is the only agent that reconstructs end-to-end chains.

A broken chain is any `req:` ID that has a gap at **two or more** V-Model levels simultaneously:

```
BROKEN_CHAINS = {req: id where gap_count(id) >= 2}
```

Also identify:
- **Level-blocked IDs**: A CRITICAL at SWE.1 (e.g., missing `:verification_method:`) blocks SWE.6 — mark as BLOCKED even if SWE.6 shows no gap independently.
- **Orphan propagation**: An orphaned `@req` in SWE.5 or SWE.6 that references a non-existent `req:` ID is a broken chain at the annotation level.

**Key chain paths to reconstruct:**

| Chain | Links | Checkers that supply evidence |
|---|---|---|
| Left-side design chain | `req:` → `arch:` → `@elaborates` → `@covers` | SWE.1T + SWE.2T + SWE.3T + SWE.4T |
| Right-side integration chain | `arch:` → `verifies:` in TCASE (no SWE.1 link) | SWE.2T + SWE.5T |
| Right-side qualification chain | `req:` → `verifies: req:` / `@req` in TCASE | SWE.1T + SWE.6T |

### Step 4 — Compute the heat-map

```
For each level L in {SWE.1, SWE.2, SWE.3, SWE.4, SWE.5, SWE.6}:
  heat[L] = {
    CRITICAL: count of CRITICAL findings at level L,
    WARNING:  count of WARNING findings at level L,
    INFO:     count of INFO findings at level L,
    Coverage%: from Coverage Checker summary
  }
```

Assign a heat colour per level:
- 🔴 RED: any CRITICAL finding
- 🟡 AMBER: no CRITICAL but ≥1 WARNING
- 🟢 GREEN: no CRITICAL, no WARNING

### Step 5 — Produce the unified summary report

See report template below.

---

## Consolidated Quality Report Template

```markdown
## SWP V-Model Quality Summary — <Component> — <date>
**Reports ingested**: SWE.1 Coverage, SWE.1 Traceability, SWE.2 Coverage, SWE.2 Traceability, SWE.3 Coverage, SWE.3 Traceability, SWE.4 Coverage, SWE.4 Traceability, SWE.5 Coverage, SWE.5 Traceability, SWE.6 Coverage, SWE.6 Traceability

---

### V-Model Coverage Heat-Map

| Level | Heat | Coverage % | CRITICAL | WARNING | INFO |
|---|---|---|---|---|---|
| SWE.1 Requirements | 🔴 | N% | N | N | N |
| SWE.2 Architecture | 🟡 | N% | 0 | N | N |
| SWE.3 Detailed Design | ⚫ | N% | N | N | N |
| SWE.4 Unit Verification | ⚫ | N% | N | N | N |
| SWE.5 Integration Testing | 🔴 | N% | N | N | N |
| SWE.6 Qualification Testing | 🟡 | N% | 0 | N | N |

**Overall V-Model health**: 🔴 CRITICAL — <N> critical gaps across <levels> levels

---

### V-Model Traceability Chain Status

| Level pair | Chain direction | Status | Gap count |
|---|---|---|---|
| SWE.1 → SWE.2 | req: → arch: allocation | 🔴 N unallocated | N |
| SWE.2 → SWE.3 | arch: → @elaborates header | ⚫ N unelaborated | N |
| SWE.3 → SWE.4 | @elaborates → @covers unit test | ⚫ N untested | N |
| SWE.2 → SWE.5 | arch: → TCASE `verifies:` | 🟡 N uncovered | N |
| SWE.1 → SWE.6 | req: → TCASE `verifies: req:` | 🔴 N uncovered | N |

---

### Broken-Chain Report (IDs failing at ≥2 levels)

| req: ID | SWE.1 | SWE.2 | SWE.3 | SWE.4 | SWE.5 | SWE.6 | Chain health | Risk |
|---|---|---|---|---|---|---|---|---|
| req:foo-001 | ✅ complete | ✅ allocated | ✅ designed | ⚠️ stub only | ⚠️ no TCASE | ❌ no test | 2 gaps | 🔴 HIGH |
| req:foo-002 | ⚠️ no method | ✅ allocated | ✅ designed | ✅ tested | ⚫ BLOCKED | ⚫ BLOCKED | 1 root gap (+ 2 blocked) | 🔴 HIGH |
| req:foo-003 | ✅ complete | ❌ unallocated | ⚫ BLOCKED | ⚫ BLOCKED | ⚫ BLOCKED | ❌ no test | 4 gaps | 🔴 CRITICAL |

---

### Unified Prioritised To-Do List

**Sorted by**: severity (CRITICAL first) → level (SWE.1 → SWE.6) → broken-chain impact.

#### 🔴 CRITICAL — Blocking issues: resolve first

- [ ] `TODO(SWE.1)` Set `:verification_method:` for `req:foo-002` — blocks SWE.6 entirely
- [ ] `TODO(SWE.2)` Allocate `req:foo-003` to an `arch:` — unallocated, blocks SWE.5 and SWE.6
- [ ] `TODO(SWE.6)` Fix test failure in `FooTest.BarBaz` covering `req:foo-001`
- [ ] `TODO(SWE.5)` Fix FIXTURE_FAILURE in `IntegrationTest.TransportHandle`

#### 🟡 MEDIUM — Significant gaps: resolve before release baseline

- [ ] `TODO(SWE.2)` Add `:actors:` to `arch:<component>-handle-transmission`
- [ ] `TODO(SWE.5)` Write TCASE for `arch:<component>-disconnect` — not yet covered
- [ ] `TODO(SWE.6)` Implement stub `FooTest.CleanupTest` covering `req:foo-004`

#### 🟢 LOW — Quality improvements: address in next iteration

- [ ] `TODO(SWE.1)` Accept <N> draft requirements after SWE.1 Review
- [ ] `TODO(SWE.4)` Implement <N> UNIMPLEMENTED unit test stubs
- [ ] `TODO(SWE.6)` Ensure static review records exist for `static_test` requirements

#### 🔵 PROCESS — ASPICE BP compliance findings (only if Review reports provided)

- [ ] `TODO(SWE.1)` RC04: `req:foo-007` `:verification_criteria:` restates description — rewrite
- [ ] `TODO(SWE.3)` DR01: `ClassName.h` `@details` is a copy of SWE.2 black-box text — replace with white-box design description

---
