---
name: unit-construction
description: "Use when writing or reviewing SWE.3 C++ .cpp implementation files in src/. Provides the mandatory file-level comment block format, CP01-CP13 coding principle patterns, clang-tidy naming rules, SRC_FILES registration, and a worked Calculator example."
---

# SWE.3 Unit Construction Skill

This skill covers the implementation side of SWE.3: writing `src/**/*.cpp` files that fulfil the declarations in `@elaborates`-tagged headers. The `.h` file owns all design documentation; the `.cpp` file contains implementation only.

---

## Overview

| Artifact             | Location                          | Owns                                                            |
| -------------------- | --------------------------------- | --------------------------------------------------------------- |
| SWE.3 header         | `src/<component>/<ClassName>.h`   | Doxygen design docs, `@elaborates`, `@req`, `@pre`/`@post`      |
| SWE.3 implementation | `src/<component>/<ClassName>.cpp` | Logic, `// req:<id>:` inline comments, file-level comment block |

**Before writing any `.cpp`**: verify `doc/coding_principles.md` exists. Without it, ASPICE BP3 (RL.2) cannot be assessed — halt and flag CRITICAL if absent.

---

## Reference / API

### Coding Principles Checklist (CP01–CP13)

| Principle | Rule                                                                                                                                                     | Enforcement                                                                       |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| CP01      | RAII for all POSIX file descriptors and handles                                                                                                          | No naked `close()` except in destructors                                          |
| CP02      | No raw `new`/`delete`                                                                                                                                    | Use `std::unique_ptr`, stack allocation, or RAII guards                           |
| CP03      | `std::error_code` on all error paths; no `throw`                                                                                                         | `catch` only at external integration boundaries, translating to `std::error_code` |
| CP04      | No `throw` expressions anywhere                                                                                                                          | `noexcept` on all methods without external throwing calls                         |
| CP05      | `// req:<id>:` inline comment on every branch realising a SWE.1 requirement                                                                              | Guards, error returns, and state transitions                                      |
| CP06      | No Doxygen blocks in `.cpp`                                                                                                                              | Design lives in `.h`; `.cpp` has implementation comments only                     |
| CP07      | Mandatory file-level comment block                                                                                                                       | See format below                                                                  |
| CP08      | Register every new `.cpp` in `SRC_FILES`                                                                                                                 | `src/CMakeLists.txt`                                                              |
| CP09      | Log levels: fatal=break-of-functionality, error=recoverable, warning=unexpected non-critical, info=non-repetitive main paths, debug=details, verbose=all | —                                                                                 |
| CP10      | `m`-prefix `CamelCase` for private/protected members; `camelBack` for locals/params; `k`-prefix for static constants; no trailing underscores            | `.clang-tidy` enforced                                                            |
| CP11      | Keep `src/CMakeLists.txt` as the single build file                                                                                                       | All source registration in one place                                              |
| CP12      | Inline comment on every branch comparing against an external API constant (POSIX errno, socket flags)                                                    | Names the constant and states the handling intent                                 |
| CP13      | Emit at minimum `warning`-level log before every non-success return in POSIX I/O wrappers                                                                | Ensures raw system condition is always recorded                                   |

### CP10 Naming — Common Expansions

| Abbreviation    | Required expansion                        |
| --------------- | ----------------------------------------- |
| `fd` (bare)     | contextual: `socketFd`, `acceptorFd`      |
| `buf`           | `buffer`                                  |
| `n`             | `bytesReceived`, `bytesSent`, `byteCount` |
| `tmp`           | contextual: `savedFd`, `savedErrorNumber` |
| `ptr`           | `Pointer` suffix: `writePointer`          |
| `errno`/`Errno` | `errorNumber`/`ErrorNumber`               |
| `addr`          | `address`                                 |
| `fds` / `pfd`   | `pollDescriptors` / `pollDescriptor`      |

### File-Level Comment Block (CP07)

```cpp
// <ClassName>.cpp — SWE.3 Unit Construction
// Implements: <ClassName> as declared in <ClassName>.h
// Elaborates: arch:<component>-<element-name>
```

### SRC_FILES Entry (CP08 + CP11)

```cmake
set(SRC_FILES
    # ... existing entries ...
    <component>/<ClassName>.cpp   # SWE.3: arch:<component>-<element-name>
)
```

Add the line to `src/CMakeLists.txt`.

---

## Lifecycle & Usage Pattern

1. Confirm the matching `.h` file has `@elaborates arch:<id>` and all method declarations.
2. Confirm `doc/coding_principles.md` exists.
3. Create the `.cpp` with the CP07 file-level comment block.
4. Implement all methods declared in the header.
5. Add `// req:<id>:` inline comments on every branch realising a SWE.1 requirement (CP05).
6. Add the `.cpp` to `SRC_FILES` in both CMake files with a trailing `arch:` comment (CP08, CP11).
7. Run `./build.sh --docker clang-tidy` — zero findings expected.
8. Run `./build.sh --docker clang-format` — zero diff expected.

---

## Examples

### Calculator — `src/libcalculator/Calculator.cpp`

The header (`Calculator.h`) declares `Calculator::add()` with `@elaborates arch:libcalculator-adder`. The `.cpp` below implements it applying CP05–CP10.

```cpp
// Calculator.cpp — SWE.3 Unit Construction
// Implements: Calculator as declared in Calculator.h
// Elaborates: arch:libcalculator-adder

#include "libcalculator/Calculator.h"

#include <cerrno>
#include <climits>
#include <system_error>

namespace libcalculator {

std::error_code Calculator::add(
    std::int32_t firstOperand,
    std::int32_t secondOperand,
    std::int32_t& result) const noexcept
{
    // req:libcalculator-add-overflow-failure: detect overflow before computation
    // to avoid undefined behavior on signed integer overflow.
    if (firstOperand > 0 && secondOperand > (INT32_MAX - firstOperand)) {
        return std::make_error_code(std::errc::value_too_large);
    }
    if (firstOperand < 0 && secondOperand < (INT32_MIN - firstOperand)) {
        return std::make_error_code(std::errc::value_too_large);
    }

    // req:libcalculator-add-success: operands are within range — compute and return.
    result = firstOperand + secondOperand;
    return {};
}

} // namespace libcalculator
```

### SRC_FILES registration

```cmake
set(SRC_FILES
    main.cpp
    libcalculator/Calculator.cpp   # SWE.3: arch:libcalculator-adder
)
```

Apply to `src/CMakeLists.txt`.

---

## Best Practices / Anti-patterns

| Anti-pattern                           | Correct                                                                      |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| `int fd_` (trailing underscore)        | `int mSocketFd` (m-prefix CamelCase)                                         |
| `int fd` (bare abbreviation)           | `int socketFd` (contextual name)                                             |
| `int n = recv(...)`                    | `const ssize_t bytesReceived = recv(...)`                                    |
| `int tmp = errno`                      | `const int savedErrorNumber = errno`                                         |
| Doxygen `/*!` block in `.cpp`          | Move all doc to `.h`; use `// why` comments in `.cpp`                        |
| `close(fd)` inline in method body      | Wrap in RAII guard; destructor calls `close()`                               |
| Error return with no `// req:` comment | Add `// req:<id>:` before the guard condition                                |
| Missing `SRC_FILES` entry              | Add to `src/CMakeLists.txt` immediately                                      |
| `if (errno == EAGAIN)` with no comment | `if (errno == EAGAIN) // EAGAIN: no data ready — non-blocking, return empty` |

---

## Self-Check Before Finalising

- [ ] `doc/coding_principles.md` exists (ASPICE BP3 RL.2)
- [ ] CP07 file-level comment block present with correct `arch:` ID
- [ ] All methods declared in `.h` are implemented
- [ ] Every error branch has a `// req:<id>:` inline comment (CP05)
- [ ] No Doxygen `/*!` or `///` doc blocks in `.cpp` (CP06)
- [ ] All private member accesses use `m`-prefix CamelCase — zero trailing underscores (CP10)
- [ ] All locals/params use full descriptive `camelBack` names — no `fd`, `buf`, `n`, `tmp`, `addr` (CP10)
- [ ] All POSIX resources wrapped in RAII — no leaked file descriptors on error paths (CP01)
- [ ] No raw `new`/`delete` (CP02)
- [ ] No `throw` expressions; `noexcept` on all applicable methods (CP03, CP04)
- [ ] `SRC_FILES` updated in both CMake files with trailing `arch:` comment (CP08, CP11)
- [ ] `./build.sh --docker clang-tidy` — zero findings
- [ ] `./build.sh --docker clang-format` — zero diff
