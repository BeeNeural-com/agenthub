---
name: posix-shared-memory
description: "POSIX shared memory API reference (shm_open, mmap, munmap, shm_unlink, ftruncate) with usage patterns and pitfalls. Use when designing or implementing POSIX shared memory IPC in C++ for E3 Software Platform components."
---

# POSIX Shared Memory

## Official References

| Document                                                              | URL                                                       | Version                     |
| --------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------- |
| `shm_overview(7)` — Overview of POSIX shared memory                   | https://man7.org/linux/man-pages/man7/shm_overview.7.html | man-pages 6.16 (2025-05-17) |
| `shm_open(3)` / `shm_unlink(3)` — Create/open or unlink shared memory | https://man7.org/linux/man-pages/man3/shm_open.3.html     | man-pages 6.16 (2025-09-21) |
| `mmap(2)` / `munmap(2)` — Map or unmap memory                         | https://man7.org/linux/man-pages/man2/mmap.2.html         | man-pages 6.16 (2025-10-29) |
| `ftruncate(2)` — Set size of a file or shared memory object           | https://man7.org/linux/man-pages/man2/ftruncate.2.html    | man-pages 6.16 (2025-10-29) |

Standard: POSIX.1-2008 (`shm_open`/`shm_unlink`), POSIX.1-2024 (`mmap`, `ftruncate`).
Available on Linux ≥ 2.4 with glibc ≥ 2.2. Link with `-lrt`.

---

## Overview

POSIX Shared Memory allows unrelated processes to communicate by mapping a common region of memory into each process's virtual address space. Writes by one process are immediately visible to all other processes that have mapped the same region.

### Key characteristics

- **Kernel persistence**: A shared memory object persists until the system is shut down, or until all processes have unmapped it AND it has been deleted with `shm_unlink()`. Closing the file descriptor alone does NOT remove the object.
- **Storage**: Implemented as a `tmpfs` filesystem, normally mounted at `/dev/shm` on Linux. Objects live in RAM (and swap if needed).
- **Name format**: `/somename` — begins with `/`, contains no further slashes, and must not exceed `NAME_MAX` (255) characters.
- **Initial size is zero**: A newly created shared memory object has size 0. `ftruncate()` must be called to set the size before mapping.
- **Zero-initialization**: Newly allocated bytes are automatically zeroed by the kernel.
- **`FD_CLOEXEC` set automatically**: `shm_open()` sets `FD_CLOEXEC` on the returned fd. The fd is safe to use in processes that spawn child processes via `exec()`.
- **Synchronization is the caller's responsibility**: The kernel does not synchronize concurrent access. Processes must use POSIX semaphores, `pthread` mutexes with `PTHREAD_PROCESS_SHARED`, or C++ atomics on properly aligned data.

---

## API Reference

### `shm_open(3)`
```c
#include <sys/mman.h>
#include <sys/stat.h>   /* mode constants */
#include <fcntl.h>      /* O_* constants */

int shm_open(const char *name, int oflag, mode_t mode);
```
- `name`: Shared memory object name, format `/somename`.
- `oflag`: Exactly one of `O_RDONLY` or `O_RDWR`, ORed with zero or more of:
  - `O_CREAT` — create if absent; `mode` specifies permissions (masked by `umask`)
  - `O_EXCL` — fail with `EEXIST` if already exists (use with `O_CREAT` for atomic creation)
  - `O_TRUNC` — truncate to zero bytes if already exists
- `mode`: Permission bits (e.g., `0600`); ignored without `O_CREAT`.
- Returns: file descriptor (≥ 0) on success; `-1` on error. The fd has `FD_CLOEXEC` set.

### `shm_unlink(3)`
```c
int shm_unlink(const char *name);
```
- Removes the shared memory object name. The object's memory is freed only when all processes that have mapped it call `munmap()`.
- Returns: `0` on success; `-1` on error.

### `ftruncate(2)`
```c
#include <unistd.h>
int ftruncate(int fd, off_t length);
```
- Sets the size of the shared memory object referenced by `fd`.
- **Must be called after `shm_open(O_CREAT)` before any `mmap()`** — a new object has size 0.
- `length` must be ≥ 0. The fd must be open for writing (`O_RDWR`).
- Extended bytes are zero-initialized.
- Returns: `0` on success; `-1` on error.

### `mmap(2)`
```c
#include <sys/mman.h>
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
```
- Maps the shared memory object into the calling process's virtual address space.
- `addr`: `NULL` (let the kernel choose; most portable).
- `length`: Number of bytes to map. Must be ≤ the object's `ftruncate()`-set size.
- `prot`: `PROT_READ`, `PROT_WRITE`, or `PROT_READ | PROT_WRITE`. Must not conflict with `oflag` in `shm_open()`.
- `flags`: `MAP_SHARED` — updates visible to all processes mapping the same region. **Always use `MAP_SHARED` for IPC shared memory.**
- `fd`: File descriptor from `shm_open()`.
- `offset`: `0` for the beginning of the object (must be a multiple of the page size).
- Returns: pointer to mapped region on success; `MAP_FAILED` (`(void*)-1`) on error.
- **The fd may be closed after `mmap()` without affecting the mapping.**

### `munmap(2)`
```c
int munmap(void *addr, size_t length);
```
- Removes the mapping from the process's address space.
- Does NOT delete the shared memory object (use `shm_unlink()` for that).
- The mapping is also removed automatically when the process terminates.
- Returns: `0` on success; `-1` on error.

---

## Lifecycle & Usage Pattern

### Producer / Creator (owns the object lifecycle)

```
shm_open("/name", O_CREAT | O_EXCL | O_RDWR, 0600)  → fd
  ↓
ftruncate(fd, size)                                  → sets object size
  ↓
mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0) → ptr
  ↓
close(fd)                                            → fd no longer needed; mapping persists
  ↓
[write to *ptr; synchronize with semaphore/mutex]
  ↓
munmap(ptr, size)                                    → removes mapping from this process
  ↓
shm_unlink("/name")                                  → removes the name; memory freed when all unmap
```

### Consumer / Reader (maps an existing object)

```
shm_open("/name", O_RDWR, 0)                         → fd
  ↓
[optional: fstat(fd, &sb) to discover size]
  ↓
mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0) → ptr
  ↓
close(fd)                                            → fd no longer needed; mapping persists
  ↓
[read from *ptr; synchronize with semaphore/mutex]
  ↓
munmap(ptr, size)                                    → removes mapping from this process
```

### Read-only consumer

```
shm_open("/name", O_RDONLY, 0)                       → fd
mmap(NULL, size, PROT_READ, MAP_SHARED, fd, 0)       → ptr (read-only mapping)
close(fd)
[read from *ptr]
munmap(ptr, size)
```

### Synchronization pattern (POSIX unnamed semaphore in shared memory)

Place the semaphore inside the shared memory struct so it is accessible to all processes:

```c
struct SharedRegion {
    sem_t ready;           // POSIX unnamed semaphore; process-shared
    // ... payload fields
};

// Producer init:
sem_init(&region->ready, /*pshared=*/1, /*value=*/0);

// Consumer waits:
sem_wait(&region->ready);

// Producer signals:
sem_post(&region->ready);

// Cleanup (producer):
sem_destroy(&region->ready);
```

### C++14 RAII Wrapper (pattern)

Use RAII to guarantee `munmap()` and optionally `shm_unlink()` on scope exit:

```cpp
// Deleter for munmap
struct MunmapDeleter {
    std::size_t size;
    void operator()(void* ptr) const noexcept {
        if (ptr && ptr != MAP_FAILED)
            ::munmap(ptr, size);
    }
};
using MappedMemory = std::unique_ptr<void, MunmapDeleter>;

// Usage:
MappedMemory mapping(
    ::mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0),
    MunmapDeleter{size}
);
if (mapping.get() == MAP_FAILED)
    // handle error
```

---

## Error Catalogue

| errno          | Function(s)             | Meaning                                                                             | Correct handling                                                               |
| -------------- | ----------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `EACCES`       | `shm_open()`            | Permission denied to open or unlink                                                 | Check permissions; verify process UID matches object owner                     |
| `EEXIST`       | `shm_open()`            | `O_CREAT \| O_EXCL` and object already exists                                       | Handle leftover from previous crash; `shm_unlink()` and retry, or report error |
| `EINVAL`       | `shm_open()`            | Name format invalid (e.g., just `/`, embedded slashes, empty)                       | Validate name before calling                                                   |
| `ENOENT`       | `shm_open()`            | Object does not exist and `O_CREAT` not specified                                   | Producer has not created it yet; retry or fail                                 |
| `ENOENT`       | `shm_unlink()`          | Object name does not exist                                                          | Already unlinked; treat as success in cleanup paths                            |
| `EMFILE`       | `shm_open()`            | Per-process fd limit reached                                                        | Log error; return failure                                                      |
| `ENFILE`       | `shm_open()`            | System-wide fd limit reached                                                        | Log error; return failure                                                      |
| `ENAMETOOLONG` | `shm_open()`            | Name exceeds `PATH_MAX` / `NAME_MAX`                                                | Validate name length before calling                                            |
| `EBADF`        | `ftruncate()`, `mmap()` | Invalid or closed fd                                                                | Ensure fd is open and valid                                                    |
| `EINVAL`       | `ftruncate()`           | `length` is negative or fd does not refer to a regular file or shared memory object | Validate length; ensure fd is from `shm_open()`                                |
| `EBADF/EINVAL` | `ftruncate()`           | fd is not open for writing                                                          | Use `O_RDWR` in `shm_open()` before `ftruncate()`                              |
| `ENOMEM`       | `mmap()`                | Insufficient virtual address space or memory                                        | Log error; return failure                                                      |
| `EACCES`       | `mmap()`                | `PROT_WRITE` requested but fd opened with `O_RDONLY`                                | Use `O_RDWR` in `shm_open()` if write access needed                            |
| `EINVAL`       | `mmap()`                | `length` is 0, `offset` not page-aligned, or no `MAP_SHARED`/`MAP_PRIVATE`          | Validate arguments                                                             |
| `SIGBUS`       | Memory access           | Accessed beyond the end of the mapped region                                        | Never access beyond `ftruncate()`-set size; bounds-check all accesses          |

---

## Best Practices

1. **Always call `ftruncate()` before `mmap()`** for newly created objects. A new shared memory object has size 0; mapping it without first setting a size results in `SIGBUS` on any access.

2. **Close the fd after `mmap()`**. The mapping persists independently of the fd. Keeping the fd open unnecessarily consumes a limited resource.

3. **Use `O_CREAT | O_EXCL` for exclusive creation**. The combination is atomic: it either creates the object or fails with `EEXIST`. This prevents two processes from both thinking they are the creator.

4. **Handle `EEXIST` from a previous crash**. If `O_CREAT | O_EXCL` returns `EEXIST`, a leftover object from a previous process may exist. The creator must decide whether to `shm_unlink()` the stale object and recreate it, or fail.

5. **Always synchronize concurrent access**. Shared memory provides no synchronization. Use POSIX unnamed semaphores (`sem_init()` with `pshared=1`) placed inside the shared region, or `pthread_mutex_t` with `PTHREAD_PROCESS_SHARED`. Never access shared data without holding the appropriate lock.

6. **Use restrictive permissions** (`0600`) unless cross-user sharing is explicitly required. Objects in `/dev/shm` are visible to all users who can access the path.

7. **`shm_unlink()` only removes the name; it does not free memory immediately**. The memory is freed only when all processes have `munmap()`-ed the region. The creator should `shm_unlink()` after creating and mapping, allowing the memory to exist as long as there are live mappings without leaving a filesystem name that other processes could unexpectedly open.

8. **Read-only consumers must use `O_RDONLY` + `PROT_READ`**. This enforces OS-level write protection on the consumer's mapping. Attempting to write to a `PROT_READ`-only mapping results in `SIGSEGV`.

9. **`offset` in `mmap()` must be page-aligned**. Use `0` for the start of the shared region. If a non-zero offset is needed, align it to `sysconf(_SC_PAGE_SIZE)`.

10. **Never access beyond `ftruncate()`-set size**. Accessing memory beyond the end of the shared object generates `SIGBUS`. Always bounds-check pointer arithmetic.

11. **Use RAII wrappers in C++14** to guarantee `munmap()` and `shm_unlink()` on scope exit. Use `std::unique_ptr` with a custom deleter for the mapping pointer. This prevents leaks in error and exception paths.

12. **Do not mix POSIX shared memory (`shm_open`) with System V shared memory (`shmget`)**. They are separate APIs; using both creates confusion and is unnecessary on any modern Linux system.

---

## Domain Glossary

This glossary classifies terms for use in requirements. Black-box terms describe externally observable behaviour and are allowed at any requirement level. White-box terms describe internal implementation details and are restricted to SWE.3 / SWE.4 artefacts only.

### Black-Box Terms (approved for SWE.1 requirements)

**shared memory segment**
Definition: A named, kernel-managed memory region that multiple processes can access simultaneously via virtual address mapping.
Rationale: The existence, name, and accessibility of the segment are observable to all participating processes. Creating, mapping, and removing a segment are observable lifecycle transitions.

**shared memory name**
Definition: The string identifier used to reference a shared memory segment, in the format `/somename`.
Rationale: The name is a required input to the create and attach operations and is visible in `/dev/shm`. It is the primary observable identifier for the segment.

**segment size**
Definition: The number of bytes available in the shared memory segment, set by the creator and observable via `fstat()`.
Rationale: Governs the bounds of all access operations; exceeding it produces `SIGBUS`. Observable by any process that opens the segment.

**producer**
Definition: The process responsible for creating the shared memory segment, setting its size, and writing data into it.
Rationale: The producer and consumer roles are observable in the system's concurrency model; they define the direction of data flow.

**consumer**
Definition: The process that attaches to an existing shared memory segment to read (and optionally write) data.
Rationale: See "producer".

**shared memory mapping**
Definition: The act of making a shared memory segment accessible within a process's virtual address space so the process can read or write it directly.
Rationale: Mapping is a discrete, observable operation with a success/failure outcome visible to the calling process.

**synchronization primitive**
Definition: A mechanism — such as a semaphore or mutex — used to coordinate concurrent access to shared memory between processes, ensuring data consistency.
Rationale: The need for synchronization and its outcome (exclusive access, wait, signal) are behaviorally observable even if the specific primitive is an implementation choice.

**segment lifecycle**
Definition: The sequence of observable states a shared memory segment passes through: created, mapped, accessible, unmapped, removed.
Rationale: Each transition is an observable system event. The lifecycle governs resource management requirements.

### White-Box Terms (restricted to SWE.3 / SWE.4 artefacts)

**`shm_open()` / `shm_unlink()`**
Definition: POSIX library functions that create/open or remove a named shared memory object.
Rationale: OS-API implementation detail. The observable behaviour is "segment created" or "segment removed", not the function call used to achieve it.

**`ftruncate()`**
Definition: System call that sets the size of a shared memory object.
Rationale: An internal setup step. The observable outcome is the segment having a usable size; the mechanism is `ftruncate()`.

**`mmap()` / `munmap()`**
Definition: System calls that map/unmap the shared memory object into virtual address space.
Rationale: Virtual memory management implementation detail. The observable outcome is "segment accessible" or "segment no longer accessible".

**file descriptor**
Definition: The integer kernel handle returned by `shm_open()`, used to call `ftruncate()` and `mmap()` before it can be closed.
Rationale: Internal OS resource handle; not visible at the application API level.

**`MAP_SHARED`**
Definition: An `mmap()` flag that ensures writes are visible to all other processes mapping the same region.
Rationale: `mmap()` flag selection is a C implementation detail.

**`PROT_READ` / `PROT_WRITE`**
Definition: `mmap()` protection flags controlling read/write access on the mapped pages.
Rationale: OS memory protection mechanism; belongs in SWE.3.

**`O_CREAT` / `O_EXCL` / `O_RDWR` / `O_RDONLY`**
Definition: `shm_open()` flags specifying creation mode and access.
Rationale: C API flags; belong in SWE.3 detailed design.

**`tmpfs`**
Definition: The Linux virtual filesystem (mounted at `/dev/shm`) where POSIX shared memory objects are stored.
Rationale: Filesystem implementation detail of the Linux kernel. Not visible to the application at requirement level.

**`sem_init()` / `pthread_mutex_t` with `PTHREAD_PROCESS_SHARED`**
Definition: POSIX primitives for placing semaphores or mutexes inside shared memory for cross-process synchronization.
Rationale: Synchronization mechanism selection is a SWE.3 design decision. SWE.1 requires "access shall be synchronized"; SWE.3 specifies how.

**`SIGBUS`**
Definition: Signal raised when a process accesses a memory address beyond the end of the mapped shared memory object.
Rationale: A low-level OS signal indicating an implementation-level bounds violation. The SWE.1 concern is "access shall not exceed segment size"; `SIGBUS` is the OS mechanism that enforces this.
