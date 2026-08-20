---
name: 'SWE.3 Detailed Design'
description: 'Conventions for writing ASPICE SWE.3 detailed design artifacts as Doxygen-documented C++ header files in src/ for the E3 Software Platform. Applies to src/**/*.h and src/**/*.hpp files.'
applyTo: '**/src/**/*.{h,hpp}'
---

# ASPICE SWE.3 Detailed Design Format

SWE.3 **detailed design artifacts are C++ header files** in `src/`. There are no separate AsciiDoc files for SWE.3. The Doxygen documentation block above each class, struct, enum, and significant public method constitutes the formal SWE.3 design artifact.

---

## Copyright Header

Every `.h`, `.hpp`, and `.tpp` file must begin with the CARIAD copyright block before any other content (including include guards):

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

## Critical Rules

1. **Every class or struct that realizes an `arch:` must carry `@elaborates arch:<id>` in its Doxygen block.** This is the mandatory traceability link to SWE.2.
2. **Every method that relates to a `req:` must carry `@req req:<id>` in its Doxygen block.** When a method realizes multiple requirements, stack one `@req` tag per ID. A method without a `@req` tag is either trivially self-evident (e.g., a pure getter with no observable side-effect) or its traceability is missing; always verify before omitting. For any method with a non-trivial return type, at least one `@req` tag is mandatory. If a requirement applies to the class but not to a specific method, place the `@req` tag in the class-level Doxygen block. In addition, place `// @req req:<id>` inline comments in the `.cpp` file on the line before the code that fulfils the requirement. See `unit-construction.instructions.md` rule UC-08.
3. **`@elaborates` must reference the exact SWE.2 anchor ID.** Use `arch:<id>` for classes that are architectural elements (defined in `architecture.md`) and for shared data types, enums, `IFoo` interfaces, and cross-boundary error types (defined in `interfaces.md`). Internal helper structs need no `@elaborates`. Do not invent IDs.
4. **Do not copy black-box responsibility text from SWE.2 AsciiDoc into header `@details`.** The `@details` must describe the white-box design: internal data structures, POSIX functions chosen, algorithms, concurrency model.
5. **Do not write method implementations in headers — except for templates.** Non-template method bodies go in `.cpp` files. Template method definitions (and partial/explicit specializations that must be visible at instantiation) must be placed in a `.tpp` file that is `#include`d at the bottom of the `.h` file — never written inline in the `.h` itself. Pure template classes (all methods templated, no `.cpp` needed) use only the `.h` + `.tpp` pair. Mixed classes that have both non-template and template methods place non-template bodies in `.cpp` and template bodies in `.tpp`. The `.tpp` file must carry the same `#ifndef`/`#define`/`#endif` include guard as any other internal header (e.g., `SWP_<COMPONENT>_<CLASSNAME>_TPP`).
6. **Read `[#info:...-swe3-note]` blocks from `interfaces.adoc` before writing.** They contain POSIX function choices and design decisions that must be reflected in the header.
7. **Use traditional `#ifndef`/`#define`/`#endif` include guards — never `#pragma once`.** *(MISRA C++ 2023 19-0-2, AUTOSAR M16-0-1)* `#pragma once` is a non-standard compiler extension. Use `#ifndef SWP_<COMPONENT>_<CLASSNAME>_H` / `#define SWP_<COMPONENT>_<CLASSNAME>_H` / `#endif // SWP_<COMPONENT>_<CLASSNAME>_H`. The guard macro must be globally unique: prefix with the project abbreviation, component, and class name, all uppercase with underscores.
8. **Use C++14.** All types from the C++ standard library or POSIX. No platform-specific macros in public headers.
9. **Enclosing namespace must be `<project>::<component>`** (e.g., `swp::libipc`). Do not place types in the global namespace or in a component-unqualified namespace.
10. **`std::function` setter methods must accept the parameter by value and `std::move()` into storage.** Do not accept by `const std::function<>&` — that forces a copy and prevents storing move-only callables (e.g., lambdas capturing a `std::unique_ptr`).
11. **Document buffer sizing strategy in `@details` when a protocol maximum message size exists.** Prefer a fixed-size member array over a lazily-growing `std::vector` in event-loop hot paths — it eliminates heap allocation and the `catch(...)` block otherwise needed for `std::bad_alloc`.

---

## Doxygen Block Format

### Class Header Block

```cpp
/*!
 * @brief <One-sentence white-box description: what this class IS, not what it SHALL DO.>
 *
 * @details
 * <3–8 sentences describing the white-box design:>
 * <1. Internal data layout: member types, container choices (e.g., std::unordered_map<int, SegmentInfo>)>
 * <2. POSIX functions used (e.g., memfd_create, sendmsg with SCM_RIGHTS, poll(2))>
 * <3. Concurrency model (e.g., "all public methods are called from the event-loop thread; no internal locking")>
 * <4. Error-signaling strategy (e.g., "returns std::error_code; does not throw")>
 * <5. Lifetime and ownership semantics>
 *
 * @elaborates arch:<component>-<element-name>
 * @req req:<id> (only for class-level requirements not tied to a specific method)
 */
// Add `final` only for leaf classes that are never subclassed. Omit for polymorphic base classes.
class ClassName final {
public:
    explicit ClassName(<ConfigType> config);

    // Rule of Five: explicitly declare all five for any class owning a resource (fd, socket, memory).
    ~ClassName();
    ClassName(const ClassName&)            = delete;
    ClassName& operator=(const ClassName&) = delete;
    ClassName(ClassName&&)                 noexcept;
    ClassName& operator=(ClassName&&)      noexcept;

    /*!
     * @brief <One-sentence method description.>
     *
     * @param[in]  paramName  <Description of input parameter.>
     * @param[out] outParam   <Description of output parameter.>
     * @return <What is returned on success. std::error_code on failure; see error paths.>
     *
     * @req req:<id-1>
     * @req req:<id-2> (stack one @req per requirement the method realizes)
     *
     * @pre  <Precondition, e.g., "object must be initialised via init().">
     * @post <Postcondition, e.g., "fd is valid and mapped when return is success.">
     */
    std::error_code methodName(ParamType paramName, OutType& outParam) noexcept;

private:
    <ConfigType>  mConfig;   ///< Configuration used during initialisation.
    // ... private members with ///< inline Doxygen (prefix m, CamelCase) ...
};
```

### Struct / Data Type Block

```cpp
/*!
 * @brief <Description of the struct and its purpose.>
 *
 * @details
 * <Describe each field's semantic role, valid ranges, and lifetime.
 *  E.g., "fd is -1 when unset; must be closed by the owner when no longer needed.">
 *
 * @elaborates arch:<component>-<interface-name>
 */
struct TypeName {
    int    fd{-1};    ///< File descriptor; -1 means unset. (public struct fields: camelBack, no prefix)
    size_t size{0};   ///< Allocated size in bytes; 0 means unallocated.
};
```

### Enum Block

```cpp
/*!
 * @brief <Description of what this enum represents.>
 *
 * @elaborates arch:<component>-<interface-name>
 */
enum class ErrorCode : int {
    Success      = 0, ///< Operation succeeded.
    InvalidSize  = 1, ///< Requested size was zero or exceeded the per-segment limit.
    LimitReached = 2, ///< Maximum segment count per client has been reached.
};
```

---

## Abstraction Level Boundary — SWE.2 vs SWE.3

| Write this in SWE.3 headers (`@details`) | Do NOT repeat from SWE.2 AsciiDoc |
|---|---|
| `"uses memfd_create(name, MFD_CLOEXEC)"` | `"provides anonymous shared memory regions"` |
| `"stores segment metadata in std::unordered_map<int, SegmentInfo>"` | `"tracks active segment metadata"` |
| `"sends FD via sendmsg with SCM_RIGHTS ancillary data"` | `"transfers file descriptors to clients over the IPC channel"` |
| `"accept() returns EAGAIN/EWOULDBLOCK in non-blocking mode"` | `"accepts incoming client connections"` |
| `"uses poll(2) with POLLIN on the listen socket fd"` | `"monitors the UDS socket for new connections"` |
| `"each client tracked by its connected fd in a std::unordered_map"` | `"manages per-client connection state"` |

---

## File Header

Every `.h` file must begin with:

```cpp
#ifndef SWP_<COMPONENT>_<CLASSNAME>_H
#define SWP_<COMPONENT>_<CLASSNAME>_H

// =============================================================================
// SWE.3 Detailed Design: <ClassName>
// Elaborates: arch:<component>-<element-name>
// Component:  <component-name>
// =============================================================================
```

And end with:

```cpp
#endif // SWP_<COMPONENT>_<CLASSNAME>_H
```

---

## Template Definition File (`.tpp`)

When a class has template methods, place their definitions in a `.tpp` file `#include`d at the bottom of the `.h`, just before the `#endif` guard. The `.tpp` carries its own include guard.

```cpp
#ifndef SWP_<COMPONENT>_<CLASSNAME>_TPP
#define SWP_<COMPONENT>_<CLASSNAME>_TPP

// <ClassName>.tpp — Template definitions for <ClassName>
// Elaborates: arch:<component>-<element-name>

namespace <project>::<component> {

template <typename T>
std::error_code ClassName::methodName(T param) noexcept
{
    // implementation
    return std::error_code{};
}

} // namespace <project>::<component>

#endif // SWP_<COMPONENT>_<CLASSNAME>_TPP
```

Include at the bottom of the `.h`:

```cpp
    // ... end of class declaration ...
};

} // namespace <project>::<component>

#include "<ClassName>.tpp"

#endif // SWP_<COMPONENT>_<CLASSNAME>_H
```

---

## Fail Conditions (GR-06)

Before writing any header file, verify the following prerequisites exist. If any condition fails, **HALT** and report the gap to the user. Do not proceed, guess, or invent content.

| Condition | Required artifact | Action on absence |
|-----------|-------------------|-------------------|
| Architecture document exists | `doc/<component>/component_architecture/architecture.md` with at least one `arch:` anchor | HALT: report missing architecture document |
| Interfaces document exists | `doc/<component>/component_architecture/interfaces.md` with at least one `arch:` anchor | HALT: report missing interfaces document |
| Target `arch:` ID is valid | The `arch:<id>` referenced by the class exists in `architecture.md` | HALT: report unknown element ID |

---

## Self-Check Before Writing

- [ ] `@elaborates arch:<id>` present and matches an exact anchor in `doc/<component>/component_architecture/`
- [ ] Every non-trivial method has `@req req:<id>` in its Doxygen block; class-level requirements use `@req` in the class Doxygen block
- [ ] Corresponding `// @req req:<id>` inline comments are present in the `.cpp` file before the implementing code
- [ ] `@details` describes white-box design (data structures, POSIX calls, concurrency), not black-box responsibility
- [ ] All non-trivial public methods have `@brief` and `@return`
- [ ] No non-template method implementations in the header (template definitions go in a `.tpp` file `#include`d at the bottom of the `.h`; the `.tpp` carries its own `#ifndef`/`#define`/`#endif` guard)
- [ ] Include guard present (`#ifndef SWP_<COMPONENT>_<CLASSNAME>_H` / `#define` / `#endif`) — do not use `#pragma once`
- [ ] Namespace is `<project>::<component>`
- [ ] CP10 naming conventions followed — load `.github/instructions/cpp-naming-conventions.instructions.md` for the full rules
- [ ] No Parasoft violations — load `.github/skills/parasoft-vwos-ruleset/SKILL.md` for the full ruleset
