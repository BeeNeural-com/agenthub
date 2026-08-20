---
name: 'SWE.3 Unit Construction'
description: 'Conventions for implementing C++ source files (*.cpp) as SWE.3 unit construction artifacts for the E3 Software Platform. Applies to src/**/*.cpp files.'
applyTo: '**/src/**/*.cpp'
---

# ASPICE SWE.3 Unit Construction Format

SWE.3 unit construction artifacts are C++ `.cpp` files in `src/`. They implement the interfaces declared in the corresponding SWE.3 `.h` design files. **The `.h` file carries the SWE.3 design documentation. The `.cpp` file contains the implementation only.**

---

## Copyright Header

Every `.cpp` file must begin with the CARIAD copyright block as the very first content:

```cpp
//
// (c) 2022 CARIAD SE, All rights reserved.
//
// NOTICE:
// All the information and materials contained herein, including the intellectual and technical concepts, are the
// property of CARIAD SE and may be covered by patents, patents in process, and are protected by trade secret and/or
// copyright law. The copyright notice above does not evidence any actual or intended publication or disclosure of this
// source code, which includes information and materials that are confidential and/or proprietary and trade secrets of
// CARIAD SE. Any reproduction, dissemination, modification, distribution, public performance, public display of or any
// other use of this source code and/or any other information and/or material contained herein without the prior written
// consent of CARIAD SE is strictly prohibited and in violation of applicable laws. The receipt or possession of this
// source code and/or related information does not convey or imply any rights to reproduce, disclose or distribute its
// contents or to manufacture, use or sell anything that it may describe in whole or in part.
//
```

---

## Priority Rules (most-violated, check first)

- **UC-06** No bare `return {};` — name the type explicitly
- **UC-13** No helper structs inside function bodies — define at file scope
- **UC-04 + UC-10** Every new `.cpp` added to `SRC_FILES` in both CMake files
- **UC-22** Shared helper types go in a header, not duplicated across `.cpp` files
- **UC-34** Function length: target 30-40 lines, split above 100
- **UC-33** Prefer stack over heap when capacity is compile-time known
- **UC-21** Every non-success `return` preceded by a `Logger::` call
- **UC-12** First `#include` must be the corresponding `.h`

---

## Rules

### Traceability and File Structure

1. **[UC-01] Every `.cpp` must correspond to a `.h` with an `@elaborates arch:<id>` tag.** An orphaned `.cpp` without a SWE.3-documented header violates traceability.
2. **[UC-02] Apply coding principles CP01–CP09.** See `doc/coding_principles.adoc` for the full list.
3. **[UC-03] Include the mandatory file-level comment block** referencing the `.h` and `arch:` ID.
8. **[UC-08] Inline `// @req req:<id>` comments are mandatory** on the line immediately before the code that implements each requirement. In addition, the corresponding method Doxygen block in the `.h` file must carry `@req req:<id>` tags (see `detailed-design.instructions.md` rule 2). Place one comment per requirement; stack multiple comments on consecutive lines when a single code block satisfies several requirements.
9. **[UC-09] No design documentation in `.cpp` files.** Design belongs in the `.h` Doxygen blocks. Implementation comments (`// why`, not `// what`) are encouraged.
12. **[UC-12] Include ordering:** The first `#include` in every `.cpp` must be its own corresponding `.h`. This guarantees the header is self-contained and does not silently depend on transitive includes.

### Build Registration

4. **[UC-04] Every new `.cpp` must be added to `SRC_FILES` in `src/CMakeLists.txt` immediately.** Forgetting this is a hard build failure (anti-pattern documented in project conventions).

### Error Handling and Logging

5. **[UC-05] Every `std::error_code` return path must be implemented.** No silent `return {}` where an error condition is possible.
6. **[UC-06] Always return an explicit type — never bare `return {}`.** Every `return` statement must name the type being returned. Write `return std::error_code{};` not `return {};`, `return false;` not `return {};`, `return 0;` not `return {};`. This applies to every return in every function — success paths, no-op early-outs, and error paths alike. Bare `return {}` is ambiguous at a glance and masks the intended type from reviewers and static analysis.
20. **[UC-20] Classify every error branch explicitly.** After every syscall that can fail, the error path must be classified as: (a) ignore — with a comment explaining why it is safe, (b) log and continue, or (c) return an error code. Silent fallthrough with no comment is a quality gap.
21. **[UC-21] Log at the level matching the condition; use concise domain prose.** Every non-success `return` must be preceded by a `Logger::logError()` or `Logger::logWarning()` call. Important lifecycle transitions (connect, disconnect, start, shutdown) use `Logger::logInfo()`. Success-path operational detail (bytes sent, poll results) uses `Logger::logDebug()`. Log messages must not expose implementation details such as namespace or method names. Include key parameters when they aid diagnosis. The only exception to mandatory error logging is a documented silent no-op where the inactive state is a valid precondition.
35. **[UC-35] Prefer non-throwing I/O; contain unavoidable throwing calls at the boundary.** *(CP03/CP04)* Do not use `std::cout` or `std::cerr` directly in production code — prefer `::write()` or `::fprintf(stderr, …)`, which do not throw and do not require heap allocation. If a throwing I/O API (e.g. `std::cerr` with exceptions enabled, a third-party stream) must be used, wrap the call in a `catch (...)` block at that boundary, translate or silently swallow the exception, and never re-throw. `try`/`catch` blocks are permitted only at these integration boundaries — never as general control-flow. See CP03 and CP04 in `doc/coding_principles.adoc`.

### Resource Management

7. **[UC-07] Use RAII for all resources.** File descriptors must be managed with guard types. No naked `close()` calls except inside destructors or RAII guards.
11. **[UC-11] No raw `new`/`delete`.** Use RAII types (`std::unique_ptr`, stack allocation, custom guards) consistent with C++14.
33. **[UC-33] Prefer stack over heap; avoid runtime allocation.** *(R5)* Allocate at compile time by default. Use `std::array`, fixed-size member arrays, or stack-local objects wherever the capacity is known at compile time. Reach for `std::vector`, `std::string`, `new`, or other heap-allocating constructs **only** when the size is genuinely unknown until runtime and cannot be bounded by a compile-time constant.

### Code Organization

13. **[UC-13] Never define helper structs inside a function body.** RAII guards and other local helper types must be defined at file scope (anonymous namespace if internal). Local structs inside functions are not reusable across the translation unit and make function bodies harder to read.
14. **[UC-14] Assign state member variables immediately after the operation they reflect.** Do not defer state assignments past unrelated subsequent steps — if a later step fails, the object must not hold partially-applied state that violates its invariant.
15. **[UC-15] No artificial block scopes.** Do not introduce bare `{}` blocks unless they control the lifetime of a scoped RAII object. A scope with no local variable needing controlled destruction adds noise.
22. **[UC-22] Any struct or class needed by more than one `.cpp` file must be declared in a header.** File-scope anonymous-namespace types are for single-translation-unit use only. Extract shared helper types to a named header in the component directory; place them in the component namespace, not an anonymous namespace.
23. **[UC-23] Reduce branching where possible.** Prefer early-return (guard clause) over nested `if/else` chains. Eliminate branches that can be replaced with arithmetic, a ternary, a lookup table, or a predicate. Never introduce a branch whose sole effect is to execute code that is unconditionally correct without it. Acceptable branch-reduction techniques include: collapsing symmetric `if/else` return paths into a single `return expr;`; replacing a boolean flag set in two branches with direct assignment of the condition; and lifting precondition checks to the top of the function so the happy path has no indentation. Do not force reduction at the cost of readability — if a technique makes the intent less clear, keep the explicit branch.
34. **[UC-34] Function length and placement.** *(R6)* Target 30–40 lines per function body. 50–100 lines is a warning zone — consider splitting. Above 100 lines is a red flag — extract cohesive sub-tasks into well-named helpers before committing. Helpers used exclusively by one class **must** be declared as `private` methods of that class, not as free functions or anonymous-namespace helpers; if the header is read-only, raise a design-change request to the Software Designer to add the private declarations first. Helpers shared by two or more classes may live in an anonymous namespace or a dedicated internal header.

### Runtime Safety

16. **[UC-16] Guard every `std::function` callback before invocation.** Always check `if (mCallback)` before calling. An unset callback is a programming error — log at error level and skip. Never risk aborting with `std::bad_function_call`.
17. **[UC-17] Use `reserve()` not `resize()` for pre-allocation without initialization.** `resize()` default-initializes elements; `reserve()` does not. When a buffer will be immediately overwritten, use `reserve()`. Use `resize()` only when default-initialized values are meaningful.
18. **[UC-18] Pre-allocate buffers to their maximum size at construction.** Buffers with a known protocol-bounded maximum must be sized at construction, not grown lazily in event-processing paths. Lazy growth requires `try`/`catch` which violates the no-throw rule (CP04).
19. **[UC-19] After `poll()`, guard each fd subsection on `revents` before any syscall.** Never call `accept()`, `read()`, or `write()` without first confirming `poll()` reported an event on that fd.

### AUTOSAR and MISRA Compliance

24. **[UC-24] Non-POD types must be defined as `class`, not `struct`.** *(AUTOSAR A11-0-1)* Use `struct` only for passive data aggregates with no invariants, no private members, and no user-defined constructors. Any type with private members, constructors, or non-trivial semantics must be `class`.
25. **[UC-25] Pointer arithmetic is forbidden — use array indexing only.** *(AUTOSAR M5-0-15)* Never apply `+`, `-`, `++`, `--`, or `+=` directly to a pointer. Access elements exclusively via `ptr[i]` or, preferably, a range-based container. This prevents out-of-bounds arithmetic that static analysis cannot always detect.
26. **[UC-26] Prefer delegating constructors to eliminate duplicated initialisation logic.** *(AUTOSAR A12-1-5)* When two or more constructors share the same member initialisation sequence, have the secondary constructors delegate to a single primary constructor via `: ClassName(…)` in the member-initialiser list. Never copy-paste initialiser lists across constructors.
27. **[UC-27] No macros in headers — use `inline`/`constexpr`/`enum class` instead.** *(MISRA C++ 2023 19-0-2, MISRA C 2012 Dir 4.9, CERT PRE00-C)* `#define` macros in `.h` files leak into every translation unit that includes the header, bypass type checking, and pollute the global namespace. Replace object-like macros with `constexpr` variables, function-like macros with `inline` or `constexpr` functions, and flag-sets with `enum class`. The same applies in `.cpp` files.
28. **[UC-28] Public functions must not return non-`const` handles to internal data.** *(AUTOSAR A9-3-1)* Returning a non-`const` pointer or non-`const` reference to a private or protected member breaks encapsulation: callers can mutate state the class cannot observe or validate. Return by value, return a `const` reference, or expose a dedicated mutating method instead.
29. **[UC-29] `friend` declarations are forbidden.** *(AUTOSAR A11-3-1)* `friend` breaks encapsulation by granting external classes or functions direct access to private members. Refactor to use the public or protected interface; if truly necessary, introduce a dedicated accessor method.
30. **[UC-30] Do not overload functions on forwarding references (`T&&`) together with other overloads.** *(AUTOSAR A13-3-1)* A forwarding-reference overload matches almost any argument and silently hijacks calls intended for more specific overloads, including copy/move constructors. Prefer explicit named parameters, `std::enable_if` constraints, or a non-template overload set instead.
31. **[UC-31] No implicit conversions.** *(MISRA C++ 2023 15-1-3)* All conversions between arithmetic types, pointer types, or user-defined types must be explicit (`static_cast<>`, a named constructor, or a named conversion function). Implicit narrowing, sign-change, or bool-to-int conversions are a common source of silent bugs and are flagged by static analysis.
32. **[UC-32] Make member functions `static` when they do not access instance state.** *(AUTOSAR M9-3-3)* A member function that does not read or write any non-`static` data member or call any non-`static` member function must be declared `static`. This makes the independence from instance state explicit and allows the compiler to enforce it.

---

## File-Level Comment Block

Every `.cpp` file must begin with:

```cpp
// <ClassName>.cpp — SWE.3 Unit Construction
// Implements: <ClassName> as declared in <ClassName>.h
// Elaborates: arch:<component>-<element-name>
// See also: .github/instructions/detailed-design.instructions.md
```

---

## SRC_FILES Update Rule

When creating a new `<name>.cpp`, immediately add it to `SRC_FILES` in `src/CMakeLists.txt`:

```cmake
set(SRC_FILES
    # ... existing entries ...
    <name>.cpp   # SWE.3: arch:<component>-<element-name>
)
```

The trailing comment is mandatory: it provides CMake-level traceability to the SWE.2 element.

---

## Implementation Pattern

```cpp
// <ClassName>.cpp — SWE.3 Unit Construction
// Implements: <ClassName> as declared in <ClassName>.h
// Elaborates: arch:<component>-<element-name>

#include "<ClassName>.h"

#include <cerrno>
#include <sys/mman.h>
#include <unistd.h>

namespace <project>::<component> {

<ClassName>::<ClassName>(<ConfigType> config) noexcept
    : mConfig{std::move(config)}
{
}

std::error_code <ClassName>::<methodName>(size_t requestedSize, int& fdOut) noexcept
{
    // @req req:<component>-<requirement-id>
    if (requestedSize == 0 || requestedSize > config_.maxSegmentSize) {
        return std::make_error_code(std::errc::invalid_argument);
    }

    // ... implementation ...
    return std::error_code{};
}

} // namespace <project>::<component>
```

---

## Error Path Convention

Every error branch must:
1. Return a meaningful `std::error_code` (use `std::errc` values where applicable, or a custom error category).
2. Be preceded by a `// @req req:<id>` comment identifying which requirement the error path satisfies.
3. Leave all output parameters in their initial/unset state (e.g., `fd` stays `-1` on failure).


