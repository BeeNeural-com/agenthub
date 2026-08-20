---
name: qualification-tester-workflow
description: "Phase 1 (specification) and Phase 2 (implementation) execution steps for the Qualification Tester agent. Load this skill at the start of each phase to get the full T-step procedure, triage gates, and phase transition rules."
---

# Qualification Tester Workflow

This skill defines the execution procedure for both phases of qualification testing.
Load at the start of each phase. Normative format rules are in the auto-applied
instruction files; this skill covers the execution sequence.

---

## Triage Gate (before any work)

Perform all checks before proceeding:
1. Verify `tests/qualification/CMakeLists.txt` exists (no `_template` suffix).
2. Verify `tests/CMakeLists.txt` contains `add_subdirectory(qualification)`.
3. Confirm at least one `req:` block with `:verification_method: dynamic_test`
   or `:verification_method: static_test` exists in the component requirements.
4. If any check fails, HALT and report which check failed.

---

## Verification Method Routing

Before writing TCASEs, classify each in-scope `req:` ID:

| Verification Method | Action |
|---|---|
| `dynamic_test` | Write TCASE + GTest |
| `static_test` | Add row to `static_test_reviews.md` (see below); no TCASE, no GTest |
| `no_test` | Skip entirely; out of scope |

### static_test handling

Add a row to `doc/<component>/component_qualification_tests/static_test_reviews.md`
(create if absent). Columns: `req_id | review_method | pr_link | reviewer | date | status`.

> **TODO**: This is a temporary solution. The agent registers the requirement as
> awaiting static review. Only a human review event should mark it as "Covered (static)".
> A future improvement will separate registration from coverage assertion.

---

## Phase 1: Specification

Read the template before writing the first spec:
`.github/skills/qualification-test-specification/templates/test-spec-swe6-qualification.tpl.md`

Mirror this heading structure exactly, in this order:
1. `# Test Specification: <name>`
2. `## Metadata` (YAML block)
3. `## Qualification Strategy`
4. `## Test Design`
5. `## TCASE_01:`, `## TCASE_02:`, ...
6. `## Critique (QR01-QR08)`
7. `## Coverage Table`

### Execute sequentially:

**T1 — Classify coverage.**
Read `_briefing.md` lines 1-30 (metadata only), then read ONLY the `###` section
matching your test spec topic via view_range. Skip all other sections.
Read the corresponding requirement file for your topic. Do not explore other files.
Identify all in-scope `req:` IDs with `dynamic_test` verification method.
Classify each by requirement type:
simple interaction, limits, state-machine, protocol, resource, error recovery.

**T2a — Design test conditions.**
For each in-scope `req:` ID:
- Use its requirement type classification.
- Select technique(s) per the `test-design-techniques` skill minimum coverage table.
- Produce a `## Test Design` section with columns:
  `req: ID | Requirement Type | Technique(s) | Condition Count | Conditions`.
- If any ID has fewer conditions than its type requires, HALT.

**T2b — Write TCASE specs + GTest stubs (black-box).**
Each TCASE maps to one or more conditions from the design table.
Follow the template structure and instruction file format rules.
Tests must use only the public API; no internal state access.
GTest stubs MUST contain only `FAIL() << "Phase 1 stub"`. Do NOT write
EXPECT/ASSERT lines, test logic, or implementation code. Ignore any existing
test body content in .cpp files; overwrite with pure FAIL() stubs.

**T3 — Traceability check.**
Verify every `req:` ID in scope has at least one TCASE with a matching `verifies:` field.
Verify no TCASE references a `req:` ID that does not exist.

**T4 — Critique (QR01-QR08).**
Load the `cross-model-review` skill. Use template `templates/qualification-phase1.md`:
- Fill all placeholders (upstream req: block excerpts with verification_criteria, full spec content).
- Invoke independent reviewer per the protocol; self-critique as fallback.
- Record findings in a `## Critique (QR01-QR08)` section (before Coverage Table).
- Address all FAIL findings before proceeding. BLOCKED only for upstream constraints.

Phase 1 ends here. Report the spec to the user and wait for Phase 2 approval.

---

## Phase 2: Implementation

### Header access rule

When reading `src/` headers for API signatures, use only:
- Public class names, method signatures, enum values, typedefs.

Ignore: private sections, `@details` Doxygen blocks, `@req` annotations.
Test design comes from requirements, not headers.

### Execute sequentially:

**T1 — Read all stubs in full.**
`@req` annotations are normative traceability links.

**T2 — Implement black-box AAA bodies.**
Follow the `test-body-conventions` skill for step mapping and format.
Use only the public API. No private members, no friend access, no internal state.

**T3 — Critique (QR04-QR08).**
Load the `cross-model-review` skill. Use template `templates/qualification-phase2.md`:
- Fill all placeholders (upstream req: block excerpts, spec for cross-reference, full test source).
- Invoke independent reviewer per the protocol; self-critique as fallback.
- Record findings in the test output or report.
- Address all FAIL findings before proceeding to build. BLOCKED only for upstream constraints.

**T4 — Build.**
If the build fails after 3 attempts, HALT and report the error.
Do not attempt further fixes.

**T5 — Run.**
Execute the test binary and collect results. If tests fail, follow the debug loop below.

**T6 — Coverage table.**
List every in-scope `req:` ID using the canonical states from
`test-specification.instructions.md`:
- **Verified**: all GTests built and passing
- **Fully Implemented**: all bodies implemented, not yet built/run
- **Partially Implemented**: some GTest bodies implemented, others remain `FAIL()`
- **Fully Specified**: TCASE + GTest stub exist (with `FAIL()`) but body not implemented
- **Partially Specified**: TCASE exists but GTest stub not written
- **Uncovered**: ID in scope with no TCASE spec
- **Blocked**: cannot test due to `src/` defect (use only in coverage table, not as TCASE status)
- **Registered for static review**: listed in `static_test_reviews.md`, awaiting human review

**T7 — Structured completion summary.**
Report:
- Coverage table (from T6)
- BLOCKED items with handoff packets (affected ID, test file path, error evidence)
- Test pass/fail counts

Phase 2 ends here. Do not start additional work.

---

## Debug Loop (T5 Failures)

When tests fail after build, follow this sequence before reporting results.

### Isolated re-run first

Re-run each failing test in isolation using `./build.sh --docker qualification_tests`.

To isolate a single test, use the GTest filter:
```bash
GTEST_FILTER="SuiteName.TestName" ./build.sh --docker qualification_tests
```

If a local `build/` directory exists from a coverage build:
```bash
./build/bin/{binary_name} --gtest_filter="SuiteName.TestName"
```

| Isolated result | Classification | Action |
|---|---|---|
| Still fails | Genuine failure | Enter debug loop |
| Now passes | Flaky / order-dependent | Record; likely resource leak from preceding test |

### Failure classes

| Class | Symptom | Fix action |
|---|---|---|
| 1 Assertion | Wrong expected value | Fix test logic |
| 2 Segfault | Crash | Run under GDB: `./build.sh --docker shell`, then `gdb ./bin/{binary}` |
| 3 Flaky | Passes in isolation | Replace sleep with polling |
| 4 Timeout/Hang | No output | `timeout 5` per test; for thread dumps: `gdb -batch -ex "thread apply all bt" -p <pid>` |
| 5 Build (on rebuild) | Compile error | Fix CMake/includes |
| 6 Spec Gap | API changed | Escalate to user; do not retry |

### Rules

- **Diff-minimalism**: only change what solves the stated problem.
- **Max 3 retries** per stage. After exhaustion, report full debug history and escalate.
- **Final confirmation**: after all fixes, re-run the full suite once to catch regressions.

---

## BLOCKED Item Handling

When a test fails due to a `src/` defect:
1. Mark `// BLOCKED: <reason>` in the test body.
2. Record the ID as Blocked in the coverage table.
3. Present a handoff packet to the user:
   - Affected `req:` ID
   - Test file path
   - Error evidence (compiler error, assertion failure, or runtime error)
4. Stop work on that ID (agent Rule 6 applies).

---

## Failure Scenario Coverage

If upstream requirement documents describe a failure scenario or error path,
it MUST appear as either:
- A test condition (Error Guessing technique) in the design table, OR
- An entry marked Blocked in the coverage table with a documented reason.

TCASE `status:` always remains `Draft`. Blockage is tracked in the coverage
table only, never as a TCASE status value.

Silently omitting documented failure scenarios is a coverage defect.
