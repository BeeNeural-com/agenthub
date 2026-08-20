---
name: integration-test-specification
description: "SWE.5 integration test worked examples: fixture patterns, socket path strategy, event-loop cap conventions, multi-element test strategies, and a complete calculator spec-to-stub walkthrough."
---

# SWE.5 Integration Test — Worked Examples & Patterns

Rules are split across three instruction files (auto-applied):
- `test-specification.instructions.md` — shared TCASE format, YAML, body requirements
- `integration-test-specification.instructions.md` — SWE.5 delta: Integration Strategy, `arch:` ID traceability (with classification subtypes), IR01–IR08
- `test-implementation.instructions.md` — `.cpp` rules: annotations, file naming, fixture, step mapping, debug loop

**Test body step-mapping convention**: Read `.github/skills/test-body-conventions/SKILL.md` before implementing any GTest body.

**Template**: `templates/test-spec-swe5-integration.tpl.md` — read before writing first spec.

This skill provides **worked examples only** — no normative rules.

---

## Fixture Example

All integration tests for a component share a single fixture header:
```
tests/integration/<component>_integration_fixture.h
```

```cpp
#pragma once
#include "gtest/gtest.h"
#include <string>
#include <thread>

class <Component>IntegrationTest : public ::testing::Test
{
protected:
    static constexpr const char* kTestSocketPath = "/tmp/<component>_integration_test.sock";

    void SetUp() override  // NOLINT(readability-identifier-naming)
    {
        ::unlink(kTestSocketPath);  // Pre-clean
        // Start server on kTestSocketPath
        // Wait for server to be ready to accept connections
    }

    void TearDown() override  // NOLINT(readability-identifier-naming)
    {
        // Shut down server
        ::unlink(kTestSocketPath);  // Post-clean
        // Close any open client connections
    }
};
```

### Event-Loop Cap Example

```cpp
/// Maximum number of server+client processEvents() alternation pairs.
/// Sufficient for two full message round-trips on a loopback socket
/// without busy-waiting.
static constexpr int kMaxEventIterations = 20;
```

### Direction-Specific Event Loop Example

```cpp
// CORRECT — only server processes the accept
server.processEvents();

// WRONG — bidirectional loop causes hang when client uses MSG_WAITALL
driveEventsUntil([&] { return server.hasClient(); });  // client blocks
```

---

## Multi-Element Test Patterns

### Pattern 1 — In-process server + client (preferred)

Run server and client as in-process objects. Server started in background thread in `SetUp`, shut down in `TearDown`. Simpler, fully deterministic. Does not exercise process-level isolation.

### Pattern 2 — Separate processes (for isolation tests)

Server as child process; client in test process. Use synchronization primitive to confirm server ready. Required when test depends on process isolation (credential verification, resource limits, crash recovery).

---

## Calculator Example

Component: `libcalculator`. No IPC or threads; fixture just constructs and destroys the object.

**Test specification** (`doc/component_integration_tests/libcalculator/arithmetic_integration_tests.md`):

```markdown
# Test Specification: libcalculator-arithmetic

## Metadata

```yaml
spec: libcalculator-arithmetic
feature: arithmetic operations
component: libcalculator
aspice_level: SWE.5
```

## Integration Strategy

- **Integration order**: Single element; no multi-element ordering required.
- **Verification environment**: Native Linux process; no IPC or hardware required.
- **Entry criteria**:
  - All SWE.2 `arch:` blocks accepted.
  - All SWE.3 headers carry `@elaborates` annotations.
  - Unit tests pass for all elements.
- **Exit criteria**:
  - Every integration-scope `arch:` ID (classification: sequence, statemachine, or activity) covered by a TCASE (or excluded). Integration-scope means the behavior is observable across element boundaries or explicitly allocated to integration verification in the architecture briefing.
  - All GTests pass.

## TCASE_01: Add produces correct result

```yaml
id: itest-libcalculator-arithmetic-add-lifecycle
type: Functional Suitability
level: Integration Test
status: Draft
priority: High
fully_automated: true
verifies: arch:libcalculator-seq-add-lifecycle
```

### Description

Verify that the Calculator `add()` operation returns the correct sum when called with valid integer operands via the public API.

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | Construct a Calculator instance | Instance created successfully |
| 2 | Call `add(3, 4, result)` | Error code indicates success |
| 3 | Read `result` | `result == 7` |
```

---

**Example 2 — Lifecycle test (verifies statemachine `arch:` ID):**

```yaml
id: itest-libcalculator-segment-api-full-lifecycle
type: Functional Suitability
level: Interface Test
status: Draft
priority: High
fully_automated: true
verifies: arch:libcalculator-segment-lifecycle
```

### Description

Verify the segment API contract across its full lifecycle: create, map, read, and release.
Cross-element interaction: the Provider element creates the segment and the Consumer element
maps it into its address space; the two roles share the same region through the segment API
boundary.

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | Request the Provider to create a named segment of 64 bytes | Returns success; segment handle valid |
| 2 | Request the Consumer to open the same named segment | Returns success; data pointer non-null |
| 3 | Write a known pattern via the Provider handle | Write returns success |
| 4 | Read the same region via the Consumer handle | Read bytes match the written pattern |
| 5 | Release both handles | No errors; segment is unmapped |
```

> **Multi-value `verifies:` (comma-separated):** When an existing TCASE already exercises the full
> behavior of an additional `arch:` ID, add it to the same `verifies:` field
> rather than writing a new TCASE:
> ```yaml
> verifies: arch:libcalculator-segment-lifecycle, arch:libcalculator-seq-segment-exchange
> ```
> The dashboard parser accepts a comma-separated list on a single line.
>
> **Preferred pattern (separate TCASEs, shared GTest):** When both `arch:` IDs have distinct
> test steps, write two TCASE sections and annotate the single GTest with one `@arch` per ID:
> ```cpp
> /*!
>  * @arch  arch:libcalculator-seq-segment-exchange
>  * @arch  arch:libcalculator-segment-lifecycle
>  * @brief Segment created, mapped, data exchanged, and released.
>  */
> TEST_F(CalculatorIntegrationTest, SegmentExchangeFullLifecycle) { ... }
> ```
> Use comma-separated `verifies:` only when the second TCASE would be a pure duplicate of the first.

**Fixture** (`tests/integration/libcalculator_integration_fixture.h`):

```cpp
#pragma once
#include <gtest/gtest.h>
#include "libcalculator/Calculator.h"

class CalculatorIntegrationTest : public ::testing::Test {
protected:
    void SetUp() override    { /* default-construct is sufficient */ }
    void TearDown() override { /* nothing to release */ }

    libcalculator::Calculator calculator_;
};
```

**GTest stub** (`tests/integration/libcalculator_ispec_arithmetic.cpp`):

```cpp
#include "libcalculator_integration_fixture.h"

/*!
 * @arch        arch:libcalculator-seq-add-lifecycle
 * @req        req:libcalculator-add-success
 * @brief      add() returns the correct sum via the public API.
 */
TEST_F(CalculatorIntegrationTest, AddProducesCorrectResult)
{
    // Arrange
    std::int32_t result{0};

    // Act
    const auto errorCode = calculator_.add(3, 4, result);

    // Assert
    EXPECT_FALSE(errorCode);
    EXPECT_EQ(result, 7);
}
```
