---
name: 'SWE.4 Unit Test Stub'
description: 'Format rules for writing Doxygen spec blocks and FAIL() stubs above TEST_F macros in tests/unit/**/*.cpp. Used by the Software Designer.'
applyTo: '**/tests/unit/**/*.cpp'
---

# SWE.4 Unit Test Stub Format

Spec blocks and stubs are the Software Designer's output. They define what each test must verify, traceable to requirements and design elements, before any implementation begins.

---

## Critical Rules

1. Every `TEST_F` or `TEST` must have a `/*!` Doxygen block immediately above it.
2. Every spec block must have `@req req:<id>` and `@covers arch:<id>`.
3. `@brief` must describe the tested behavior in indicative mood — not "Test that…" or "Check that…".
4. Stub bodies use `FAIL() << "Not yet implemented — SWE.4 stub"`. Never leave empty bodies.
5. `@covers` must reference an `@elaborates` ID that exists in `src/*.h`.
6. Never invent `req:` or `arch:` IDs — read them from actual source files.
7. Write both success-path and failure-path stubs for every functional requirement.

---

## Spec Block Format

```cpp
/*!
 * @brief <Behavior statement in indicative mood.>
 *
 * @req     req:<component>-<requirement-id>
 * @covers  arch:<component>-<element-name>
 *
 * @pre  <Precondition.>
 * @post <Expected postcondition.>
 */
TEST_F(FixtureName, UnitUnderTestTestedBehavior)
{
    FAIL() << "Not yet implemented — SWE.4 stub";
}
```

---

## Test Naming Convention

`TEST_F(<ComponentFixture>, <UnitUnderTest><TestedBehavior>)`

Examples:
- `TEST_F(ResourceManagerTest, AllocateInvalidSizeReturnsInvalidArgument)`
- `TEST_F(ConnectionHandlerTest, DisconnectReleasesAllResources)`

---

## File Header

```cpp
// <element_name>_test.cpp — SWE.4 Unit Test Stubs
// Unit under test: <ClassName> (src/<element_name>.h)
// Elaborates:      arch:<component>-<element-name>

#include "<ComponentName>_test_fixture.h"
#include "<element_name>.h"
```

---

## Per-file Fixture Subclass

Each test file declares its own subclass to avoid `TEST_F` name collisions:

```cpp
class <Element>Test : public <ComponentName>Test {};
```

---

## Self-Check Before Submitting Stubs

- [ ] Every `TEST_F`/`TEST` has `/*!` block with `@req`, `@covers`, `@brief`
- [ ] `@brief` uses indicative mood
- [ ] Both success and failure paths stubbed for each requirement
- [ ] `FAIL()` message present — no empty bodies
- [ ] All `req:` and `arch:` IDs verified against existing files
- [ ] Per-file fixture subclass declared
