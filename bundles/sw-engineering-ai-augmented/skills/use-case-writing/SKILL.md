---
name: use-case-writing
description: "Use when writing or reviewing use-case files. Provides common patterns, rules and examples."
---

# Use case writing skill

This skill provides common patterns and rules for the documentation of use cases.

## Overview

Use-case files (`doc/<component>/use_cases/<use_case_identifier>.md`) describe observable black-box behavior from the perspective of the user or an external actor. Even when the product specification may include hints or internal details, use cases must remain independent of those details.

## Use of abbreviations

Use only abbreviations that are defined in the glossary. Write terms in full everywhere else, for example, write "file descriptor" instead of "fd", or "shared memory" instead of "shm".

## No API names or symbols

Never name standard library functions, system calls, flags, options, or error codes in the use-case prose. Describe the externally observable black-box behavior in plain text.

Examples:
| DO NOT write                | CORRECT |
|-----------------------------|---------|
| `memfd_create()`            | creates an anonymous memory segment |
| `mmap()`, `munmap()`        | maps / unmaps the segment into the address space |
| `ftruncate()`               | sets the segment size |
| `fcntl(F_ADD_SEALS, ...)`   | seals the segment against size modification |
| `accept()`                  | accepts the incoming connection |
| `poll()` , `select()`       | checks for pending socket events |
| `bind()` , `listen()`       | binds to the path and starts listening |
| `connect()`                 | requests the Client to connect to the Server at the path provided by the Application |
| `getsockopt(SO_PEERCRED)`   | reads the kernel-verified process identity |
| `sendmsg` + `SCM_RIGHTS`    | transmits the file descriptor via inter-process transfer |
| `recvmsg` + `SCM_RIGHTS`    | receives the file descriptor |
| `SOCK_CLOEXEC`, `O_CLOEXEC` | configured to prevent inheritance by child processes |
| `PROT_READ`, `PROT_WRITE`   | with read and write access |
| `read()` returns 0          | detects the connection has closed |
| `unlink()`                  | removes the socket file |
| `ENOENT`, `ECONNREFUSED`    | server is not reachable at the path |
| `system call`, `syscall`    | platform operation |

## No internal data structures

Never mention internal storage mechanisms such as arrays, lists, maps, buffers, queues, or other data structures. Describe only the observable capacity limits and behavioral outcomes.

Examples:
| DO NOT write | CORRECT use |
|--------------|-------------|
| selects an unused entry in the internal array | not externally observable; part of initialization of the actor or instance |
| releases the entry in the internal array | not externally observable; part of cleanup of the actor or instance|
| the internal client handling array |not externally observable; implied by the component's use of one or more client handling instances |
| fixed-size array of structures | describe the capacity limits instead, e.g., "up to the maximum number of simultaneous Clients" |
| stores the handle in a hash map | not externally observable; part of internal management of the actor or instance |

## No concrete error, status, flags, or option names

Never use implementation-style flags, options, status or code names/symbols in the use-case prose. Describe outcomes in plain text.

Examples:
| DO NOT write          | CORRECT |
|-----------------------|---------|
| `INTERNAL`            | internal error |
| `UNAVAILABLE`         | connection unavailable |
| `INVALID_ARGUMENT`    | invalid argument |
| `RESOURCE_EXHAUSTED`  | resource exhausted |
| `FAILED_PRECONDITION` | precondition violation |
| `DATA_LOSS`           | segment reception failure |
| `PERMISSION_DENIED`   | connection rejected |
| `POLLING`             | polling |
| `EVENT_DRIVEN`        | event-driven |
| `READ_ONLY`           | read-only |
| `READ_WRITE`          | read-write |

## Failure path sentence structure

Every failure path item follows a strict sentence order: **log first, then reject/return**. The log action is the diagnostic step; the rejection/return is the final observable outcome.

**Patterns:**
```
<Actor> logs a/an <severity-level> [with <details>] and rejects the request with a/an "<status>" status.
<Actor> logs a/an <severity-level> [with <details>] and returns "<status>".
```
**Log severity levels**

Use "fatal error" for errors that make the component non-functional; "error" for recoverable failures; "warning" for unexpected but non-fatal conditions.

**Quote the status name**

Wrap the status in double quotes, e.g., `"invalid argument"`, `"internal error"`, `"connection unavailable"`, to distinguish it from regular prose of a use case.

Examples:
| DO NOT write| CORRECT |
|---|---|
| Server rejects the request with an invalid argument; logs fatal. | Server logs a fatal error and rejects the request with an "invalid argument" status. |
| Client rejects the request with an internal error; logs fatal with the system error. | Client logs a fatal error with the system error and rejects the request with an "internal error" status. |
| Client rejects the request with connection unavailable; logs error with the path. | Client logs an error with the socket path and system error and rejects the request with a "connection unavailable" status. |
| returns `EOVERFLOW` | Application rejects the request with an "arithmetic overflow" status |

## Failure paths of system operations

Every step that involves a system operation (e.g., socket operations, polling, sending, receiving, closing) can fail. Use cases must include a failure path for each such step, unless the step truly has no failure outcomes.

If a system operation appears in multiple steps, use the step number in the failure path for disambiguation (e.g., "If a system error occurs while <operation> (step N), ...").

Patterns:
| Scenario | Possible failure path |
|---|---|
| Pending event processing | If a system error occurs while checking for pending socket events (step N), the Actor logs an error with the system error and returns the error to the Application. |
| Sending a message | If a system error occurs while sending the command, the Actor logs an error with the system error and rejects the request with an "internal error" status. |
| Releasing a resource (best effort) | If a system error occurs while closing the communication socket, the Actor logs a warning with the system error. Cleanup still proceeds. |
| Connection closed during operation (handled as in other use case) | If the communication socket is closed during ..., the Actor logs an error and handles the disconnection as described in [use-case-identifier](use-case-file-name.md). |

## Two-phase construction of resource-acquiring components

Components that acquire system resources (e.g., sockets, file descriptors, memory) follow a two-phase model:

**Phase 1: Construction:**
- The user (or an external actor) creates the component (or a `<Role>` instance).
- The construction acquires no system resources.
- The construction cannot fail.
- The construction accepts no configuration parameters related to the to-be-acquired resources.
- The construction may include parameters, which are independent of needed system resources and cannot cause construction failure.

**Phase 1b: Setup (optional):**
- The user performs any necessary setup needed for correct component operation before resource acquisition. This may include, for example, registration of notification handlers.

**Phase 2: Activation:**
- The user requests the component to perform the resource-acquiring work (e.g., start listening, connect to a server).
- The user provides **all required parameters** for resource acquisition (e.g., the socket path).
- The activation step validates the parameters (validation may fail -> failure path).
- The resource acquisition is performed so that all needed system resources are acquired and set up for the correct component operation; or it fails and any partially acquired resources are released (any failed resource acquisition -> failure path).

**Why no constructor parameters?** A constructor cannot meaningfully fail; there is no return channel for errors. By deferring all parameter acceptance and validation to the activation step, failures can be reported cleanly through the normal error path.

**Vocabulary:**
- Use "creates a `<Role>` instance" in phrasing of the construction step. Never use "creates the `<Role>`".
- Use "requests the `<Role>` to `<action>`" in phrasing of the activation step.

Examples:
| Step         | Example |
|--------------|---------|
| Construction | Application creates a Server instance. No system resources are acquired. |
| Setup        | Application registers notification handler for "event-name".<br>Application registers notification handlers for "event-name-1", ...|
| Activation   | Application requests the Server to start listening, providing the socket path.<br>The Server validates that the path is non-empty.<br>Resource-acquiring work step by step. |

---

## Example: Calculator

### Product specification (`doc/<component>/product_specification/calculator.md`)

```markdown
# Calculator library - concept

The library provides a calculator component that performs basic arithmetic operations on integers.

## Supported operations

The calculator supports the following operations:

### Sum

The calculator can compute the sum of two integers. If the result exceeds the representable integer range, the operation is rejected with an "arithmetic overflow" status.

...
```

### Use case file (`doc/<component>/use_cases/uc_calculator_sum.md`)

```markdown
# uc:calculator-sum

Application requests the Calculator to add two integers and retrieve the sum.

**Precondition:** None. This is a standalone use case with no prior setup.

**Normal flow:**

1. Application creates a Calculator instance. No system resources are acquired.
2. Application provides two integer operands and requests the Calculator to compute their sum.
3. The Calculator checks whether the addition would exceed the representable integer range.
4. The Calculator adds the operands and returns the result to the Application.

**Result:** The Application holds the computed sum. The Calculator remains ready for further operations.

**Failure paths:**

* If the addition would overflow the representable integer range (step 3), the Calculator logs an error and rejects the request with an "arithmetic overflow" status.

**Precondition for:** None. No other use case depends on this one.

**Reference:** [Calculator Concept](../product_specification/calculator.md#sum)

[back to index](./index.md)
```
