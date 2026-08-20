---
name: cpp-tail-arrays
description: "Guidelines for using and implementing tail arrays in C++ objects. Tail arrays let objects collocate array data with object state to improve cache locality and reduce allocation overhead when the array size is known only at construction time."
---

# C++ tail arrays and collocated tail data

Use this skill when designing a C++ class that must hold one or more dynamically-sized arrays within the same allocation as the object itself, with the array size known only at construction time. Covers the `tail_array<T>` abstraction, factory pattern, layout planning, arena ownership, lifecycle (init/teardown), and patterns for multiple tail regions or tail-allocated implementation objects.

---

## Overview

A tail array is a technique to place array data immediately after an object's static layout in memory, all within a single allocation. The object holds a small array header (typically size and offset) rather than a pointer to separate heap memory. This yields:

- **Collocated memory**: Object state and array data are brought into cache together.
- **Single allocation**: Factory function reserves one contiguous block from an arena.
- **Relocatable addressing**: Offset-based storage (not pointers) makes the layout suitable for arenas and memory mappings.
- **Known total size**: The factory computes layout once at construction and never changes it.

The typical use case is startup-owned objects with a variable sized array(s) in an embedded system that live for the entire component lifetime in a fixed arena.

Use of tail arrays in objects impacts how such objects are constructed, initialized, and managed. A factory function is required to compute the total object layout, allocate memory, construct the object, and initialize the tail array headers with the correct offsets and sizes. 

The following concepts contribute to their efficient implementation:

- **Tail array wrapper**: A template class `tail_array<T>` that provides an API to access the tail data as a normal array, and stores information about the array size and location.
- **Tail layout helper**: A utility to compute aligned offsets for multiple tail regions of an object, with built-in overflow checking to ensure safe layout planning.
- **Runtime assertions**: A mechanism that supports fail-fast checks in tail array or helper implementations and simplifies API design by allowing execution to stop immediately in a controlled manner when invalid conditions are detected (e.g., offset too large for the offset type).
- **Custom object allocator**: A simple monotonic arena that serves allocations sequentially and never deallocates, suitable for startup-owned objects.

TODO: The code snippets must be verified for correctness!

---

## The tail_array<T> wrapper

A `tail_array<T>` stores the size and location of an array of `T` as part of the enclosing object's static layout. Instead of holding a pointer to `T[size]`, it stores:

- A **count** (number of elements)
- An **offset** (relative distance from the wrapper's own address to the first element)

The offset is typically a narrower integer type (e.g., `uint16_t` or `uint32_t`) than a pointer, reducing memory overhead on 64-bit systems.

```cpp
template<typename T, typename OffsetType = std::uint32_t, typename CountType = std::uint32_t>
class tail_array
{
private:
    OffsetType m_offset;  // Distance from *this to first element aligned to T
    CountType m_count;    // Number of elements
    
public:
    tail_array() noexcept
    : m_offset{0}, m_count{0}
    {
    }
    
    // Called by outer object factory method after memory is allocated for the whole outer object,
    // i.e., including all tail array data.
    // a_array_offset is the offset from the start of the tail_array object to the first element of the array data.
    // If the offset or element count exceed the capacity of the respective types, the method produces a runtime assertion
    // and leaves the tail_array in the default state (empty array).
    void init(std::size_t a_array_offset, std::size_t a_element_count) noexcept
    {
        // Check that offset and count fit in the respective types
        if (a_array_offset > std::numeric_limits<OffsetType>::max()) {
            runtime_assert(false, "tail_array offset exceeds OffsetType capacity");
            return;  // Leaves object in default state
        }
        if (a_element_count > std::numeric_limits<CountType>::max()) {
            runtime_assert(false, "tail_array count exceeds CountType capacity");
            return;  // Leaves object in default state
        }
        m_offset = static_cast<OffsetType>(a_array_offset);
        m_count = static_cast<CountType>(a_element_count);
    }
    
    // Array-like access
    T* data() noexcept
    {
        if (m_count == 0) {
            return nullptr;
        }
        return reinterpret_cast<T*>(reinterpret_cast<char*>(this) + m_offset);
    }
    
    T& operator[](std::size_t a_index) noexcept
    {
        return data()[a_index];
    }
    
    T* begin() noexcept
    {
        return data();
    }
    
    T* end() noexcept
    {
        return data() + m_count;
    }
    
    std::size_t size() const noexcept
    {
        return m_count;
    }
};
```

---

## Embedded, not standalone

A `tail_array<T>` is always embedded in an outer class as a member. It is not allocated separately. The outer object's factory function reserves one contiguous block that contains:

- The static layout of the outer object, including one or more `tail_array<T>` wrappers.
- The actual array data for each `tail_array<T>`, properly aligned

All of this is allocated at once from an arena.

---

## Offset storage vs. pointers

The default behavior uses **offset storage** (narrow integer). This is more compact than a pointer and remains valid if the allocation is moved or copied as a unit.

```cpp
// NOT recommended: pointer storage wastes space
template<typename T>
class tail_array_with_pointer
{
private:
    T* m_data;          // 8 bytes on 64-bit
    std::size_t m_count; // 8 bytes
};

// Recommended: offset storage is more compact
template<typename T>
class tail_array_with_offset
{
private:
    std::uint32_t m_offset; // 4 bytes
    std::uint32_t m_count;  // 4 bytes
};
```

If pointer storage is explicitly required (e.g., for compatibility), it can be selected via a template parameter.

---

## The factory pattern

Objects with tail arrays are created using a **factory function** (typically a static `make()` method) that:

1. **Computes the layout**: Calculates aligned offsets for each tail region.
2. **Checks overflow**: Detects arithmetic overflow while planning offsets and total size.
3. **Allocates**: Reserves one contiguous block from an arena.
4. **Initializes tail headers**: Calls `init()` on each `tail_array<T>` with its offset and count; overflow-to-offset-type mismatch triggers fail-fast assertion.
5. **Constructs the outer object**: Uses placement-new to construct the outer type at the allocated address.
6. **Returns or fails**: Returns a pointer to the constructed object, or `nullptr` if allocation failed.

## Tail layout helper

To avoid tedious handwritten offset arithmetic of the array position in the total object layout, a **tail layout** helper encapsulates the offset calculation and validates the result:

```cpp
// Conceptual tail layout helper templated on outer type
template<typename OuterType>
class tail_layout
{
private:
    std::size_t m_offset;
    bool m_overflow;
    
public:
    tail_layout() noexcept
    : m_offset(sizeof(OuterType)), m_overflow(false)
    {
    }
    
    // Align and reserve space for T[a_count], returning the offset of the array data
    // relative to the start of the OuterType layout.
    // Returns 0 if total object size exceeds std::size_t.
    template<typename T>
    std::size_t reserve(std::size_t a_count) noexcept
    {
        if (m_overflow) {
            return 0;  // Already in overflow state
        }
        
        // Align m_offset to T
        constexpr std::size_t alignment = alignof(T);
        m_offset = (m_offset + alignment - 1) & ~(alignment - 1);
        std::size_t result = m_offset;
        
        // Check if total array size fits within std::size_t
        if (a_count > std::numeric_limits<std::size_t>::max() / sizeof(T)) {
            m_overflow = true;
            return 0;
        }
        
        std::size_t array_size = a_count * sizeof(T);
        
        // Check if end of the array data in the OuterType at the aligned offset fits within std::size_t
        if (m_offset > std::numeric_limits<std::size_t>::max() - array_size) {
            m_overflow = true;
            return 0;
        }
        
        m_offset += array_size;
        return result;
    }
    
    // Returns total object size, i.e., including the tail array data.
    // Returns 0, if total object size exceeds std::size_t.
    std::size_t total_size() const noexcept
    {
        return m_overflow ? 0 : m_offset;
    }

    template<typename TailMemberType, typename CountType>
    static void init_member(OuterType& a_outer, TailMemberType OuterType::* a_member, std::size_t a_tail_data_offset, std::size_t a_count) noexcept
    {
        auto* member_ptr = &(a_outer.*a_member);
        std::size_t member_offset = static_cast<std::size_t>(reinterpret_cast<char*>(member_ptr) - reinterpret_cast<char*>(&a_outer));
        member_ptr->init(a_tail_data_offset - member_offset, a_count);
    }
};
```

This helper replaces manual offset calculation in the factory:

```cpp
// Without tail layout planner: error-prone manual math
// NOTE: align_up<T>(a_offset) is a helper that rounds a_offset up to the next multiple of alignof(T)
std::size_t outer_end = sizeof(<outer_type>);
std::size_t array1_offset = align_up<array1_element_t>(outer_end);
std::size_t array2_offset = align_up<array2_element_t>(array1_offset + sizeof(array1_element_t) * a_count1);
std::size_t total_size   =                            (array2_offset + sizeof(array2_element_t) * a_count2);

// With tail layout planner: cleaner
tail_layout<outer_type> layout;
auto array1_offset = layout.reserve<array1_element_t>(a_count1);
auto array2_offset = layout.reserve<array2_element_t>(a_count2);
if (layout.total_size() == 0) {
    return nullptr;  // Overflow occurred
}
```

After determining the tail array data offsets and the needed total size, the factory can allocate memory and initialize object and the tail array wrappers. The tail layout helper also provides a static `init_member()` function to simplify the initialization of the tail array members, which abstracts away the offset math, since the tail array wrappers use offsets relative to their own address.

To hide repeated and error prone `offset - offsetof(object, member)` math in factories, call `init_member(...)` on the layout object:

```cpp
tail_layout<outer_type> layout;
...
layout.init_member(*outer, &outer_type::m_tail, tail_offset_data_in_outer, array_size);
```

---

## Prevent copy and move

Objects containing tail arrays should explicitly delete copy and move operations to prevent accidental misuse, since the tail data is tightly coupled with the object's memory layout and cannot be safely copied or moved without special handling. Deleted functions should be declared public to produce clear error messages that explicitly state the function is deleted.

```cpp
class outer_type final
{
public:
    // Prevent copy and move
    outer_type(const outer_type&) = delete;
    outer_type& operator=(const outer_type&) = delete;
    outer_type(outer_type&&) = delete;
    outer_type& operator=(outer_type&&) = delete;
    
    // Other declarations
};
```

---

## Runtime assertions

Runtime assertions are a simple mechanism for fail-fast checks when fatal, non-recoverable conditions occur in implementations, without complicating the API with error codes or similar constructs. For example, this applies when the tail array data offset exceeds the capacity of the offset type. That condition is a programming error that developers should detect and fix, rather than handle at runtime.

The runtime assertion interface and handling can be implemented as shown below. The default action aborts the program, and the integrator can customize the behavior by setting a custom handler.

```cpp
// Interface

using runtime_assert_handler_t = void (*)(const char*) noexcept;
void runtime_assert(bool a_condition, const char* a_message) noexcept;
void set_runtime_assert_handler(runtime_assert_handler_t a_handler) noexcept;

// Possible implementation

void default_runtime_assert_handler(const char* a_message) noexcept
{
    (void)a_message;
    std::abort();
}

runtime_assert_handler_t& runtime_assert_handler() noexcept
{
    static runtime_assert_handler_t handler = &default_runtime_assert_handler;
    return handler;
}

void set_runtime_assert_handler(runtime_assert_handler_t a_handler) noexcept
{
    runtime_assert_handler() = (a_handler != nullptr) ? a_handler : &default_runtime_assert_handler;
}

void runtime_assert(bool a_condition, const char* a_message) noexcept
{
    if (!a_condition) {
        runtime_assert_handler()(a_message);
    }
}

```

## Custom object allocator

TODO:

---

## Examples

### Example 1: Single tail array

A resource pool that manages a fixed number of connection slots:

```cpp
class connection_pool final
{
private:
    struct connection_slot
    {
        int socket_fd;
        bool in_use;
    };
    
    // Other members for pool management
    tail_array<connection_slot> m_slots;
    
    connection_pool() noexcept
    {
    }
    
public:
    // Factory: create a pool with a specific capacity
    static connection_pool* make(object_allocator& a_allocator, std::size_t a_capacity) noexcept
    {
        if (a_capacity > 128) {  // Example limit
            return nullptr;  // Sanity check
        }
        
        tail_layout<connection_pool> layout;

        auto slots_offset = layout.reserve<connection_slot>(a_capacity);
        
        if (layout.total_size() == 0) {
            return nullptr;  // Overflow in layout
        }
        
        auto addr = a_allocator.alloc<connection_pool>(layout.total_size());
        if (addr == nullptr) {
            return nullptr;
        }
        
        // Initialize the tail array (fail-fast on invalid offset narrowing)
        layout.init_member(*addr, &connection_pool::m_slots, slots_offset, a_capacity);
        
        // Placement-construct the outer object and return it
        return new (addr) connection_pool();
    }
    
    connection_slot* get_slot(std::size_t a_index) noexcept
    {
        if (a_index >= m_slots.size()) {
            return nullptr;
        }
        return &m_slots[a_index];
    }
    
    std::size_t capacity() const noexcept
    {
        return m_slots.size();
    }
    
    // Prevent copy and move
    connection_pool(const connection_pool&) = delete;
    connection_pool& operator=(const connection_pool&) = delete;
    connection_pool(connection_pool&&) = delete;
    connection_pool& operator=(connection_pool&&) = delete;
};
```

---

### Example 2: Multiple tail arrays

A server that tracks both active file descriptors and event records in parallel arrays:

```cpp
class event_dispatcher final
{
private:
    struct poll_entry
    {
        int fd;
        short events;
        short revents;
    };
    
    struct event_record
    {
        int type;
        std::size_t timestamp;
    };
    
    std::size_t m_max_events;
    tail_array<poll_entry> m_poll_table;
    tail_array<event_record> m_event_buffer;
    
    event_dispatcher(std::size_t a_max_events) noexcept
    : m_max_events(a_max_events)
    {
    }
    
public:
    static event_dispatcher* make(object_allocator& a_allocator, std::size_t a_max_events) noexcept
    {
        tail_layout<event_dispatcher> layout;
        
        auto poll_offset = layout.reserve<poll_entry>(a_max_events);
        auto event_offset = layout.reserve<event_record>(a_max_events);
        
        if (layout.total_size() == 0) {
            return nullptr;  // Overflow in layout
        }
        
        auto addr = a_allocator.alloc<event_dispatcher>(layout.total_size());
        if (addr == nullptr) {
            return nullptr;
        }
        
        // Initialize both tail arrays (fail-fast on invalid offset narrowing)
        layout.init_member(*addr, &event_dispatcher::m_poll_table, poll_offset, a_max_events);
        layout.init_member(*addr, &event_dispatcher::m_event_buffer, event_offset, a_max_events);
        
        return new (addr) event_dispatcher(a_max_events);
    }
    
    poll_entry* poll_table() noexcept
    {
        return m_poll_table.data();
    }
    
    event_record* event_buffer() noexcept
    {
        return m_event_buffer.data();
    }
    
    // Prevent copy and move
    event_dispatcher(const event_dispatcher&) = delete;
    event_dispatcher& operator=(const event_dispatcher&) = delete;
    event_dispatcher(event_dispatcher&&) = delete;
    event_dispatcher& operator=(event_dispatcher&&) = delete;
};
```

---

### Example 3: Tail-allocated implementation (pimpl-like)

An outer facade that holds a complex implementation object in its tail:

```cpp
class server_handle final
{
private:
    struct server_impl
    {
        std::mutex lock;
        int listen_socket;
        tail_array<client_connection> m_clients;
        // ... more impl details
    };
    
    server_impl* m_impl;
    
    server_handle(server_impl* a_impl) noexcept
    : m_impl(a_impl)
    {
    }
    
public:
    static server_handle* make(object_allocator& a_allocator, std::size_t a_max_clients) noexcept
    {
        tail_layout<server_handle> layout;
        
        auto impl_offset = layout.reserve<server_impl>(1);
        auto clients_offset = layout.reserve<client_connection>(a_max_clients);
        
        if (layout.total_size() == 0) {
            return nullptr;  // Overflow in layout
        }
        
        auto addr = a_allocator.alloc<server_handle>(layout.total_size());
        if (addr == nullptr) {
            return nullptr;
        }
        
        // Placement-construct the impl object
        auto impl = new (reinterpret_cast<char*>(addr) + impl_offset) server_impl{};
        
        // Initialize the tail array inside impl (fail-fast on invalid offset narrowing)
        tail_layout<server_impl> impl_layout;
        impl_layout.init_member(*impl, &server_impl::m_clients, clients_offset - impl_offset, a_max_clients);
        
        // Placement-construct the handle and return it
        return new (addr) server_handle(impl);
    }
    
    std::size_t client_capacity() const noexcept
    {
        return m_impl->m_clients.size();
    }
    
    server_handle(const server_handle&) = delete;
    server_handle& operator=(const server_handle&) = delete;
};
```

---

## Lifecycle: init, teardown, and reuse

Objects with tail arrays typically follow a lifecycle pattern suited to arena ownership:

1. **Construction**: The factory creates the object in uninitialized state (tail arrays have empty state).
2. **Initialization**: Explicit `init()` calls wire up the tail headers.
3. **Use**: The object is used normally.
4. **Teardown**: Explicit `teardown()` method (if non-trivial element types) or just clearing flags to mark as unused.
5. **Reuse**: The memory block can be reinitialized (without reallocation) by calling `init()` again.

### Support for repeated init/teardown

If the object type supports initialization and teardown without deallocation, it enables reuse patterns. For non-trivial element types (e.g., elements with locks or file descriptors), provide explicit methods:

```cpp
class server_handle final
{
private:
    // ... as before ...
    
    bool m_initialized{false};
    
public:
    // ... factory and other methods ...
    
    // Explicit initialization (called once after make(), or after teardown())
    int init() noexcept
    {
        if (m_initialized) {
            return -1;  // Already initialized
        }
        
        // Wire up any element-level state
        for (auto& client : m_impl->m_clients) {
            client.reset();
        }
        
        m_initialized = true;
        return 0;
    }
    
    // Explicit teardown (cleans up without releasing memory)
    int teardown() noexcept
    {
        if (!m_initialized) {
            return -1;
        }
        
        // Clean up element-level resources
        for (auto& client : m_impl->m_clients) {
            client.close();
        }
        
        m_initialized = false;
        return 0;
    }
};
```

---

## Best practices and anti-patterns

### ✅ Do

- **Default-construct tail arrays to empty state**: A default constructor should leave `m_offset` and `m_count` zero, ready for `init()`.
- **Use a tail layout helper**: Encapsulate offset math to reduce errors and improve readability.
- **Keep integrity checks fail-fast**: Let implementation assert on integrity checks (e.g., offset narrowing errors) and stop execution early.
- **Delete copy and move**: Arena-owned objects should not be copied, moved, or assigned.
- **Use plain pointers for ownership**: Arena ownership is not compatible with `std::unique_ptr` or `std::shared_ptr` by default.
- **Group tightly related tail arrays**: Keep the order and colocation intentional; document the layout plan in a comment.

### ❌ Don't

- **Store pointers to array elements outside the object**: The tail data is part of the same allocation; moving or destroying the allocation invalidates all element pointers.
- **Assume the tail array is initialized after construction**: Always call `init()` explicitly in the factory.
- **Mix heap and arena allocation**: Allocate everything from the arena in one call, not piecemeal.
- **Disable or bypass runtime assertions**: Keep fail-fast checks active so failing integrity checks stop immediately.
- **Use `std::vector` or dynamic allocation inside tail array elements**: Keep elements as simple data or small objects without further heap allocation.
- **Forget deletion of copy/move operations**: This prevents accidental misuse.

---

## Appendix: Compiler extensions and alternatives

### Zero-length array - ZLA (GCC extension)

Some codebases use GCC's zero-length array syntax for tail data:

```cpp
struct poll_table_zla
{
    std::uint32_t m_count;
    pollfd m_items[0];  // NOT standard C++; GCC extension
};
```

This replaces a `tail_array<T>` member with one tail member in the owning type.

### Flexible array member - FAM (C99, C++17 onwards)

C99 and later introduced flexible array members. C++17 does not yet provide standard support, but some compilers extend the language:

```cpp
struct poll_table_fam
{
    std::uint32_t m_count;
    pollfd m_items[];  // Compiler extension in C++
};
```

### Usage pattern for ZLA and FAM

```cpp
template<typename PoolType>
PoolType* make_pool_table(object_allocator& a_allocator, std::size_t a_count) noexcept
{
    std::size_t total_size = sizeof(PoolType) + a_count * sizeof(pollfd);
    auto* addr = a_allocator.alloc<PoolType>(total_size);
    if (addr == nullptr) {
        return nullptr;
    }
    addr->m_count = static_cast<std::uint32_t>(a_count);
    return addr;
}

template<typename PoolType>
pollfd* data(PoolType* a_table) noexcept
{
    return a_table->m_items;
}

template<typename PoolType>
pollfd& at(PoolType& a_table, std::size_t a_index) noexcept
{
    return a_table.m_items[a_index];
}
```

Constraints of ZLA and FAM approaches:

- The tail member must be the last member of the owning type.
- One direct tail member per owning type is practical.
- Modeling multiple tail regions requires one larger tail block and manual splitting and alignment logic.

Because of these constraints, `tail_array<T>` is usually the better and extension-free solution for portable C++ code.

### Pointer-based alternative

If the offset type is too restrictive, a pointer-based variant can be selected:

```cpp
template<typename ElementType>
class tail_array_ptr
{
private:
    ElementType* m_data;
    std::size_t m_count;
};

// More memory overhead but no offset range limits
```

Use only if measured and justified; offset-based is preferred.

---
