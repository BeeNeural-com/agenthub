---
name: qualification-test-specification
description: "SWE.6 qualification test worked examples: fixture patterns, black-box proxy techniques for uninjectable error paths, and a complete calculator spec-to-stub walkthrough."
---

# SWE.6 Qualification Test — Worked Examples & Patterns

Rules are split across three instruction files (auto-applied):
- `test-specification.instructions.md` — shared TCASE format, YAML, body requirements
- `qualification-test-specification.instructions.md` — SWE.6 delta: req: traceability, black-box proxies, QR01–QR08
- `test-implementation.instructions.md` — `.cpp` rules: annotations, file naming, fixture, step mapping, debug loop

**Test body step-mapping convention**: Read `.github/skills/test-body-conventions/SKILL.md` before implementing any GTest body.

**Template**: `templates/test-spec-swe6-qualification.tpl.md` — read before writing first spec.

This skill provides **worked examples only** — no normative rules.

---

## Fixture Example

All qualification tests for a component share a single fixture header:
```
tests/qualification/<component>_qualification_test_fixture.h
```

```cpp
#pragma once
#include "gtest/gtest.h"
// Include the component's public API header(s)

class <Component>Test : public ::testing::Test
{
protected:
    void SetUp() override  // NOLINT(readability-identifier-naming)
    {
        // initialize component under test using production configuration
    }

    void TearDown() override  // NOLINT(readability-identifier-naming)
    {
        // release resources
    }

    // Declare SUT instance(s) and helpers here
};
```

### Multi-Client Accept Example

```cpp
// WRONG — only the first accept is processed
for (std::size_t i = 0; i < kNumClients; ++i) {
    clients[i].connect(kSocketPath);
}
server.processEvents();  // processes only 1 accept
EXPECT_EQ(server.getClientCount(), kNumClients);  // FAILS

// CORRECT — one processEvents() call per expected event
for (std::size_t i = 0; i < kNumClients; ++i) {
    clients[i].connect(kSocketPath);
}
for (std::size_t i = 0; i < kNumClients; ++i) {
    server.processEvents();  // processes 1 accept each
}
EXPECT_EQ(server.getClientCount(), kNumClients);  // PASSES
```

---

## Black-Box Proxy Examples

When a requirement describes an error path that cannot be triggered through the public API, use one of these proxy techniques.

### Guard-Entry Proxy Example

Call the operation before the component reaches its valid/ready state. This verifies the error-return branch without OS-level fault injection.

```cpp
/*!
 * @req   req:<component>-<operation>-unready-error
 * @brief <operation>() returns error when called before listen().
 */
TEST_F(<Component>Test, <Operation>BeforeListenReturnsError)
{
    // Arrange: component constructed but NOT started via listen()
    // Black-box qualification note: Direct poll() failure is uninjectable.
    //          Guard-entry proxy — calling processEvents() on an unstarted
    //          instance is the closest observable equivalent.

    // Act: call the operation on the unready component
    const auto result = sut_.<operation>();

    // Assert: error code returned
    EXPECT_EQ(result, <ErrorCode>);
}
```

**Use when**: the guarded entry path is the closest observable equivalent. See `qualification-test-specification.instructions.md` § 3 for proxy rules.

### Observable-Effects Proxy Example

Assert that **all observable side effects** of the full sequence are present, proving the component completed the entire path including the error branch.

```cpp
/*!
 * @req   req:<component>-cleanup-continues-on-error
 * @brief Full cleanup completes even when internal close() fails.
 */
TEST_F(<Component>Test, CleanupCompletesAllSteps)
{
    // Arrange: connect N clients, start server
    // Black-box qualification note: Internal close() failure is uninjectable.
    //          Observable-effects proxy — asserting all cleanup side effects
    //          proves the full sequence completed.

    // Act: trigger shutdown
    sut_.stop();

    // Assert: all observable effects present
    EXPECT_EQ(sut_.getClientCount(), 0);         // all connections closed
    EXPECT_FALSE(fileExists(kTestSocketPath));     // socket file removed
    // ... additional side-effect assertions ...
}
```

**Use when**: the internal error is demonstrably uninjectable via the public API.

Rules for when to use proxies are in `qualification-test-specification.instructions.md` § 3.

---

## Calculator Example

Component: `libcalculator`. Covers `req:libcalculator-add-success` and `req:libcalculator-add-overflow-failure`.

**Test specification** (`doc/component_qualification_tests/libcalculator/arithmetic_tests.md`):

```markdown
# Test Specification: libcalculator-arithmetic

<!-- Template: SWE.6 Software Qualification Test Specification -->
<!-- Verifies: Software Requirements (req:*) -->
<!-- ASPICE: SWE.6 — Software Qualification Testing -->

---

## Metadata

```yaml
spec: libcalculator-arithmetic
feature: arithmetic operations
component: libcalculator
req: req:libcalculator-add-success
aspice_level: SWE.6
```

---

## TCASE_01: Add returns correct sum

```yaml
id: qtest-libcalculator-arithmetic-add-success
type: Functional Suitability
level: Component Acceptance
status: Draft
priority: High
fully_automated: true
verifies: req:libcalculator-add-success
```

### Description

Verify that the Calculator `add()` operation returns the correct sum when called with valid non-overflowing integer operands.

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | Construct a Calculator instance (step 1 of uc-calculate-sum) | Instance created |
| 2 | Call `add()` with operands 3 and 4 (step 2) | Error code indicates success |
| 3 | Read result (step 4) | `result == 7` |

---

## TCASE_02: Add detects overflow

```yaml
id: qtest-libcalculator-arithmetic-add-overflow
type: Functional Suitability
level: Component Acceptance
status: Draft
priority: High
fully_automated: true
verifies: req:libcalculator-add-overflow-failure
```

### Description

Verify that the Calculator `add()` operation returns an arithmetic overflow error when the sum exceeds the int32_t range.

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | Construct a Calculator instance (step 1 of uc-calculate-sum). Set firstOperand to INT32_MAX and secondOperand to 1 | Instance created |
| 2 | Call `add()` with the two operands (step 2) | Error code indicates arithmetic overflow |
| 3 | Read output parameter (step 3, failure path) | Output parameter is unchanged |
```

**Fixture** (`tests/qualification/libcalculator_qualification_test_fixture.h`):

```cpp
#pragma once
#include <gtest/gtest.h>
#include "libcalculator/Calculator.h"

class LibcalculatorTest : public ::testing::Test {
protected:
    void SetUp() override    { /* default-construct is sufficient */ }
    void TearDown() override { /* nothing to release */ }

    libcalculator::Calculator calculator_;
};
```

**GTest file** (`tests/qualification/libcalculator_tspec_arithmetic.cpp`):

```cpp
#include "libcalculator_qualification_test_fixture.h"
#include <climits>

/*!
 * @req   req:libcalculator-add-success
 * @brief add() returns the correct sum for non-overflowing operands.
 */
TEST_F(LibcalculatorTest, AddReturnsCorrectSum)
{
    // Arrange (step 1): default-constructed Calculator instance.
    std::int32_t result{0};

    // Act (step 2): call add with non-overflowing operands.
    const auto errorCode = calculator_.add(3, 4, result);

    // Assert (step 4): success and correct sum.
    EXPECT_FALSE(errorCode);
    EXPECT_EQ(result, 7);
}

/*!
 * @req   req:libcalculator-add-overflow-failure
 * @brief add() returns an overflow error when the result exceeds int32_t range.
 */
TEST_F(LibcalculatorTest, AddOverflowReturnsError)
{
    // Arrange (step 1): default-constructed Calculator instance.
    // Arrange (step 2): operands that cause overflow.
    FAIL() << "Not yet implemented";
}
```
