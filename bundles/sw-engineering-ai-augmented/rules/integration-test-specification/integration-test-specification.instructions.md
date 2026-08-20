---
description: SWE.5-specific conventions for integration test specification Markdown documents. Extends test-specification.instructions.md with arch-ID traceability, Integration Strategy section, and IR01–IR08 review criteria.
applyTo: "**/doc/*/component_integration_tests/**/*.md"
---

# SWE.5 Integration Test Specification — Level-Specific Conventions

**Applies to**: `**/doc/*/component_integration_tests/**/*.md`

**Shared base**: `test-specification.instructions.md` — TCASE format, YAML structure, body requirements, file organisation, status lifecycle, spec text quality, coverage model, self-improvement trigger. Read the base file first; this file contains only SWE.5 delta rules.

**Template**: Before writing the first TCASE spec, read `.github/skills/integration-test-specification/templates/test-spec-swe5-integration.tpl.md`.

---

## 1. Integration Strategy Section (ASPICE BP1 RL.2)

Every integration test spec file must include an `## Integration Strategy` section that documents the integration verification strategy. This section is **required** — without it, ASPICE BP1 cannot be assessed at RL.2 or above.

```markdown
## Integration Strategy

- **Integration order**: <which elements are integrated first and why>
- **Verification environment**: <e.g., native Linux process pair; no hardware required; uses real IPC sockets>
- **Entry criteria**:
  - All SWE.2 `arch:` blocks for this component accepted
  - All SWE.3 `.h` files carry `@elaborates` annotations
  - Unit tests (SWE.4) pass for all elements under test
- **Exit criteria**:
  - Every integration-scope `arch:` ID (with `classification: sequence`, `statemachine`, or `activity`) is covered by a TCASE spec (or listed in an explicit Exclusions section in the Integration Strategy with the ID, rationale, and author approval). Integration-scope means the behavior is observable across element boundaries or is explicitly allocated to integration verification in the architecture briefing.
  - All GTests pass
  - All review records for `arch:` blocks with no automatable GTest path are filed
```

**Placement rule**: The Integration Strategy section must appear once, between `## Metadata` and the first `## TCASE_NN` section.

**Scope**: One strategy section per spec file. Multi-component specs use combined content naming all components.

**File structure**: `# Test Specification: <name>` → `## Metadata` → `## Integration Strategy` → `## TCASE_01` → ...

---

## 2. YAML Field Specialisation

Extends the shared YAML structure from `test-specification.instructions.md` § 2.

```yaml
id: itest-{component}-{topic}-{aspect}
type: {test_type}
level: {test_level}
status: Draft
priority: {priority}
fully_automated: true
verifies: arch:{id}   # Use the full arch: ID from SWE.2 (classification: sequence, statemachine, or activity)
```

| Field | Allowed Values | Notes |
|---|---|---|
| `id` | `itest-<component>-<topic>-<aspect>` | Integration test prefix |
| `level` | `Integration Test`, `Interface Test`, `Scenario Test` | |
| `verifies` | Exact `arch:` ID from SWE.2 | e.g., `arch:libipc-seq-connection-lifecycle` or `arch:libipc-server-lifecycle`; the `arch:` prefix is part of the value. Comma-separated list accepted when one TCASE covers multiple IDs: `arch:libipc-server-lifecycle, arch:libipc-seq-connection-lifecycle` |

## 3. One TCASE per arch: ID

Apply rules in order:

1. **Default:** write one TCASE per `arch:` ID. When one GTest implements multiple TCASEs, add one `@arch` annotation per referenced `arch:` ID in the GTest Doxygen block.

2. **Co-annotation rule:** when an existing TCASE covering a lifecycle sequence already fully exercises the states, transitions, and observable outcomes of a corresponding `statemachine` arch: ID, add the statemachine ID to that TCASE's `verifies:` field (comma-separated) and add a second `@arch` annotation to the GTest body. Do not write a separate TCASE in this case.

3. **Narrow exception:** a single TCASE may use comma-separated `verifies:` for any additional `arch:` ID that would require a pure-duplicate TCASE with identical test steps. Justify with a brief comment in the Description.

Never use the comma-separated exception to collapse unrelated `arch:` IDs with distinct test steps.

## 4. Description — Cross-Element Justification

In addition to the shared body requirements, integration test Descriptions must state which components interact and what data flows across each boundary. When the arch-ID under test is single-element-dominant or an in-process API boundary, include one sentence stating the cross-element behavior that justifies dynamic integration testing beyond unit coverage.

The prose must be precise enough for a developer to implement the GTest without reading SWE.2.

## 5. File Organisation — Integration Suffix

One spec file per `_briefing.md` group heading:

```
<heading_snake_case>_integration_tests.md
```

Example: `Initialization Sequences` → `initialization_integration_tests.md`

## 6. Spec-Side Prohibited Patterns

| Pattern | Why Prohibited |
|---|---|
| TCASE section without `verifies:` field | Breaks SWE.2↔SWE.5 direct traceability |
| `verifies:` pointing to a non-existent `arch:` ID | Creates orphaned spec |
| TCASE without `id:` field | Breaks stable traceability |
| TCASE without Description and Test Procedure | Insufficient for implementation |
| Multiple `arch:` IDs in a single TCASE section without the §3 co-annotation or exception justification | Breaks one-to-one traceability |
| Mocking the integration boundary itself | Defeats the purpose of integration testing |
| Modifying SWE.2 `.md` files from within a SWE.5 agent | Out of scope; use SWE.2 agents |

## 7. Review Criteria (T-Review Checklist)

Use these numbered criteria for spec review (Phase 1 T4) and T-Review (Phase 2 T3). Cite by ID.

**IR01** — An Integration Strategy section exists documenting: integration order, entry/exit criteria, and verification environment
**IR02** — Each TCASE has `verifies:` referencing a real SWE.2 `arch:` ID (with `classification: sequence`, `statemachine`, or `activity`; see §3 for co-annotation and exception rules)
**IR03** — Each TCASE covers a cross-element interaction; single-element behavior belongs in SWE.4
**IR04** — Description describes a complete cross-element flow: precondition → action → observable outcome
**IR05** — Each `TEST_F` in `tests/integration/` has `@arch` annotation referencing a real SWE.2 `arch:` ID
**IR06** — `TEST_F` body uses only the public API (no access to private implementation details)
**IR07** — Fixture `SetUp`/`TearDown` covers all inter-element resource setup and teardown; no stale resource leaks
**IR08** — TCASE `type:` is one of the ISO 25010 quality characteristics: `Functional Suitability`, `Performance Efficiency`, `Reliability`, `Security`, `Compatibility`, `Fault Injection`, `Stress Testing`, `Resource Usage`, or `Back-to-Back Testing`
