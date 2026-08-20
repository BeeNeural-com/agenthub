---
description: SWE.6-specific conventions for qualification test specification Markdown documents. Extends test-specification.instructions.md with req-ID traceability, black-box proxy patterns, and QR01–QR08 review criteria.
applyTo: "**/doc/*/component_qualification_tests/**/*.md"
---

# SWE.6 Test Specification — Level-Specific Conventions

**Applies to**: `**/doc/*/component_qualification_tests/**/*.md`

**Shared base**: `test-specification.instructions.md` — TCASE format, YAML structure, body requirements, file organisation, status lifecycle, spec text quality, coverage model, self-improvement trigger. Read the base file first; this file contains only SWE.6 delta rules.

**Template**: Before writing the first TCASE spec, read `.github/skills/qualification-test-specification/templates/test-spec-swe6-qualification.tpl.md`.

---

## 1. Qualification Strategy Section (ASPICE BP1 RL.2)

Every qualification test spec file must include a `## Qualification Strategy` section that documents the qualification verification strategy. This section is **required** — without it, ASPICE BP1 cannot be assessed at RL.2 or above.

```markdown
## Qualification Strategy

- **Coverage scope**: <which req: IDs are in scope for this spec file>
- **Verification environment**: <e.g., native Linux test binary; uses production library linked against GTest fixture>
- **Entry criteria**:
  - All SWE.1 `req:` blocks for this component accepted
  - All SWE.3/SWE.4 artifacts for in-scope elements accepted
  - Integration tests (SWE.5) pass for all cross-element interactions
- **Exit criteria**:
  - Every in-scope `req:` ID with `verification_method: dynamic_test` is covered by a passing GTest
  - All review records for `req:` IDs with `verification_method: static_test` are filed in `doc/<component>/component_qualification_tests/static_test_reviews.md`
```

**Placement rule**: The Qualification Strategy section must appear once, between `## Metadata` and the first `## TCASE_NN` section.

**Scope**: One strategy section per spec file.

**File structure**: `# Test Specification: <name>` → `## Metadata` → `## Qualification Strategy` → `## TCASE_01` → ...

---

## 2. YAML Field Specialisation

Extends the shared YAML structure from `test-specification.instructions.md` § 2.

```yaml
id: qtest-{component}-{topic}-{aspect}
type: {test_type}
level: Component Acceptance
status: Draft
priority: {priority}
fully_automated: true
verifies: {requirement_id}   # Use the full req: ID from SWE.1, e.g. req:libipc-server-listen-success
```

| Field | Allowed Values | Notes |
|---|---|---|
| `id` | `qtest-<component>-<topic>-<aspect>` | Qualification test prefix |
| `level` | `Component Acceptance` | |
| `verifies` | Exact `req:` ID from SWE.1 | e.g., `req:libipc-server-listen-success`; the `req:` prefix is part of the value |

## 3. One TCASE per req: ID

Never combine multiple `req:` IDs into a single TCASE section. If several requirements are tested by the same GTest, write separate TCASE sections — one per `req:` ID.

## 4. Black-Box Proxy Patterns for Uninjectable Failure Paths

When a requirement describes an error path that cannot be triggered through the public API, two proxy patterns are accepted: **guard-entry proxy** (call the operation before the component reaches its valid state) and **observable-effects proxy** (assert all observable side effects of the full sequence are present).

Rules:
- A `NOTE:` comment in the Description must acknowledge the constraint.
- A `// Black-box qualification note:` comment at the top of the test body.
- Do **not** use proxies when a real trigger is available.

## 5. File Organisation — Qualification Suffix

One spec file per `_briefing.md` group heading:

```
<heading_snake_case>_tests.md
```

Example: `Connection Setup` → `connection_setup_tests.md`

If no `_briefing.md` exists, WARN the user and propose falling back to the SWE.1 topic structure; wait for confirmation before proceeding.

**File structure**: `# Test Specification: <name>` → `## Metadata` → `## Qualification Strategy` → `## TCASE_01` → ...

## 6. Spec-Side Prohibited Patterns

| Pattern | Why Prohibited |
|---|---|
| TCASE section without `verifies:` field | Breaks bidirectional traceability |
| `verifies:` pointing to a non-existent `req:` ID | Creates orphaned spec |
| TCASE without `id:` field | Breaks stable traceability |
| TCASE without Description and Test Procedure | Insufficient for implementation |
| Multiple `req:` IDs in a single TCASE section | Breaks one-to-one traceability |
| `static_test` requirement covered by a TCASE | `static_test` reqs must be filed in `static_test_reviews.md`, not as TCASEs |
| Modifying SWE.1 `.md` files from within a SWE.6 agent | Out of scope; use SWE.1 agents |
| Failure injection via real OS conditions | Inject via stub or test double |

## 7. Review Criteria (T-Review Checklist)

Use these numbered criteria for spec review (Phase 1 T4) and T-Review (Phase 2 T3). Cite by ID.

**QR01** — Each TCASE has `verifies:` referencing exactly one real SWE.1 `req:` ID (one TCASE per req, except for split-test justification)
**QR02** — Description corresponds directly to the `:verification_criteria:` of the covered `req:`; not a restatement of the description
**QR03** — `type:` is one of the ISO 25010 quality characteristics: `Functional Suitability`, `Performance Efficiency`, `Reliability`, `Security`, `Compatibility`, `Fault Injection`, `Stress Testing`, `Resource Usage`, or `Back-to-Back Testing`; `no_test` req: IDs must have a justification comment in the spec
**QR04** — `TEST_F` bodies use only the public API; no access to private implementation details (strict black-box)
**QR05** — Each `TEST_F` has `@req req:<id>` annotation referencing a real SWE.1 `req:` ID
**QR06** — `TEST_F` body follows Arrange-Act-Assert; `FAIL()` stub not present
**QR07** — Fixture `SetUp`/`TearDown` uses the same deployment configuration as production; no test-specific shortcuts
**QR08** — Failure paths from the `req:` `:verification_criteria:` are exercised by proxy methods where direct injection is unavailable; not silently skipped
