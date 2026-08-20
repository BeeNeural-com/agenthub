---
name: 'Testability Design'
description: 'Rules for writing injectable-interface headers in src/ to enable unit testing without real OS or platform dependencies. Applied by the Software Designer alongside detailed-design.instructions.md.'
applyTo: '**/src/**/*.{h,hpp}'
---

# Testability Design Rules

Only classes that are **injected as dependencies into other classes**, or that cross a **public component boundary**, need a pure abstract interface (`IFoo`). Internal implementation classes that nothing else depends on directly do not need one.

---

## When to Define an `IFoo` Interface

| Case | Interface needed? |
|---|---|
| Class is injected into another class as a dependency | Yes: `IFoo` + GMock |
| Class is part of the public API (crosses component boundary) | Yes: `IFoo` + GMock |
| Class is stored by value in a fixed-size container (vtable not allowed) | Yes: template injection + GMock (no `IFoo` header needed) |
| Class is an internal helper used only within a single `.cpp` | No |
| Class is a pure data holder (struct/value type) | No |
| Dependency is a POSIX syscall or C-ABI free function | No: use Link Seam instead |

---

## Rules

1. **Abstract interface per injected dependency.** For each class that is injected into another, define a pure abstract `IFoo` interface in its own header (`I<Foo>.h`).
2. **Constructor injection only.** Accept the dependency as `I<Foo>&` or `std::unique_ptr<I<Foo>>` in the constructor. Never via setters or static accessors.
3. **No static or global state in public headers.** No `static` data members that hold OS handles, singletons, or callbacks.
4. **`IFoo` belongs in `src/`.** It is a production type, not a test artifact. The mock (`MockFoo`) lives in `tests/unit/mocks/`.
5. **`IFoo` carries `@req` tags** for any requirement it satisfies. Add `@elaborates arch:<id>` only when the interface is an explicit `arch:` element in `interfaces.md`.
6. **No `std::function` ops tables in production headers.** Do not store `std::function` fields as operation injection points. `std::function` heap-allocates for non-trivial callables and cannot be declared `noexcept`. Use template injection or IFoo instead.

---

## Pattern Selection

Three patterns cover all mocking scenarios. For worked code templates, load the `cpp-mocking-strategies` skill.

| Pattern | When to use | Key invariant |
|---|---|---|
| **IFoo + GMock** | Dependency injected as reference/pointer | `IFoo` in `src/`; mock inherits from `IFoo` with identical signatures |
| **Template injection** | Collaborator stored by value (vtable not allowed) | Fake struct mirrors exact public methods of the real type (same names, signatures, `noexcept`) |
| **Link Seam** | POSIX syscall or C-ABI free function with exactly one production implementation | Named wrapper namespace in `src/<component>/<host>_posix.h`; production calls wrapper, never raw `::syscall()` directly |

### Pattern-Specific Constraints

**IFoo + GMock:**
- Define `I<Foo>` with the exact method signatures of the real class.
- The mock inherits only from `I<Foo>` and uses `MOCK_METHOD` for each virtual method.
- `IFoo` header in `src/`; `MockFoo` header in `tests/unit/mocks/`.

**Template injection:**
- Host class becomes a template on the collaborator type; default template argument is the real type.
- Variant A (array-slot): host owns a `std::array<TSlot, N>` pool.
- Variant B (reference-injection): host stores `TOps&` supplied at construction.

**Link Seam:**
- Wrap each syscall in a named function inside a dedicated `posix` namespace.
- Header (`<host>_posix.h`) declares wrappers; production `.cpp` calls the real syscall; test `.cpp` uses `std::function` spies.
- CMake wires real `.cpp` into the production library, mock `.cpp` into the test binary (not both).
- Spy globals must be reset in `TearDown()`.

---

## Self-Check

- [ ] Every injected C++ collaborator has a matching `IFoo` header in `src/`
- [ ] Constructor accepts `IFoo&` or `std::unique_ptr<IFoo>`; no setters or globals
- [ ] Value-member collaborators use template injection; no forced heap allocation for vtable
- [ ] No `std::function` fields used as ops injection points in production headers
- [ ] Every POSIX syscall dependency uses a link seam, not an `IFoo`
- [ ] Seam wrappers declared in `<host>_posix.h` and live in `src/<component>/`; mock `.cpp` files in `tests/unit/seams/`
- [ ] Production class calls `posix::<c_function>()`; never `::syscall()` directly
- [ ] Spy globals are reset in `TearDown()`
- [ ] No static data members holding OS handles
- [ ] `IFoo` header is in `src/`, not in `tests/`
