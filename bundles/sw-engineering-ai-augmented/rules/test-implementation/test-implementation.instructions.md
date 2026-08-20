---
description: Rules for implementing GTest test bodies in tests/integration/ and tests/qualification/. Covers file placement, fixture conventions, GTest annotations, file naming, step mapping, code quality, pre-build validation, and debug loop. Single source of truth for all .cpp implementation rules shared across SWE.5 and SWE.6.
applyTo: "**/tests/integration/**/*.cpp,**/tests/integration/**/*.h,**/tests/qualification/**/*.cpp,**/tests/qualification/**/*.h"
---

# Test implementation rules

Applies when editing GTest files in `tests/integration/` or `tests/qualification/`.

---

## 1. File placement protocol

Decide before writing any code.

**APPEND_EXISTING** (default): same binary, same fixture, same feature family, no material boundary.

**CREATE_NEW**: only when a real boundary exists:
- `FIXTURE_BOUNDARY`: different base fixture or lifecycle
- `BINARY_BOUNDARY`: different test binary or execution environment
- `FEATURE_BOUNDARY`: materially different feature area
- `SCOPE_BOUNDARY`: integration vs. qualification

Rules:
- Do not default to CREATE_NEW just because a new spec file exists.
- If CREATE_NEW: update `CMakeLists.txt` and justify.
- Always list candidate files considered.

Record the decision with fields: File placement, Target, Boundary, Justification.

---

## 2. GTest file naming

### SWE.5 integration tests

```
tests/integration/<component>_ispec_<topic>.cpp
tests/integration/<component>_integration_fixture.h
```

### SWE.6 qualification tests

```
tests/qualification/<component>_tspec_<topic>.cpp
tests/qualification/<component>_qualification_test_fixture.h
```

Never place SWE.5 files outside `tests/integration/` or SWE.6 files outside `tests/qualification/`.

---

## 3. GTest annotation rules

### SWE.5 integration tests

The annotation tag is `@arch`. Its value is a unified `arch:` ID from SWE.2 (with `classification: sequence`, `statemachine`, or `activity`). Legacy test files may still use `@arch-seq`; both are accepted but new code must use `@arch`.

```cpp
/*!
 * @arch arch:<component>-<descriptive-kebab-id>
 * @req req:<component>-<req-short-name>
 * @brief <One-sentence summary; must fit on a single line>
 */
TEST_F(<IntegrationFixture>, <DescriptiveCamelCaseName>)
```

| Annotation | Required | Rule |
|---|---|---|
| `@arch` | Always | Value is an `arch:` ID from SWE.2 with `classification: sequence`, `statemachine`, or `activity` |
| `@req` | Optional | Include when a direct SWE.1 context tag is useful |
| `@brief` | Always | Single line; no embedded newlines |

- At least one `@arch` must be present for SWE.5 traceability. If the annotation is missing or its value does not match a real SWE.2 ID, flag the test with a `// TODO: missing @arch` comment.
- A test may carry multiple `@arch` or `@req` lines. When one GTest implements multiple TCASEs (multi-value `verifies:` in the spec, or co-annotation of a statemachine alongside a sequence), add one `@arch` line per referenced `arch:` ID.
- Unimplemented stubs must include: `FAIL() << "Integration test not yet implemented";`

### SWE.6 qualification tests

```cpp
/*!
 * @req req:<component>-<short-name>
 * @brief <One-sentence summary; must fit on a single line>
 */
TEST_F(<Fixture>, <DescriptiveCamelCaseName>)
```

- `@req` value must exactly match the `verifies:` field from the TCASE YAML. If `@req` is missing or its value does not match a real SWE.1 ID, flag the test with a `// TODO: missing @req` comment.
- `@brief` must be a single line (no embedded newlines).
- One test may carry multiple `@req` lines if it verifies multiple requirements.
- Unimplemented stubs must include: `FAIL() << "Test not yet implemented";`

---

## 4. Fixture conventions

- **Discover the existing fixture first.** Read all `*_fixture.h` files in the test directory before creating a new one.
- **`SetUp()` / `TearDown()`**: add `// NOLINT(readability-identifier-naming)` on both overrides (Automotive Open System Architecture (AUTOSAR) naming rule).
- **Guard cleanup in `TearDown()`** against null/invalid state: must be safe even if SetUp failed partway.
- **Shared helpers** go in the fixture. Do not duplicate infrastructure across test files.
- After implementing test bodies, delete unused fixture members and local variables.

### Integration-specific fixture rules

- Use an **explicit-step fixture**: minimal `SetUp`/`TearDown`; each test body calls `processEvents()` explicitly. Do not create helpers that hide how many event-processing iterations occurred.
- **Exception**: A bidirectional event-driving helper is acceptable only for connection establishment.
- **Socket paths**: Use a fixed named constant. Pre-clean in `SetUp()` and post-clean in `TearDown()` via `::unlink()`.
- **Event-loop iteration caps**: Must be a named constant with a comment explaining why the bound is sufficient. No magic integers.
- **Direction-specific loops**: Use single-side loops when only one side should process events. Bidirectional helpers cause hangs with blocking read protocols.

### Qualification-specific fixture rules

- `SetUp`/`TearDown` must use the same deployment configuration as production (QR07).
- No test-specific shortcuts that would not exist in a real deployment.
- Tests use only the public Application Programming Interface (API) (QR04); do not access private members.

---

## 5. Spec-to-code step mapping (normative)

Every implemented test body must map **one-to-one** to the Test Procedure table from its TCASE specification. This mapping is the primary review artifact; a human reviewer must be able to verify compliance by reading the test body alongside the spec table.

Both SWE.5 and SWE.6 test implementations follow the same rules. For accepted syntax formats and worked examples, load the `test-body-conventions` skill.

### 5.1 Rules

1. **Every step appears.** No Test Procedure step may be silently skipped. If a step cannot be implemented, add `// Step N: BLOCKED: <reason>`.
2. **Step numbers are normative.** They anchor the review. A reviewer reads Step 3 in the spec and finds `(step 3)` or `Step 3:` in the code.
3. **Verbatim preferred.** Step comments should reuse wording from the spec table. Minor adaptation for code context is acceptable.
4. **Multiple Acts/Asserts.** When a test has multiple phases, repeat the label with the correct step: `// Act (step 5):`, `// Assert (step 5):`.
5. **Step ranges.** Use a hyphen: `(steps 6-8):`. Only for truly atomic code blocks that implement multiple steps at once.
6. **Failure paths.** Append annotation: `(step 4, failure path):`.
7. **Continuation lines.** Use 10-space indent: `//          (step 2): <continuation>`.

### 5.2 Prohibited patterns

| Pattern | Why Prohibited |
|---|---|
| Plain `// Arrange:`, `// Act:`, `// Assert:` without step numbers | Breaks spec-to-code traceability; reviewer cannot verify step coverage |
| Ad-hoc step numbering that does not match the spec table | Creates false traceability; misleads reviewers |
| Grouping multiple spec steps under one comment without listing each | Hides which steps are implemented |

---

## 6. Implementation-side prohibited patterns

| Pattern | Why Prohibited |
|---|---|
| Failure-path Arrange using real OS-level conditions | Fragile in Continuous Integration (CI); use a stub or test double |
| Test binary overrides `-D` macro that controls class member array sizes without recompiling the linked library | Application Binary Interface (ABI) mismatch: `sizeof(Class)` disagrees across compilation units, causing heap corruption. Build a separate library target with the same define. |
| Sending zero-length messages in single-threaded tests against `MSG_WAITALL` readers | `recv(fd, buf, 0, MSG_WAITALL)` blocks indefinitely on Linux STREAM sockets even when `poll()` returns `POLLIN`. Cover zero-length framing at the unit test level only. |

---

## 7. Code quality gate

Run after writing all test code, before T-Review.

**Zero magic numbers**: every literal must be a named constant or structurally obvious (`0`, `1` in loop counters).
**Every sleep must use a named constant and include a comment explaining its purpose.** Prefer polling/condition-driven waits over fixed sleeps.
**Use existing infrastructure**: check whether the fixture already provides a helper before writing a new one.
**Minimize**: no verbose logging duplicating assertions, no single-use helper variables, no commented-out code, no unused includes.

---

## 8. Pre-build validation

**Step 0: Always use `./build.sh --docker <target>`.** Direct `cmake --build` or `make` invocations will fail outside the Docker build environment. There is no local toolchain.

Run the checklist below before invoking the build. If any check fails, stop and report.

1. **CMakeLists exists**: verify the test `CMakeLists.txt` exists with no `_template` suffix.
2. **Parent wiring**: verify `tests/CMakeLists.txt` contains `add_subdirectory({subdir})`.
3. **Source files registered**: every `.cpp` in the test directory is listed in the CMakeLists.
4. **e3sdk_metadata guard**: verify `e3sdk_metadata` contains an `e3swp` target entry.

---

## 9. Debug loop

When tests fail after build, follow the debug loop in the tester workflow skill (`integration-tester-workflow` or `qualification-tester-workflow`). Core constraints: max 3 retries per stage (then escalate), diff-minimalism only, full suite re-run after fix, immediate escalation on spec gaps.

---

## 10. Phase 2 T-review crosswalk

During Phase 2 T-Review (Phase 2 T3), the level-specific review criteria (IR01-IR08 for SWE.5, QR01-QR08 for SWE.6) are the authoritative checklist. The implementation-relevant subset maps to rules already in this file:

| Review ID | Criterion | This file |
|---|---|---|
| IR05 | Each `TEST_F` has `@arch` annotation referencing a real SWE.2 `arch:` ID | § 3, SWE.5 annotations |
| IR06 | `TEST_F` body uses only the public API | § 4, integration fixture rules |
| IR07 | Fixture `SetUp`/`TearDown` covers inter-element resources | § 4, integration fixture rules |
| QR04 | `TEST_F` bodies use only the public API (strict black-box) | § 4, qualification fixture rules |
| QR05 | Each `TEST_F` has `@req` annotation referencing a real SWE.1 ID | § 3, SWE.6 annotations |
| QR06 | `TEST_F` body follows Arrange-Act-Assert with step mapping; no `FAIL()` stub remains | § 5, Spec-to-code step mapping |
| QR07 | Fixture uses production configuration; no test-specific shortcuts | § 4, qualification fixture rules |
| QR08 | Failure paths exercised by proxy methods where direct injection unavailable; not silently skipped | § 6, implementation-side prohibited patterns (no real OS-level fault injection) |
