---
name: cpp-callbacks
description: "Guidelines for designing callbacks in C++. Covers the available options with their trade-offs and code examples."
---

# Callback design patterns (C++)

This guideline addresses a recurring design problem: a C++ class (e.g., `EventSource`) must invoke user-supplied behavior at a well-defined event point (e.g., `onEvent`). It outlines and compares four practical implementation approaches, with examples and spelling for both C++14 and C++17. As a baseline, std::function is considered, along with its trade-offs.

---

## Scenario (used throughout)

```cpp
using EventType = int;   // defined by the library

// Library class - its source is not owned by the application developer.
// It must call back into application code when an event fires.
struct EventSource
{
    void processEvents();   // fires onEvent internally
};

// Application class that wraps EventSource and wants to react to events.
struct MyEventSource
{
    EventSource mEventSource;
};
```

---

## Option 0 - `std::function` (baseline / not recommended)

### How it works

`std::function` is the "obvious" solution from `<functional>`. It wraps any callable (lambda, functor, free function, bound member function) behind a type-erased interface.

```cpp
#include <functional>

using EventType = int;

struct EventSource
{
    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        if (onEvent)
            onEvent(eventValue);
    }

    std::function<void(EventType)> onEvent;   // or a setter equivalent
};

struct MyEventSource
{
    MyEventSource()
    {
        mEventSource.onEvent = [this](EventType event) { onEvent(event); };
    }

    void onEvent(EventType event)
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource mEventSource;
};
```

### Why it is often a poor fit for embedded / AUTOSAR / VWOS platforms

| Concern         | Detail |
|-----------------|--------|
| Heap allocation | Small-buffer optimisation is implementation-defined; a capturing lambda that doesn't fit the SBO **heap-allocates** |
| Size overhead   | `sizeof(std::function<void(EventType)>` is typically 24–48 bytes |
| No `noexcept`   | `operator()` is not `noexcept`; copy/move may throw |
| Slower call     | Virtual-dispatch-like indirection plus possible pointer-to-heap dereference |
| MISRA / Autosar | Banned or restricted in several embedded coding guidelines |

**Verdict:** convenient for host-side tooling; avoid in production platform code.

---

## Option 1 - `void*` context + raw function pointer (type-erased, zero-overhead)

This is the classic C-style callback pattern, dressed up with C++ templates to eliminate the manual static trampoline.

### Motivation

A plain function pointer `void (*)(void*, EventType)` is the smallest possible type-erased callback: 1-2 pointers, no heap, `noexcept`-safe, C-ABI compatible.

The only traditional drawback - needing a hand-written static trampoline on every handler type - is eliminated by making the library generate it internally via a captureless lambda.

---

### C++17 variant (`auto` NTTP - most concise, preferred)

```cpp
using EventType = int;

struct EventSource
{
    using OnEventCallback = void (*)(void*, EventType);

    // MemberFunction is deduced automatically via 'auto' NTTP (C++17)
    template<auto MemberFunction, typename T>
    void setOnEventHandler(T& handler)
    {
        mOnEventContext  = &handler;
        mOnEventCallback = [](void* context, EventType event) {
            (static_cast<T*>(context)->*MemberFunction)(event);
        };
        // Captureless lambda decays to a plain function pointer - no heap.
    }

    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        notify(eventValue);
    }

    void notify(EventType event)
    {
        if (mOnEventCallback)
            mOnEventCallback(mOnEventContext, event);
    }

    void*             mOnEventContext{nullptr};
    OnEventCallback   mOnEventCallback{nullptr};
};

struct MyEventSource
{
    MyEventSource()
    {
        mEventSource.setOnEventHandler<&MyEventSource::onEvent>(*this);
    }

    // No static trampoline needed - library generates it from the NTTP.
    void onEvent(EventType event)
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource mEventSource;
};
```

---

### C++14 variant (explicit member-function-pointer type, preferred)

`auto` as an NTTP is C++17. In C++14 the pointer type must be spelled out explicitly:

```cpp
using EventType = int;

struct EventSource
{
    using OnEventCallback = void (*)(void*, EventType);

    // T and the member-function type must both be explicit template parameters.
    template<typename T, void (T::*MemberFunction)(EventType)>
    void setOnEventHandler(T& handler)
    {
        mOnEventContext  = &handler;
        mOnEventCallback = [](void* context, EventType event) {
            (static_cast<T*>(context)->*MemberFunction)(event);
        };
    }

    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        notify(eventValue);
    }

    void notify(EventType event)
    {
        if (mOnEventCallback)
            mOnEventCallback(mOnEventContext, event);
    }

    void*             mOnEventContext{nullptr};
    OnEventCallback   mOnEventCallback{nullptr};
};

struct MyEventSource
{
    MyEventSource()
    {
        // Both template arguments must be supplied explicitly.
        mEventSource.setOnEventHandler<MyEventSource, &MyEventSource::onEvent>(*this);
    }

    void onEvent(EventType event)
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource mEventSource;
};
```

---

### Original / C++11 variant (static trampoline - for reference only)

Before NTTP-based generation was available, every handler type had to provide a `static` trampoline manually. Shown here to make the `static_cast` pattern visible:

```cpp
using EventType = int;

struct EventSource
{
    using OnEventCallback = void (*)(void*, EventType);

    void setOnEventHandler(void* context, OnEventCallback callback)
    {
        mOnEventContext  = context;
        mOnEventCallback = callback;
    }

    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        notify(eventValue);
    }

    void notify(EventType event)
    {
        if (mOnEventCallback)
            mOnEventCallback(mOnEventContext, event);
    }

    void*             mOnEventContext{nullptr};
    OnEventCallback   mOnEventCallback{nullptr};
};

struct MyEventSource
{
    MyEventSource()
    {
        mEventSource.setOnEventHandler(this, &MyEventSource::onEventTrampoline);
    }

    // The event handling implementation
    void onEvent(EventType event)
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    // Hand-written trampoline: recovers 'this' from the void* context
    // and forwards to the real implementation.
    static void onEventTrampoline(void* context, EventType event)
    {
        static_cast<MyEventSource*>(context)->onEvent(event);
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource mEventSource;
};
```

> **Note:** This variant requires a separate `onEventTrampoline` static method on every handler type.
> The NTTP variants above generate the equivalent trampoline inside the library, removing this boilerplate.

### Trade-offs

| | |
|---|---|
| ✅ | Zero overhead - two pointers, one indirect call |
| ✅ | `EventSource` is a concrete (non-template) class |
| ✅ | Runtime polymorphism: handler can be swapped at runtime |
| ✅ | No heap allocation |
| ⚠️ | C++17 call site is clean; C++14 call site is verbose |
| ⚠️ | `void*` requires discipline - no compile-time type safety on the context pointer |

---

### Extension - multiple events, one context pointer

When `EventSource` fires more than one event, the handler object typically handles all of them.
Rather than calling a separate `setOnEventHandler()` per event - which would store the same `void*` context pointer redundantly - a single `setHandlers()` with multiple NTTPs registers every callback in one call while keeping the context pointer stored exactly once.

#### C++17 (variadic `auto` NTTPs - preferred)

```cpp
using EventTypeA = int;
using EventTypeB = float;

struct EventSource
{
    using CallbackA = void (*)(void*, EventTypeA);
    using CallbackB = void (*)(void*, EventTypeB);

    // One call, one context pointer, one trampoline per event.
    template<auto MemberFunctionA, auto MemberFunctionB, typename T>
    void setHandlers(T& handler)
    {
        mContext   = &handler;                          // stored once
        mOnEventA  = [](void* context, EventTypeA event) {
            (static_cast<T*>(context)->*MemberFunctionA)(event);
        };
        mOnEventB  = [](void* context, EventTypeB event) {
            (static_cast<T*>(context)->*MemberFunctionB)(event);
        };
    }

    void processEvents()
    {
        if (mOnEventA) mOnEventA(mContext, /* … */ EventTypeA{});
        if (mOnEventB) mOnEventB(mContext, /* … */ EventTypeB{});
    }

    void*       mContext{nullptr};      // shared by all events
    CallbackA   mOnEventA{nullptr};
    CallbackB   mOnEventB{nullptr};
};

struct MyHandler
{
    void onA(EventTypeA value)
    {
        /* … */
    }

    void onB(EventTypeB value)
    {
        /* … */
    }
};

struct MyEventSource
{
    MyEventSource()
    {
        // Single call - both handlers registered, context stored once.
        mSrc.setHandlers<&MyHandler::onA, &MyHandler::onB>(mHandler);
    }

    MyHandler    mHandler;
    EventSource  mSrc;
};
```

#### C++14 (explicit member-function-pointer types)

```cpp
// Inside EventSource:
template<typename T,
         void (T::*MemberFunctionA)(EventTypeA),
         void (T::*MemberFunctionB)(EventTypeB)>
void setHandlers(T& handler)
{
    mContext   = &handler;
    mOnEventA  = [](void* context, EventTypeA event) {
        (static_cast<T*>(context)->*MemberFunctionA)(event);
    };
    mOnEventB  = [](void* context, EventTypeB event) {
        (static_cast<T*>(context)->*MemberFunctionB)(event);
    };
}
```

Call site: `mSrc.setHandlers<MyHandler, &MyHandler::onA, &MyHandler::onB>(mHandler);`

#### Storage comparison

| Approach                                 | `void*` stored    | fn ptrs stored |
|------------------------------------------|-------------------|----------------|
| Separate `setOnEventHandler()` per event | N (one per event) | N              |
| Single `setHandlers()`                   | **1**             | N              |

The saving grows with the number of events.
For N events on a single handler object, the multi-NTTP pattern is both more compact in storage and more explicit at the call site about the coupling between all handlers and the same object.

> **Note:** The handler methods may share identical signatures (e.g. `void onOpen(int descriptor)` and `void onClose(int descriptor)`).
> This applies to both the C++17 (`auto` NTTP) and C++14 (explicit member-function-pointer type) variants.
> The template arguments are member-function **pointer values**, not types - two methods with the same signature are still distinct pointer values, so the compiler generates a separate, correct trampoline for each.

---

## Option 2 - Virtual interface (simplest, one vtable-call overhead)

### How it works

Define a pure-virtual interface. `EventSource` holds a pointer to it. `MyEventSource` implements it. No trampolines, no `void*`, no templates in the library.

### C++11 / C++14 / C++17 - identical

```cpp
using EventType = int;

struct IEventHandler
{
    virtual void onEvent(EventType event) = 0;
    virtual ~IEventHandler()               = default;
};

struct EventSource
{
    void setHandler(IEventHandler& handler)
    {
        mHandler = &handler;
    }

    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        if (mHandler)
            mHandler->onEvent(eventValue);
    }

    IEventHandler* mHandler{nullptr};
};

struct MyEventSource : IEventHandler
{
    MyEventSource()
    {
        mEventSource.setHandler(*this);
    }

    void onEvent(EventType event) override
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource mEventSource;
};
```

### Trade-offs

| | |
|---|---|
| ✅ | Simplest code - no templates in the library, no `void*` |
| ✅ | Fully type-safe |
| ✅ | Works from C++11 onward without any syntax difference |
| ✅ | `EventSource` remains a concrete class |
| ⚠️ | One vtable indirection per call (typically negligible) |
| ⚠️ | `MyEventSource` is coupled to the interface by inheritance |
| ⚠️ | Adding a second callback requires a second method in the interface |

> **Multiple events:** Supported by design - add one pure-virtual method per event to the interface.
> The same `IEventHandler*` pointer covers all events; no separate context pointer is needed per event.

---

## Option 3 - Template `EventSource<Handler>` (zero overhead, compile-time only)

### How it works

Parameterise `EventSource` on the handler type. The call is resolved at compile time via a direct member-function call - no pointer, no vtable, no indirection whatsoever.

### C++11 / C++14 / C++17 - identical

```cpp
using EventType = int;

template<typename Handler>
struct EventSource
{
    void setHandler(Handler& handler)
    {
        mHandler = &handler;
    }

    void processEvents()
    {
        EventType eventValue = /* compute next event value */ 0;
        if (mHandler)
            mHandler->onEvent(eventValue);
    }

    Handler* mHandler{nullptr};
};

struct MyEventSource
{
    MyEventSource()
    {
        mEventSource.setHandler(*this);
    }

    void onEvent(EventType event)
    {
        std::cout << "onEvent(" << event << ")" << std::endl;
    }

    void processEvents()
    {
        mEventSource.processEvents();
    }

    EventSource<MyEventSource> mEventSource;   // CRTP-like, resolved at compile time
};
```

### Trade-offs

| | |
|---|---|
| ✅ | Absolute zero overhead - compiler inlines everything |
| ✅ | No `void*`, no vtable, no function pointer |
| ✅ | Works from C++11 onward |
| ❌ | `EventSource` becomes a class template - cannot store `EventSource<A>` and `EventSource<B>` in the same container |
| ❌ | No runtime polymorphism - handler type must be fixed at compile time |
| ⚠️ | Increased compile time / code size if instantiated for many handler types |

> **Multiple events:** Supported by design - add one method per event to the handler type and call each via `mHandler` inside `processEvents()`.
> The same `Handler*` is the implicit shared context for all events; `EventSource<T>` stores it once.

---

## Summary comparison

| | `std::function`<br>(Option 0) | `void*` + fn ptr<br>(Option 1) | Virtual interface<br>(Option 2) | Template EventSource<br>(Option 3) |
|---------------------------------|---|---|---|---|
| Overhead                        | Medium–High | ~1 indirect call | ~1 vtable call | Zero |
| Heap allocation                 | Possible    | No  | No  | No |
| `EventSource` is a template     | No          | No  | No  | **Yes** |
| Runtime polymorphism            | Yes         | Yes | Yes | **No**  |
| Type safety                     | Yes         | No (`void*`)  | Yes | Yes |
| C++14 usable                    | Yes         | Yes (verbose) | Yes | Yes |
| C++17 improvement               | -           | `auto` NTTP (clean call site) | - | - |
| Embedded / MISRA friendly       | No          | Yes | Yes | Yes |
| Handler boilerplate             | Capturing lambda | Method only | `override` only | Method only |
| Multiple events,<br>one context | Yes (context captured<br>per lambda) | Yes, via `setHandlers()` | Yes, by design | Yes, by design |

---

## Decision guide

```
Need runtime polymorphism?
├── No  →  Option 3 (template EventSource)   - zero overhead, cleanest call
└── Yes
    ├── Simplicity is priority?
    │   └── Yes  →  Option 2 (virtual)       - least library complexity
    └── No vtable / C-ABI / strict size budget?
        ├── C++17 available  →  Option 1 C++17  (auto NTTP)
        └── C++14 only       →  Option 1 C++14  (explicit member-fn type)
```

`std::function` is recommended **only** for host-side tooling, tests, or prototyping - not for production platform code.
