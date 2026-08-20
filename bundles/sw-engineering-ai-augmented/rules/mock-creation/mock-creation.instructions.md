---
name: 'Mock Creation'
description: 'Rules for creating GMock headers and wiring them in tests/unit/mocks/. Used by the Software Implementer (Stage 1) to create MockFoo from IFoo interfaces defined in src/ by the Software Designer.'
applyTo: '**/tests/unit/mocks/**'
---

# Mock Creation Rules

Mocks live in `tests/unit/mocks/`. Each mock implements one injectable interface (`IFoo`) from `src/`. Never add mocks to `src/`.

---

## Folder Layout

```
tests/unit/mocks/
  CMakeLists.txt           ← INTERFACE library target
  Mock<Foo>.h      ← one file per IFoo interface
```

---

## GMock Header Pattern

```cpp
#ifndef SWP_<COMPONENT>_MOCK_<FOO>_H
#define SWP_<COMPONENT>_MOCK_<FOO>_H

// Mock<Foo>.h — GMock for I<Foo>

#include <gmock/gmock.h>
#include "<component>/I<Foo>.h"

namespace <project>::<component> {

class Mock<Foo> : public I<Foo> {
public:
    MOCK_METHOD(std::error_code, <operation>, (<params>), (noexcept, override));
};

} // namespace <project>::<component>

#endif // SWP_<COMPONENT>_MOCK_<FOO>_H
```

---

## CMakeLists.txt

```cmake
add_library(${TARGET_NAME}_mocks INTERFACE)
target_include_directories(${TARGET_NAME}_mocks INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(${TARGET_NAME}_mocks INTERFACE gmock)
```

Link in `tests/unit/CMakeLists.txt`:

```cmake
target_link_libraries(${TARGET_NAME}_gtest PRIVATE ${TARGET_NAME}_mocks)
```

---

## Rules

1. One `Mock<Foo>.h` per `IFoo` interface. No combined mock headers.
2. Use `MOCK_METHOD` (GMock v3+ syntax) — not deprecated `MOCK_METHOD0`/`MOCK_METHOD1`.
3. Specify `(noexcept, override)` when the interface method declares `noexcept`.
4. Inherit only from `IFoo` — never from concrete classes.
5. The `CMakeLists.txt` target is `INTERFACE` — no `.cpp` or `.a` produced.

---

## Self-Check

- [ ] One mock per interface, located in `tests/unit/mocks/`
- [ ] Uses `MOCK_METHOD` syntax with correct specifiers
- [ ] `CMakeLists.txt` declares `INTERFACE` library and links `gmock`
- [ ] `tests/unit/CMakeLists.txt` links `${TARGET_NAME}_mocks`
