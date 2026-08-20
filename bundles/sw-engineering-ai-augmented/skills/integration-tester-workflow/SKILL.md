---
name: integration-tester-workflow
description: "Phase 1 (specification) and Phase 2 (implementation) execution steps for the Integration Tester agent. Load this skill at the start of each phase to get the full T-step procedure, triage gates, and phase transition rules."
---

# Integration Tester Workflow

This skill defines the execution procedure for both phases of integration testing.
Load at the start of each phase. Normative format rules are in the auto-applied
instruction files; this skill covers the execution sequence.

---

## Triage Gate (before any work)

Perform all checks before proceeding:
1. Verify `tests/integration/CMakeLists.txt` exists (no `_template` suffix).
2. Verify `tests/CMakeLists.txt` contains `add_subdirectory(integration)`.
3. Confirm at least one `arch:` block with `classification: sequence` or
   `activity` exists in the component architecture.
4. Confirm `_briefing.md` exists and contains an `## Integration Scope Decision`
   section listing primary SWE.5 targets.
5. If any check fails, HALT and report which check failed.

### Target Classification

- **Primary targets**: `arch:` IDs with `classification: sequence` or `activity`.
  These describe cross-element interactions and are the natural SWE.5 test subjects.
- **Secondary targets**: `arch:` IDs with `classification: statemachine` only when
  the state transitions are triggered by cross-element stimuli (e.g., a lifecycle
  state machine whose transitions depend on actions from another element). Verify
  this by checking whether the state machine diagram references actions from other
  elements as triggers.
- **Excluded**: `arch:` IDs with `classification: element`, `operation`, `data`, or
  `decision`. These describe single-element structure or behavior and belong in SWE.4.
- **Excluded from primary**: activity diagrams that describe purely internal control
  flow of a single element with no cross-element interactions. These are secondary at
  best. An activity qualifies as primary only if it processes events or signals
  originating from a different element.

---

## Phase 1: Specification

Read the template before writing the first spec:
`.github/skills/integration-test-specification/templates/test-spec-swe5-integration.tpl.md`

Mirror this heading structure exactly, in this order:
1. `# Test Specification: <name>`
2. `## Metadata` (YAML block)
3. `## Integration Strategy`
4. `## Test Design`
5. `## TCASE_01:`, `## TCASE_02:`, ...
6. `## Critique (IR01-IR08)`
7. `## Coverage Table`

### Execute sequentially:

**T1 — Load context (parallel reads).**
Issue ALL of the following reads in a SINGLE parallel response:
- `_briefing.md`: read only the `### <Heading>` section matching your topic.
- The sequence/activity diagram architecture file(s) referenced as Primary diagram
  in your briefing section.
- Any supporting architecture files referenced as Supporting IDs in your section.

Do not read unrelated sections or files. The briefing section identifies exactly
which architecture files are relevant for your topic.

**T2 — Interaction Extraction (MANDATORY).**

This step builds the Interaction Map: the primary source for test design. Every
TCASE derives from this map, not from individual arch: IDs in isolation.

From the sequence/activity diagrams loaded in T1:
1. Identify every message, signal, or control flow that crosses a boundary between
   distinct architectural elements (participants in the diagram).
2. Classify each crossing as one of:
   - **Boundary stimulus**: a publicly triggerable action by one element that causes
     an observable effect on another element. These are test candidates.
   - **Setup/enabling step**: internal or preparatory action that enables a boundary
     stimulus but is not directly testable (e.g., pool allocation, internal state
     initialization). These are preconditions, not test subjects.
3. For each boundary stimulus, record:
   - Source element (who sends/triggers)
   - Target element (who receives/reacts)
   - Trigger action (what the source does)
   - Cross-boundary observable (what the target must exhibit as a result)
   - Failure modes at the boundary (what can go wrong between source and target)

Produce the Interaction Map as a table:

```markdown
## Interaction Map

| # | Source → Target | Trigger Action | Cross-Boundary Observable | Boundary Failure Modes |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |
```

**Validation rules for the Interaction Map:**
- Every row must name two DISTINCT elements as Source and Target.
- Every row must describe an externally observable effect (not an internal state change).
- Rows where Source == Target are invalid; remove them or reframe as a causal chain
  that crosses at least one boundary.
- Cross-reference with the briefing Interactions table: any interaction in the diagram
  NOT covered by the briefing is a candidate additional test (flag for the user but
  do not halt).

**T3 — Design test conditions from the Interaction Map.**
For each boundary stimulus in the Interaction Map:
- Select technique(s) per the `test-design-techniques` skill minimum coverage table,
  using the diagram classification (sequence/activity) to determine minimum techniques.
- Each test condition must trace to a sequence or activity `arch:` ID via `verifies:`.
- Produce a `## Test Design` section with columns:
  `arch: ID | Classification | Technique(s) | Condition Count | Conditions`.
- If any primary ID has fewer conditions than its classification requires, HALT.

**Hard IR03 gate (applied at T3, enforced throughout):**
Every TCASE produced from the design table must satisfy ALL of the following:
- Names at least 2 distinct elements as active participants.
- Contains at least 1 causal chain that crosses a documented boundary between
  distinct elements (a stimulus on element A causes an observable effect on element B).
- The `verifies:` field points to a sequence or activity `arch:` ID (not an element,
  operation, data, or decision ID).

If a candidate TCASE cannot satisfy these criteria, it describes single-element
behavior and belongs in SWE.4. Remove it from the integration spec.

**T4 — Write TCASE specs + GTest stubs.**
Each TCASE maps to one or more conditions from the design table.
Follow the template structure and instruction file format rules.
The Test Procedure must show the cross-element interaction flow: which element is
stimulated, which element is observed, and what the expected cross-boundary effect is.
GTest stubs MUST contain only `FAIL() << "Phase 1 stub"`. Do NOT write
EXPECT/ASSERT lines, test logic, or implementation code. Ignore any existing
test body content in .cpp files; overwrite with pure FAIL() stubs.

**T5 — Traceability + IR03 structural validation.**
For each TCASE:
1. Verify `verifies:` points to a real `arch:` ID with `classification: sequence`
   or `activity`.
2. Extract the STIMULUS element (the element that initiates the interaction) and the
   OBSERVER element (the element on which the assertion is checked).
3. If STIMULUS == OBSERVER for all assertions in the TCASE, flag it as a potential
   SWE.4 item. Verify whether the causal chain still crosses a boundary even if the
   final assertion is on the same element (e.g., element A stimulates element B,
   which causes a callback back to element A). If no boundary crossing exists in the
   causal chain, remove the TCASE from the integration spec.
4. Verify every primary `arch:` ID in scope has at least one TCASE.
5. Verify no TCASE references a non-existent `arch:` ID.

**T6 — Critique (IR01-IR08).**
Load the `cross-model-review` skill. Use template `templates/integration-phase1.md`:
- Fill all placeholders (upstream arch: block excerpts, full spec content).
- Invoke independent reviewer per the protocol; self-critique as fallback.
- Record findings in a `## Critique (IR01-IR08)` section (before Coverage Table).
- Address all FAIL findings before proceeding. BLOCKED only for upstream constraints.

Phase 1 ends here. Report the spec to the user and wait for Phase 2 approval.

---

## Phase 2: Implementation

### Header access rule

When reading `src/` headers for API signatures, use only:
- Public class names, method signatures, enum values, typedefs.

Ignore: private sections, `@details` Doxygen blocks, `@req` annotations.
Test design comes from architecture, not headers.

### Execute sequentially:

**T1 — Read all stubs in full.**
`@arch` annotations are normative traceability links to `arch:` IDs.
`@req` is optional supporting context.

**T2 — Implement AAA bodies.**
Follow the `test-body-conventions` skill for step mapping and format.

**T3 — Critique (IR05-IR07).**
Load the `cross-model-review` skill. Use template `templates/integration-phase2.md`:
- Fill all placeholders (upstream arch: block excerpts, spec for cross-reference, full test source).
- Invoke independent reviewer per the protocol; self-critique as fallback.
- Record findings in the test output or report.
- Address all FAIL findings before proceeding to build. BLOCKED only for upstream constraints.

**T4 — Build.**
If the build fails after 3 attempts, HALT and report the error.
Do not attempt further fixes.

**T5 — Run.**
Execute the test binary and collect results. If tests fail, follow the debug loop below.

**T6 — Coverage table.**
List every in-scope `arch:` ID using the canonical states from
`test-specification.instructions.md`:
- **Verified**: all GTests built and passing
- **Fully Implemented**: all bodies implemented, not yet built/run
- **Partially Implemented**: some GTest bodies implemented, others remain `FAIL()`
- **Fully Specified**: TCASE + GTest stub exist (with `FAIL()`) but body not implemented
- **Partially Specified**: TCASE exists but GTest stub not written
- **Uncovered**: ID in scope with no TCASE spec
- **Blocked**: cannot test due to `src/` defect (use only in coverage table, not as TCASE status)

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

Re-run each failing test in isolation using `./build.sh --docker integration_tests`.

To isolate a single test, use the GTest filter:
```bash
GTEST_FILTER="SuiteName.TestName" ./build.sh --docker integration_tests
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
   - Affected `arch:` ID
   - Test file path
   - Error evidence (compiler error, assertion failure, or runtime error)
4. Stop work on that ID (agent Rule 6 applies).

---

## Failure Scenario Coverage

If upstream architecture documents describe a failure scenario or error path,
it MUST appear as either:
- A test condition (Error Guessing technique) in the design table, OR
- An entry marked Blocked in the coverage table with a documented reason.

TCASE `status:` always remains `Draft`. Blockage is tracked in the coverage
table only, never as a TCASE status value.

Silently omitting documented failure scenarios is a coverage defect.
