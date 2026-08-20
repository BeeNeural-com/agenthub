---
name: test-implementation-mismatch
description: "Escalation protocol when a test build reveals an API mismatch between test specification prose and current src/ headers. Use when a compiler or linker error indicates a function, type, or symbol from the spec does not exist or differs in signature."
---

# Test Implementation Mismatch Protocol

This skill defines the escalation protocol for test implementation agents (SWE.5, SWE.6) when the test specification prose describes an API, behaviour, or interaction that does not match the current `src/` headers.

> **SWE.5/SWE.6 agents detect mismatches from build or test failures, not by reading `src/` directly.** If the build or test output reveals a signature mismatch, apply this protocol using the compiler or linker error as evidence.

---

## Overview

A **mismatch** is any of:
- A function, method, or type named in the spec does not exist in any `src/` header.
- The expected return type, parameters, or error codes differ from the actual signature.
- The spec describes an IPC protocol step that differs from the architecture `arch:` block description.
- An error code symbol name differs between the spec and the actual `src/` header.

---

## Lifecycle and Usage Pattern

### Step 1: Do not invent

**Do not** invent or stub the missing API. Write a comment in the test body:

```cpp
// MISMATCH: tspec describes <description> but src/<header>.h does not declare it.
// Blocked: see escalation in implementation report.
FAIL() << "API mismatch: see implementation report";
```

### Step 2: Record the mismatch

Produce a findings table in your response. The format differs by level:

#### SWE.4 (Unit test level)

```markdown
## API Mismatch Findings: SWE.4

| Element | Test describes | Actual `src/` API | Severity |
|---|---|---|---|
| arch:<id> | `ClassName::method(args)` | not declared in `src/<file>.h` | CRITICAL |
| arch:<id> | returns `ERR_FOO` | symbol is `ERROR_FOO` in header | WARNING |
```

#### SWE.5 (Integration test level)

```markdown
## Integration API Mismatch Findings: SWE.5

| SWE.2 ID | ispec describes | Actual SUT API / SWE.2 description | Severity |
|---|---|---|---|
| arch:<component>-<descriptive-kebab-id> | Provider sends confirmed size on accept | No such function in server header | CRITICAL |
| arch:<component>-<descriptive-kebab-id> | Request payload is `uint64_t` | Actual: `uint32_t` in current header | WARNING |
```

#### SWE.6 (Qualification test level)

```markdown
## API Mismatch Findings: SWE.6

| req: ID | tspec describes | Actual SUT API | Severity |
|---|---|---|---|
| req:<component>-<topic> | `createSegment(const char*, size_t)` | not found in any header | CRITICAL |
| req:<component>-<topic> | returns `ERR_NAME_TOO_LONG` | symbol is `ERROR_NAME_TOO_LONG` | WARNING |
```

### Step 3: Escalate

After presenting the findings table to the user, escalate automatically:

#### CRITICAL findings

Call `runSubagent` to fix the spec:

**SWE.4 CRITICAL:**
```json
{
  "description": "Add missing declaration to SWE.3 header",
  "prompt": "You are acting as the SWE.3 Detailed Design specialist.\n\nComponent: [component]\nMissing declaration: [ClassName::method(args)] in src/[file].h\nReason: SWE.4 test [TestName] requires this method.\n\nAdd the missing declaration to the header. Return: the updated function signature."
}
```

**SWE.5 CRITICAL:**
```json
{
  "description": "Correct SWE.5 ispec mismatch",
  "prompt": "You are acting as the SWE.5 Test Specification Writer specialist.\n\nComponent: [component]\nMismatch findings: [findings table]\nInstruction: Correct the ispec prose or the SWE.2 arch: block for accuracy.\n\nReturn: list of changes and any remaining SWE.2 issues."
}
```

**SWE.6 CRITICAL:**
```json
{
  "description": "Correct SWE.6 tspec mismatch",
  "prompt": "You are acting as the SWE.6 Test Specification Writer specialist.\n\nComponent: [component]\nMismatch findings: [findings table]\nInstruction: Correct the tspec prose if it is the root cause. If SWE.1 :verification_criteria: is the root cause, flag it but do not edit the SWE.1 file.\n\nReturn: list of changes and any remaining SWE.1 issues."
}
```

Block until the upstream agent responds, then resume implementation.

#### WARNING findings

Do not block. Implement the test with the best available match and annotate the discrepancy:

```cpp
// WARNING: tspec uses 'ERROR_FOO' but header declares 'ERR_FOO'. Using ERR_FOO.
EXPECT_EQ(result, ERR_FOO);
```

Flag for user review in the implementation report.

---

## Reference / API

### Severity rules

| Finding type | Severity |
|---|---|
| Function/method not declared in any header | CRITICAL |
| Type not defined in any header | CRITICAL |
| Wrong parameter type or count | CRITICAL |
| Different symbol name for the same concept | WARNING |
| Different return type (compatible cast possible) | WARNING |
| Extra optional parameter missing from spec | WARNING (INFO if trivially defaultable) |
