---
name: cpp-mocking-strategies
description: "Use when deciding how to mock C++ dependencies for unit tests. Covers five techniques — IFoo+GMock, template policy injection (member, EBO, dual-constructor), link-seam TU substitution — with decision table, clang-format-compliant patterns, and worked examples. Use during SWE.3 testability design or Software Implementer Stage 1."
---

# C++ Mocking Strategies Skill

Provides the classification rule and worked examples for selecting the correct mocking technique for each category of C++ dependency. Used by the Software Designer when performing testability design (SWE.3 Stage 1) and by the Software Implementer when creating mock headers and link-seam stubs.

---

## Overview

Five patterns cover all mocking scenarios in a C++ POSIX codebase. The primary decision is one question: **Does this dependency have multiple meaningful production implementations?**

- **Yes** → IFoo+GMock (injected reference) or template injection (value-member / fixed-size container).
- **No** → Link seam (TU substitution).

The `std::function` ops-table pattern exists but is not appropriate for embedded or real-time code.

---

## Reference / API

### Classification Decision Table

| Dependency type | Multiple prod. implementations? | Technique |
|---|---|---|
| C++ class injected as collaborator | Yes | IFoo + GMock |
| C++ class stored by value (stateful, needs call recording) | Yes | Template injection — member reference variant |
| C++ class stored by value (stateless ops, no recording needed) | Yes | Template injection — EBO / `[[no_unique_address]]` variant |
| C++ class stored by value (production 0-arg, test stateful spy) | Yes | Template injection — dual-constructor variant |
| POSIX syscall (`socket`, `bind`, `listen`, `accept`, `connect`, `poll`, `recv`, `send`, `close`, `unlink`) | No | Link seam (TU substitution) |
| Third-party C library function | No | Link seam (TU substitution) |
| Static logger / diagnostic sink | No | Link seam (replace `.cpp` in test link) |
| Operations injected as callables with per-test lambda bodies | — | `std::function` table — **not for production; heap + no `noexcept`** |

### Technique Comparison Table

| Technique | Runtime cost | Test ergonomics | DUT type: test vs production | Portability |
|---|---|---|---|---|
| IFoo + GMock | 1 vtable dispatch per call | GMock `EXPECT_CALL`, full argument matching | Same concrete type | Fully portable |
| Template injection (member ref) | None | Fake is a plain struct; per-instance spy via reference | Different (`<Host><Fake>` vs `<Host>`) | Fully portable |
| Template injection (EBO) | None (zero-size base) | Stateless only — no call recording without accessor | Different | Fully portable (C++14); `[[no_unique_address]]` needs C++20 |
| Template injection (dual-ctor) | None | 0-arg for production; 0-arg or 1-arg for tests; shared static spy or per-instance | Different | Fully portable |
| Link seam (TU substitution) | None | `std::function` spy per seam symbol; reset in `TearDown()` | Same concrete type | Fully portable; no compiler extensions |
| `std::function` table | Heap + indirect call | Lambdas, easy per-test setup | Same concrete type | Fully portable |

---

## Patterns

### Pattern 1 — IFoo Interface + GMock

Use when the dependency is a C++ class that is injected as a constructor argument and has (or could have) multiple production implementations.

```cpp
// src/<component>/I<Foo>.h  — production type
class I<Foo>
{
public:
    virtual ~I<Foo>()                                        = default;
    virtual std::error_code <operation>(<params>) noexcept   = 0;
};

// src/<component>/<Host>.h  — dependency injected via constructor
class <Host> final
{
public:
    explicit <Host>(I<Foo>& <foo>) noexcept;

private:
    I<Foo>& m<Foo>;
};

// tests/unit/mocks/Mock<Foo>.h  — test artifact only
#include <gmock/gmock.h>
#include "<component>/I<Foo>.h"

class Mock<Foo> : public I<Foo>
{
public:
    MOCK_METHOD(std::error_code, <operation>, (<params>), (noexcept, override));
};

// tests/unit/<host>_test.cpp — fixture
class <Host>Test : public ::testing::Test
{
protected:
    Mock<Foo>       m<Foo>Mock;
    <Host>          mSut{m<Foo>Mock};
};
```

**When not to use:** When `<Host>` stores the ops type by value in a fixed-size array. Vtable pointer in every element wastes memory and forces heap if the array is replaced with `unique_ptr`.

---

### Pattern 2a — Template Injection (Member Reference)

Use when the ops type is stored by value but the test needs call recording (a stateful spy). The test supplies an ops instance by reference.

```cpp
// src/<component>/<Host>.h
template<typename TOps = <RealOps>>
class <Host> final
{
public:
    explicit <Host>(TOps& ops) noexcept
    : mOps{ops}
    {
    }

private:
    TOps& mOps;
};

// tests/unit/mocks/Fake<Ops>.h  — plain struct, no GMock needed for simple cases
struct Fake<Ops>
{
    int  createCallCount{0};
    bool createShouldFail{false};

    std::error_code create(<params>) noexcept
    {
        ++createCallCount;
        return createShouldFail ? std::make_error_code(std::errc::io_error)
                                : std::error_code{};
    }
};

// tests/unit/<host>_test.cpp
class <Host>Test : public ::testing::Test
{
protected:
    Fake<Ops>       mOps;
    <Host><Fake<Ops>> mSut{mOps};
};
```

---

### Pattern 2b — Template Injection (EBO / `[[no_unique_address]]`)

Use when the ops type is **stateless** (pure wrapper around free functions) and zero memory overhead is required. Suitable for fixed-size pool arrays.

```cpp
// src/<component>/<Host>.h  — C++14: private inheritance gives zero-size base (EBO)
template<typename TOps = <RealOps>>
class <Host> final : private TOps
{
public:
    <Host>() noexcept = default;

private:
    void doWork(<params>) noexcept
    {
        TOps::create(<params>);  // qualified call into base
    }
};

// Alternative C++20: [[no_unique_address]] member (preferred — no inheritance)
template<typename TOps = <RealOps>>
class <Host> final
{
private:
    [[no_unique_address]] TOps mOps;
};
```

**Limitation:** The ops base or member is inaccessible from outside `<Host>`. A test cannot read call counts or inject failure flags without an explicit accessor. Use Pattern 2a when spy state is needed.

---

### Pattern 2c — Template Injection (Dual Constructor)

Use when production call sites must remain zero-argument (no injection noise) while tests still need stateful spy access. A per-instantiation static holds the default ops; an explicit constructor accepts an override.

```cpp
// src/<component>/<Host>.h
template<typename TOps = <RealOps>>
class <Host> final
{
public:
    // Production: 0-arg, uses the per-instantiation static ops object.
    <Host>() noexcept
    : mOps{sDefaultOps}
    {
    }

    // Test: caller supplies a specific ops instance.
    explicit <Host>(TOps& ops) noexcept
    : mOps{ops}
    {
    }

    static TOps& defaultOps() noexcept
    {
        return sDefaultOps;
    }

private:
    TOps&        mOps;
    static TOps  sDefaultOps;
};

template<typename TOps>
TOps <Host><TOps>::sDefaultOps{};

// tests/unit/<host>_test.cpp  — three usage tiers
//
// Tier 1: stateless fake, all instances share the static
//   <Host><Fake<Ops>> a, b, c;
//
// Tier 2: stateful spy via shared static
//   <Host><Fake<Ops>>::defaultOps().createShouldFail = true;
//   <Host><Fake<Ops>> a, b;
//   EXPECT_EQ(<Host><Fake<Ops>>::defaultOps().createCallCount, 2);
//   <Host><Fake<Ops>>::defaultOps() = {};  // reset between tests
//
// Tier 3: independent per-instance spies
//   Fake<Ops>           spyA, spyB;
//   <Host><Fake<Ops>>   a{spyA}, b{spyB};
//   EXPECT_EQ(spyA.createCallCount, 1);
```

**Trade-off:** `defaultOps()` is visible in the production API. It is harmless for a stateless `<RealOps>`, but adds a static accessor that production callers do not need. Prefer Pattern 2a for new code unless zero-argument production sites are a hard constraint.

---

### Pattern 3 — Link Seam (Translation-Unit Substitution)

Use when the dependency is a POSIX syscall or C-ABI free function with exactly one real implementation. Wrap each syscall in a named function inside a dedicated namespace. The production build links the real `.cpp`; the test build links a mock `.cpp` in its place. No compiler extensions are required.

```cpp
// src/<component>/<Host>Posix.h  — shared declaration (both builds include this)
namespace <project>::<component>::posix
{
    int  <c_function>(<params>) noexcept;
}  // namespace <project>::<component>::posix

// src/<component>/<Host>Posix.cpp  — real implementation (production build only)
#include "<component>/<Host>Posix.h"

namespace <project>::<component>::posix
{
    int <c_function>(<params>) noexcept
    {
        return ::<c_function>(<params>);
    }
}  // namespace <project>::<component>::posix

// tests/unit/seams/<Host>PosixMock.cpp  — mock implementation (test build only)
#include "<component>/<Host>Posix.h"

#include <functional>

namespace <project>::<component>::posix
{
    std::function<int(<params>)> g<CFunctionName>Spy;  // reset in TearDown()

    int <c_function>(<params>) noexcept
    {
        if (g<CFunctionName>Spy)
        {
            return g<CFunctionName>Spy(<params>);
        }
        return -1;
    }
}  // namespace <project>::<component>::posix
```

The production class calls `posix::<c_function>(...)` — never `::<c_function>(...)` directly.

CMake wiring:

```cmake
# Production library — links the real POSIX wrapper
target_sources(${TARGET_NAME} PRIVATE
    <Host>Posix.cpp
)

# Test binary — links the mock wrapper instead; real .cpp is NOT listed here
target_sources(${TARGET_NAME}_gtest PRIVATE
    seams/<Host>PosixMock.cpp  # one mock .cpp per seam boundary
)
```

Spy teardown in the test fixture:

```cpp
void TearDown() override
{
    posix::g<CFunctionName>Spy = nullptr;
}
```

---

### Pattern 4 — `std::function` Ops Table (Informational — Do Not Use in Production)

Documented for completeness. Each operation is a `std::function` field. Tests assign lambdas per-operation.

```cpp
struct <Ops>Table
{
    std::function<int(const char*, std::size_t)>  create;
    std::function<void(int)>                      close;
};
```

**Why not to use in VWOS/embedded code:**
- `std::function` heap-allocates for non-trivial callables — violates the no-heap rule in interrupt or real-time contexts.
- `std::function` is not `noexcept` — wrapping it requires explicit try/catch to maintain `noexcept` contracts.
- `std::function` has non-trivial destructor overhead in tight loops.

Use Pattern 2a (member-reference template injection) instead: it achieves identical ergonomics with a plain struct and zero overhead.

---

## Lifecycle & Usage Pattern

### Classification Workflow (SWE.3 Stage 1 — Testability Design)

1. List every external call made by the class under design.
2. For each call, answer: **"Does a second meaningful production implementation of this exist, or could reasonably exist?"**
   - Yes, and it is injected as a constructor argument → Pattern 1 (IFoo) or Pattern 2a/2b/2c (template).
   - Yes, but it lives by value in a fixed-size array → Pattern 2a, 2b, or 2c.
   - No → Pattern 3 (link seam).
3. For template injection, choose the variant: 2a if spy state is needed; 2b if ops are stateless and zero overhead is required; 2c only if production call sites must be zero-argument.
4. For POSIX syscalls or C-ABI free functions, introduce `<Host>Posix.h` + `<Host>Posix.cpp` in `src/`. Add `<Host>PosixMock.cpp` to `tests/unit/seams/`.
5. Record the classification in the class `@details` Doxygen block alongside the POSIX function choices.

### Portability Trigger Rule

The answer to the classification question in step 2 can change over the lifetime of a component. When a **second real platform implementation with different internal structure** becomes concrete (not speculative), the pattern must be promoted:

| Current pattern | Trigger condition | Promoted pattern |
|---|---|---|
| Link seam (TU substitution) | A second platform requires different function signatures for the same logical operation | Template injection — Pattern 2a or 2b |
| Per-class seam files | Multiple classes share the same platform boundary | Single `TPlatformOps` template parameter across all classes (Platform Abstraction Layer) |

**Do not promote speculatively.** Add abstraction only when a concrete second implementation exists or is formally planned. Premature promotion adds template complexity with no current testability benefit.

When promotion is triggered, the change crosses the SWE.2 boundary: a new `arch:` must be added to `architecture.md` and documented in `interfaces.md` before any header is modified.

---

## Examples

### Example A — Injected Collaborator with Two Production Implementations → Pattern 1

`<EventDispatcher>` accepts an `ILogger&`. A `ConsoleLogger` is used in production; a `NullLogger` is used in production for embedded targets. Both are real production types.

```cpp
// src/<component>/ILogger.h
class ILogger
{
public:
    virtual ~ILogger()                              = default;
    virtual void warning(const char* msg) noexcept  = 0;
};

// src/<component>/<EventDispatcher>.h
class <EventDispatcher> final
{
public:
    explicit <EventDispatcher>(ILogger& logger) noexcept;

private:
    ILogger& mLogger;
};

// tests/unit/mocks/MockLogger.h
#include <gmock/gmock.h>
#include "<component>/ILogger.h"

class MockLogger : public ILogger
{
public:
    MOCK_METHOD(void, warning, (const char* msg), (noexcept, override));
};

// tests/unit/<event_dispatcher>_test.cpp
class <EventDispatcher>Test : public ::testing::Test
{
protected:
    MockLogger          mLogger;
    <EventDispatcher>   mSut{mLogger};
};

TEST_F(<EventDispatcher>Test, LogsWarningOnFailure)
{
    EXPECT_CALL(mLogger, warning(::testing::_)).Times(1);
    mSut.triggerFailurePath();
}
```

---

### Example B — Fixed-size Slot Array, Stateful Spy → Pattern 2a

`<Dispatcher>` owns `std::array<TSlot, kMaxSlots>` where `TSlot` performs I/O. The test needs to record how many times `send()` was called.

```cpp
// src/<component>/<Dispatcher>.h
template<typename TSlot = <RealSlot>>
class <Dispatcher> final
{
public:
    explicit <Dispatcher>() noexcept = default;

private:
    std::array<TSlot, kMaxSlots> mSlotPool;
};

// tests/unit/fakes/Fake<Slot>.h  — plain struct, no GMock required
struct Fake<Slot>
{
    int          sendCallCount{0};
    std::error_code send(const uint8_t* /*payload*/, uint32_t /*size*/) noexcept
    {
        ++sendCallCount;
        return {};
    }
};

// tests/unit/<dispatcher>_test.cpp
TEST(DispatcherTest, SendsToAllActiveSlots)
{
    <Dispatcher><Fake<Slot>> sut;
    // arrange: activate slots, then call dispatch
    // assert: iterate mSlotPool and check sendCallCount per slot
}
```

---

### Example C — Stateless POSIX Wrapper, Zero Overhead → Pattern 2b

`<MemoryRegion>` owns a pointer mapped via `mmap`. There is only one `mmap` in production, but the ops struct is stateless so EBO gives zero size overhead.

```cpp
// src/<component>/<MemoryRegion>.h
template<typename TOps = <RealMmapOps>>
class <MemoryRegion> final : private TOps
{
public:
    std::error_code map(int fd, std::size_t size) noexcept
    {
        mAddr = TOps::map(fd, size);
        return (mAddr != nullptr) ? std::error_code{} : std::make_error_code(std::errc::not_enough_memory);
    }

private:
    void* mAddr{nullptr};
};

// tests/unit/fakes/Fake<MmapOps>.h
struct Fake<MmapOps>
{
    std::array<std::byte, 256> buffer{};

    void* map(int /*fileDescriptor*/, std::size_t /*size*/) noexcept
    {
        return buffer.data();
    }

    void unmap(void* /*address*/, std::size_t /*size*/) noexcept
    {
    }
};

// tests/unit/<memory_region>_test.cpp
TEST(<MemoryRegion>Test, MapReturnsSuccess)
{
    <MemoryRegion><Fake<MmapOps>> sut;
    const auto result = sut.map(3, 128U);
    EXPECT_FALSE(result);
}
```

---

### Example D — Zero-Argument Production Sites, Per-Instance Spy in Tests → Pattern 2c

`<ResourcePool>` is constructed throughout the codebase with no arguments. Tests need independent per-instance spy state.

```cpp
// src/<component>/<ResourcePool>.h
template<typename TOps = <RealOps>>
class <ResourcePool> final
{
public:
    <ResourcePool>() noexcept
    : mOps{sDefaultOps}
    {
    }

    explicit <ResourcePool>(TOps& ops) noexcept
    : mOps{ops}
    {
    }

    static TOps& defaultOps() noexcept
    {
        return sDefaultOps;
    }

private:
    TOps&        mOps;
    static TOps  sDefaultOps;
};

template<typename TOps>
TOps <ResourcePool><TOps>::sDefaultOps{};

// tests/unit/<resource_pool>_test.cpp
TEST(<ResourcePool>Test, IndependentSpies)
{
    Fake<Ops>                   spyA;
    Fake<Ops>                   spyB;
    <ResourcePool><Fake<Ops>>   poolA{spyA};
    <ResourcePool><Fake<Ops>>   poolB{spyB};

    poolA.acquire();
    EXPECT_EQ(spyA.acquireCallCount, 1);
    EXPECT_EQ(spyB.acquireCallCount, 0);
}
```

---

### Example E — POSIX `poll()` → Pattern 3

`<EventLoop>` calls `::poll()` directly. Only one real `poll` exists in production.

```cpp
// src/<component>/<EventLoop>Posix.h
namespace <project>::<component>::posix
{
    int poll(pollfd* fds, nfds_t nfds, int timeoutMs) noexcept;
}  // namespace <project>::<component>::posix

// src/<component>/<EventLoop>Posix.cpp
#include "<component>/<EventLoop>Posix.h"

#include <poll.h>

namespace <project>::<component>::posix
{
    int poll(pollfd* fds, nfds_t nfds, int timeoutMs) noexcept
    {
        return ::poll(fds, nfds, timeoutMs);
    }
}  // namespace <project>::<component>::posix

// tests/unit/seams/<EventLoop>PosixMock.cpp
#include "<component>/<EventLoop>Posix.h"

#include <functional>

namespace <project>::<component>::posix
{
    std::function<int(pollfd*, nfds_t, int)> gPollSpy;

    int poll(pollfd* fds, nfds_t nfds, int timeoutMs) noexcept
    {
        if (gPollSpy)
        {
            return gPollSpy(fds, nfds, timeoutMs);
        }
        return 0;
    }
}  // namespace <project>::<component>::posix

// tests/unit/<event_loop>_test.cpp
class <EventLoop>Test : public ::testing::Test
{
protected:
    void TearDown() override
    {
        posix::gPollSpy = nullptr;
    }
};

TEST_F(<EventLoop>Test, ReturnsErrorWhenPollFails)
{
    posix::gPollSpy = [](pollfd* /*fds*/, nfds_t /*n*/, int /*t*/) noexcept -> int
    {
        errno = EINTR;
        return -1;
    };

    const auto result = mSut.processEvents();
    EXPECT_EQ(result.value(), EINTR);
}
```

---

## Best Practices / Anti-patterns

| ✅ Do | ❌ Don't |
|---|---|
| Use Pattern 1 (IFoo) only when multiple production implementations exist or the dependency crosses a component boundary | Create IFoo for every class — adds vtable cost and bloats `src/` |
| Use Pattern 2a for stateful value-member ops; 2b for stateless zero-overhead ops; 2c only when 0-arg production sites are required | Force heap allocation just to enable virtual dispatch in a value-member array |
| Use Pattern 3 for POSIX syscalls — wrap in `posix::` namespace, swap `.cpp` in CMake | Call `::syscall()` directly in business logic — no seam without compiler extensions |
| Keep seam mock `.cpp` files in `tests/unit/seams/` — one file per seam boundary | Scatter seam `.cpp` files across the test tree |
| Reset spy state in `TearDown()` | Let spy state leak between tests — causes non-deterministic failures |
| Use `MOCK_METHOD` (GMock v3+ four-argument form) for Pattern 1 | Use deprecated `MOCK_METHOD0` / `MOCK_METHOD1` |
| Inherit `Mock<Foo>` only from `I<Foo>` | Subclass a concrete class — the base constructor side-effects run in test |
| Prefer plain fake structs (Pattern 2) for simple call recording | Use `std::function` table in production code — heap + no `noexcept` |

---

## Domain Glossary

| Term | Definition |
|---|---|
| **IFoo** | A pure abstract C++ interface class (`I` prefix) that defines the contract for an injectable dependency |
| **Template injection** | C++ template parameterisation used to swap a collaborator type at compile time without virtual dispatch |
| **EBO (Empty Base Optimization)** | Compiler optimization that collapses a zero-data-member base subobject to zero bytes; used in Pattern 2b via private inheritance |
| **`[[no_unique_address]]`** | C++20 attribute that gives the same zero-size guarantee as EBO for a non-static data member |
| **Link seam** | A test-substitution point created at link time by swapping one translation unit for another in the CMake source list |
| **Seam wrapper** | A thin named function in a `posix::` namespace that the production class calls instead of the raw syscall, making the translation unit boundary explicit and replaceable |
| **Spy** | A `std::function` member of the mock translation unit that records or forwards calls made through a link seam, enabling post-test argument and call-count verification |
| **Translation unit (TU)** | One `.cpp` file plus all headers it includes after preprocessing; the unit the compiler processes in one pass to produce one `.o` object file |
