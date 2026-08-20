---
name: unit-test-specification
description: "Generic worked examples for ASPICE unit test specification and implementation: Doxygen spec blocks, GTest fixture classes, and Arrange-Act-Assert test bodies in tests/unit/. Use when writing or reviewing unit test files for E3 Software Platform components."
---

# SWE.4 Unit Test Specification — Skill Reference

This skill provides generic worked examples for SWE.4 unit test specification and implementation.
All SWE.4 artifacts are Doxygen-documented GTest files in tests/unit/.

---

## Generic Traceability Pattern

SWE.3 header uses `@elaborates arch:<id>`
→ SWE.4 test block uses `@covers arch:<id>` and `@req req:<id>`

---

## Example 1 — Fixture Pattern

```cpp
#pragma once

#include <gtest/gtest.h>
#include "resource_manager.h"

/*!
 * @brief Test fixture for ResourceManager unit tests.
 * @covers arch:<component>-<service-element>
 */
class ResourceManagerTest : public ::testing::Test {
protected:
    void SetUp() override
    {
        manager_ = std::make_unique<ResourceManager>(ManagerConfig{});
    }

    void TearDown() override
    {
        manager_.reset();
    }

    std::unique_ptr<ResourceManager> manager_;
};
```

---

## Example 2 — Specification Stub Pattern

```cpp
/*!
 * @brief Allocating a zero-size resource returns invalid argument.
 *
 * @req    req:<component>-<topic>-<validation>
 * @covers arch:<component>-<service-element>
 *
 * @pre  Service instance is initialized.
 * @post Output handle remains unchanged on failure.
 */
TEST_F(ResourceManagerTest, AllocateZeroSizeReturnsInvalidArgument)
{
    FAIL() << "Not yet implemented — SWE.4 stub";
}
```

---

## Example 3 — Implemented Test Pattern

```cpp
/*!
 * @brief Allocating a zero-size resource returns invalid argument.
 *
 * @req    req:<component>-<topic>-<validation>
 * @covers arch:<component>-<service-element>
 */
TEST_F(ResourceManagerTest, AllocateZeroSizeReturnsInvalidArgument)
{
    // Arrange
    constexpr std::size_t invalidSize = 0U;
    int handle = -1;

    // Act
    const auto result = manager_->allocate(1, invalidSize, handle);

    // Assert
    EXPECT_EQ(result, std::make_error_code(std::errc::invalid_argument));
    EXPECT_EQ(handle, -1);
}
```

---

## Checklist

- `@req` is mandatory.
- `@covers` is mandatory.
- Use `@pre` and `@post` for observable contracts.
- Stubs must use explicit `FAIL()` placeholders.
- Implementations must keep Arrange/Act/Assert structure.

## ASPICE Rating Guidelines

For the official Automotive SPICE rating rules that govern SWE.4 process assessment (code coverage purpose, automation self-verification, explorative testing, release plan independence), see:

- [aspice-rating-guidelines.adoc](./aspice-rating-guidelines.adoc) — VDA Automotive SPICE Guidelines, 2nd Edition 2023, Section 3.11: rating rules RL.1–RL.4 with conditions and consequences.

---

## Coverage Classification

Before starting, classify each `arch:` ID:

| State | Criteria |
|---|---|
| **COMPLETE** | `@covers arch:<id>` exists in at least one `TEST_F` with a real Arrange-Act-Assert body (no `FAIL()` stub) |
| **SPEC_ONLY** | Doxygen `/*!` spec block + `FAIL()` stub exists but no implementation |
| **MISSING** | No `@covers arch:<id>` reference in any `tests/unit/` file |

---

## Per-File Fixture Subclass Rule

Every test file must declare its own named fixture subclass immediately after the includes:

```cpp
// Per-file fixture subclass — prevents GTest suite-name collisions across test files.
// All TEST_F macros in this file use <Element>Test, not the shared base class name.
class <Element>Test : public <ComponentName>Test {};
```

**Rationale for subclassing**: GTest identifies tests by `(SuiteName, TestName)`. Two files using the same base-class suite name with the same test case name causes a silent duplicate registration where the second wins and the first never runs. A per-file subclass gives each file a unique suite name, making duplicate detection explicit.

**Rule summary:**
- One test file per architectural element: `tests/unit/<element_name>_test.cpp`
- Each file declares `class <Element>Test : public <ComponentName>Test {};`
- All `TEST_F` macros in that file use the per-file subclass name
- No two test files share the same fixture subclass name
- Fixture headers belong in `tests/unit/*_test_fixture.h`, not inline in `.cpp` files

---

## Test Coverage Mapping

For each `req:` ID allocated to an `arch:`, produce at minimum:
1. **Success path test** — the normal/happy-path behavior specified by the requirement.
2. **Failure/error path test** — the error condition(s) from the requirement's `:verification_criteria:`.

---

## Calculator Example

Component: `libcalculator`. Covers `arch:libcalculator-adder`.

**Fixture** (`tests/unit/calculator_test_fixture.h`):

```cpp
#pragma once
#include <gtest/gtest.h>
#include "libcalculator/Calculator.h"

/*!
 * @brief Shared base fixture for Calculator unit tests.
 * @covers arch:libcalculator-adder
 */
class CalculatorTest : public ::testing::Test {
protected:
    libcalculator::Calculator calculator_;
};
```

**Test file** (`tests/unit/calculator_adder_test.cpp`):

```cpp
#include "calculator_test_fixture.h"

// Per-file fixture subclass — prevents GTest suite-name collisions.
class CalculatorAdderTest : public CalculatorTest {};

/*!
 * @brief Adding two non-overflowing integers returns their sum.
 *
 * @req    req:libcalculator-add-success
 * @covers arch:libcalculator-adder
 */
TEST_F(CalculatorAdderTest, AddTwoIntegersReturnsSum)
{
    // Arrange
    std::int32_t result{0};

    // Act
    const auto errorCode = calculator_.add(3, 4, result);

    // Assert
    EXPECT_FALSE(errorCode);
    EXPECT_EQ(result, 7);
}

/*!
 * @brief Adding INT32_MAX and 1 returns an arithmetic overflow error.
 *
 * @req    req:libcalculator-add-overflow-failure
 * @covers arch:libcalculator-adder
 *
 * @pre  Calculator is default-constructed.
 * @post result is unchanged on error.
 */
TEST_F(CalculatorAdderTest, AddOverflowReturnsError)
{
    FAIL() << "Not yet implemented — SWE.4 stub";
}
```
