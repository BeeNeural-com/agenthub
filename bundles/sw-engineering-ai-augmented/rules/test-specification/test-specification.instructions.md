---
description: Shared conventions for writing TCASE test specification Markdown documents across SWE.5 integration tests and SWE.6 qualification tests. Level-specific rules are in the dedicated integration-test-specification.instructions.md and qualification-test-specification.instructions.md files.
applyTo: "**/doc/*/component_integration_tests/**/*.md,**/doc/*/component_qualification_tests/**/*.md"
---

# Test Specification — Shared Authoring Conventions

**Applies to**: All TCASE test specification Markdown files in `doc/<component>/component_integration_tests/` and `doc/<component>/component_qualification_tests/`.

This file contains the rules that are **identical** across SWE.5 and SWE.6 test specifications. Level-specific rules (YAML field values, traceability targets, review criteria) are in the dedicated instruction files:
- `integration-test-specification.instructions.md` — SWE.5 delta (arch: IDs with classification subtypes, Integration Strategy, IR01–IR08)
- `qualification-test-specification.instructions.md` — SWE.6 delta (req: IDs, black-box proxies, QR01–QR08)

---

## 1. TCASE Identifier Convention

```
## TCASE_NN: <Short_Descriptive_Title>
```

- `NN` is a two-digit sequential number starting from `01`, unique within the file.
- `<Short_Descriptive_Title>` is a human-readable title describing the test scenario.
- Numbering is positional within the file. If stable traceability IDs are needed, use the `id:` field in the YAML block.

## 2. Mandatory YAML Fields (Shared Structure)

Every TCASE section must include a YAML metadata block. The shared field set is:

| Field | Required | Notes |
|---|---|---|
| `id` | Yes | Stable traceability ID; decouples traceability from positional TCASE numbering. Prefix and format are level-specific — see the dedicated instruction file. |
| `type` | Yes | ISO 25010 quality characteristics (`Functional Suitability`, `Performance Efficiency`, `Reliability`, `Security`, `Compatibility`) or ISO 26262 test techniques (`Fault Injection`, `Stress Testing`, `Resource Usage`, `Back-to-Back Testing`) |
| `level` | Yes | Level-specific — see the dedicated instruction file |
| `status` | Yes | `Draft`, `Review`, `Approved` |
| `priority` | Yes | `High`, `Medium`, `Low` |
| `fully_automated` | Yes | `true`, `false` |
| `verifies` | Yes | Exact traceability target ID. Type is level-specific — see the dedicated instruction file. |

## 3. One TCASE per Traceability ID

Never combine multiple traceability IDs into a single TCASE section. Write one TCASE per ID. Level-specific exceptions are documented in the dedicated instruction files.

### 3a. TCASE Splitting Criteria (within one ID)

When a single ID has multiple distinct test scenarios, split them into **separate TCASEs**:

| Criterion | Split into separate TCASEs | Keep in one TCASE |
|---|---|---|
| Success path vs. failure path | Always separate | — |
| Independent precondition violations | One TCASE per precondition group | — |
| Boundary/edge cases | Separate when Arrange differs materially | Group when only the input value varies |
| Same Arrange + same interaction, only assertion differs | — | One TCASE with multiple Assert steps |

**Rationale**: Atomic TCASEs isolate failures. If a bundled TCASE fails at Step 3, Steps 4–6 are opaque.

## 4. TCASE Body Requirements

The `dynamic_test`/`static_test`/`no_test` classification is a property of the **requirement** (SWE.1 `:verification_method:`), not the test case. Requirements with `:verification_method: static_test` do not produce a TCASE or GTest. Instead, they are tracked in `doc/<component>/component_qualification_tests/static_test_reviews.md` with columns: `req_id | review_method | pr_link | reviewer | date | status`. Requirements with `:verification_method: no_test` are skipped entirely.

> **SWE.6 note**: This coupling to SWE.1 `:verification_method:` applies to qualification tests (SWE.6), which derive their scope from `req:` IDs. For integration tests (SWE.5), TCASEs derive from SWE.2 `arch:` IDs with `classification: sequence`, `statemachine`, or `activity`; the SWE.1 `:verification_method:` attribute is not a gating criterion for SWE.5 scope.

Each TCASE section must include:

- **Description**: a complete test condition — what is being verified, under what trigger condition, and why it matters. Precise enough for a developer to implement the GTest without reading the upstream artifact.
- **Test Procedure**: a table with Step | Action | Expected columns. Each step is one observable action with one verifiable expected result.

Level-specific body rules (e.g., cross-element justification for integration, black-box proxy patterns for qualification) are in the dedicated instruction files.

## 5. File Organisation

Test spec files are derived from the `_briefing.md` group headings, one spec file per group:

| Source | Rule |
|---|---|
| `_briefing.md` `### <Heading>` | One spec file per heading. File name suffix is level-specific — see dedicated instruction file. |

Heading-to-filename conversion: lowercase, replace spaces with underscores, drop trailing qualifiers that duplicate the suffix.

**Mandatory**: Do not merge multiple briefing groups into one spec file. Do not split one briefing group across multiple files. The briefing group headings are the single source of truth for file decomposition.

If no `_briefing.md` exists, WARN the user and propose mirroring the upstream artifact topic structure as fallback. Wait for user confirmation before proceeding.

## 6. Status Lifecycle

```
Draft → Review → Approved
```

- `Draft`: TCASE has been written but not yet peer-reviewed.
- `Review`: TCASE is under active review.
- `Approved`: TCASE has been reviewed, confirmed against the upstream artifact, and approved for release.

## 7. Spec Text Quality

Description and Test Procedure prose describes **what** behavior is verified, not **how**. Use behavioral language readable by non-developers.

**Forbidden terms in condition text:**

| Category | Examples | Use instead |
|---|---|---|
| Syscall names | `sendmsg`, `poll`, `POLLHUP`, `close` | "a send failure", "a connection break" |
| Socket paths/types | `/tmp/test.sock`, `AF_UNIX` | "the IPC endpoint" |
| Timing values | `200ms` | "within the configured timeout" |
| Internal names | `mClientMap`, `poll reactor` | "the client registry" |
| C++ types | `unique_ptr`, `std::vector` | omit |

Technical details belong in GTest stub comments and test bodies, not in spec prose.

## 8. Coverage State Model

Used by agents during Triage to classify each traceability ID.

| State | Criteria |
|---|---|
| **Blocked** | Upstream artifact structurally incomplete or prerequisite tests not passing |
| **Uncovered** | ID in scope with no TCASE spec |
| **Partially Specified** | TCASE exists but GTest stub not written |
| **Fully Specified** | TCASE + GTest stub exist (with `FAIL()`) but body not implemented |
| **Partially Implemented** | Some GTest bodies implemented; others remain `FAIL()` |
| **Fully Implemented** | All bodies implemented; not yet built/run |
| **Verified** | All GTests built and passing |
| **Results Communicated** | Test results documented in test report and communicated to upstream roles (satisfies ASPICE BP7/BP5) |

## 9. Self-Improvement Trigger

If a new TCASE pattern, edge case, or component convention is discovered during agent operation:
1. Note it explicitly at the end of the agent response.
2. Propose updating this instructions file, the level-specific file, or a skill.
3. Apply only after user confirmation.
