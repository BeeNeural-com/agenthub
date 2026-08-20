---
name: unix-domain-sockets
description: "Unix Domain Sockets (UDS) API reference and implementation patterns. Use when designing or implementing Unix Domain Socket IPC in C++ for E3 Software Platform components."
---

# Unix Domain Sockets (UDS)

## Official References

| Document                                         | URL                                                 | Version                     |
| ------------------------------------------------ | --------------------------------------------------- | --------------------------- |
| `unix(7)` — Overview of AF_UNIX sockets          | https://man7.org/linux/man-pages/man7/unix.7.html   | man-pages 6.16 (2025-09-21) |
| `socket(2)` — Create a communication endpoint    | https://man7.org/linux/man-pages/man2/socket.2.html | man-pages 6.16 (2025-10-29) |
| `bind(2)` — Bind a name to a socket              | https://man7.org/linux/man-pages/man2/bind.2.html   | man-pages 6.16 (2025-10-29) |
| `listen(2)` — Listen for connections             | https://man7.org/linux/man-pages/man2/listen.2.html | man-pages 6.16 (2025-10-29) |
| `accept(2)` / `accept4(2)` — Accept a connection | https://man7.org/linux/man-pages/man2/accept.2.html | man-pages 6.16 (2025-10-29) |
| `poll(2)` — Wait for events on file descriptors  | https://man7.org/linux/man-pages/man2/poll.2.html   | man-pages 6.16 (2025-10-29) |

Standard: POSIX.1-2024. All APIs are available on Linux ≥ 2.6.28 and glibc ≥ 2.10.

---

## Overview

Unix Domain Sockets (`AF_UNIX`, also `AF_LOCAL`) provide efficient local IPC between processes on the same machine. They use the standard BSD socket API but communicate through the kernel's socket layer instead of a network stack.

Three socket types are supported:

| Type             | Semantics                                      | Boundary preserved | Connection needed |
| ---------------- | ---------------------------------------------- | ------------------ | ----------------- |
| `SOCK_STREAM`    | Ordered, reliable byte stream                  | No                 | Yes (`connect`)   |
| `SOCK_DGRAM`     | Datagram (always reliable on UDS)              | Yes                | No                |
| `SOCK_SEQPACKET` | Ordered, reliable, message-boundary-preserving | Yes                | Yes (`connect`)   |

For server–client IPC with framed messages, `SOCK_SEQPACKET` is preferred; for raw byte streaming, `SOCK_STREAM` is used.

### Address types

A UDS address is represented in `struct sockaddr_un` (`<sys/un.h>`):

```c
struct sockaddr_un {
    sa_family_t sun_family;   /* AF_UNIX */
    char        sun_path[108]; /* Pathname (Linux: 108 bytes) */
};
```

Three address variants exist:

| Variant      | Description                                                    | Cleanup required                      |
| ------------ | -------------------------------------------------------------- | ------------------------------------- |
| **Pathname** | Bound to a filesystem path; creates a socket-type file         | Yes — `unlink(path)`                  |
| **Unnamed**  | Not bound; used for connected endpoints returned by `accept()` | No                                    |
| **Abstract** | `sun_path[0] == '\0'`; no filesystem entry; Linux-specific     | No — auto-removed when last fd closed |

**Portable code must use pathname sockets** and always `unlink()` the path on shutdown. Abstract sockets are a Linux extension and must not be used in portable (POSIX) code.

---

## API Reference

### `socket(2)`
```c
#include <sys/socket.h>
int socket(int domain, int type, int protocol);
```
- `domain`: `AF_UNIX`
- `type`: `SOCK_STREAM | SOCK_CLOEXEC` (combine with `SOCK_NONBLOCK` if needed)
- `protocol`: `0` (only one protocol per type in AF_UNIX)
- Returns: new fd (≥ 0) on success; `-1` on error (`errno` set)
- **Always OR in `SOCK_CLOEXEC`** at creation to avoid fd leaks across `exec()`.

### `bind(2)`
```c
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```
- Assigns a pathname to the socket; creates a socket-type file in the filesystem.
- `addrlen` should be `sizeof(struct sockaddr_un)` for maximum portability.
- Always `memset(&addr, 0, sizeof(addr))` before use (clears non-standard fields on some platforms).
- Returns: `0` on success; `-1` on error.

### `listen(2)`
```c
int listen(int sockfd, int backlog);
```
- Marks the socket as passive (server side).
- `backlog`: maximum length of the pending-connection queue. Values above `/proc/sys/net/core/somaxconn` are silently capped (default 4096 since Linux 5.4, 128 before).
- Returns: `0` on success; `-1` on error.

### `accept(2)` / `accept4(2)`
```c
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
int accept4(int sockfd, struct sockaddr *addr, socklen_t *addrlen, int flags);
```
- Extracts the first pending connection and returns a **new** connected fd.
- `flags` (accept4 only): `SOCK_CLOEXEC`, `SOCK_NONBLOCK`.
- **On Linux, the new fd does NOT inherit `O_NONBLOCK` from the listening socket.** Always set flags explicitly via `accept4()`.
- **Prefer `accept4()` with `SOCK_CLOEXEC`** over `accept()` followed by `fcntl()`.
- Returns: new fd (≥ 0) on success; `-1` on error.

### `connect(2)`
```c
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```
- Initiates a connection to the server at the given path.
- For `AF_UNIX SOCK_STREAM` (blocking): the kernel creates a socket pair in-kernel and places the new server-side fd into the server's accept queue. `connect()` returns `0` as soon as the connection is in the queue — **the server does not need to call `accept()` first**.
- For `AF_UNIX SOCK_STREAM` (non-blocking): returns `-1` with `errno = EAGAIN` if the connection cannot complete immediately. Note: **AF_UNIX uses `EAGAIN`, not `EINPROGRESS`** — `EINPROGRESS` is TCP-specific.
- If the server's accept queue (backlog) is full: returns `-1` with `errno = ECONNREFUSED` immediately. AF_UNIX does not retry.
- Returns: `0` on success; `-1` on error.

### `send(2)` / `recv(2)`
```c
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```
- **Always use `MSG_NOSIGNAL` flag on `send()`** to suppress `SIGPIPE` when the peer closes the connection. Without it, `SIGPIPE` is delivered to the process and may terminate it.
- Returns: bytes sent/received on success; `-1` on error; `0` on `recv()` indicates peer has closed the connection.

### `poll(2)`
```c
#include <poll.h>
int poll(struct pollfd *fds, nfds_t nfds, int timeout);
```
- Monitors a set of fds for I/O events.
- Key event flags: `POLLIN` (data available or connection pending), `POLLHUP` (peer closed), `POLLERR` (error), `POLLRDHUP` (peer shut down write end; requires `_GNU_SOURCE`).
- `timeout = -1` blocks indefinitely; `timeout = 0` returns immediately.
- Returns: number of fds with non-zero `revents`; `0` on timeout; `-1` on error.
- **`POLLHUP` can appear together with `POLLIN`** when the peer has closed but data is still readable. Always drain all data before treating `POLLHUP` as a disconnect.

### `close(2)` + `unlink(2)`
```c
int close(int fd);
int unlink(const char *pathname);
```
- `close(listening_fd)` closes the acceptor socket at the OS level. Rejects all further `accept()` calls immediately.
- `unlink(path)` removes the socket file from the filesystem. Must be called explicitly by the server; the kernel does NOT auto-remove pathname socket files.

---

## Lifecycle & Usage Pattern

### Server

```
socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0)   → listening_fd
  ↓
[unlink(path) if stale file exists]               → clean path
  ↓
bind(listening_fd, &addr, sizeof(addr))           → socket file created
  ↓
listen(listening_fd, SOMAXCONN)                   → marks socket as passive
  ↓
loop:
  poll({listening_fd, POLLIN}, ...)               → waits for incoming connection
  accept4(listening_fd, NULL, NULL, SOCK_CLOEXEC) → connected_fd (new per-client fd)
  [read/write on connected_fd]
  close(connected_fd)                             → releases per-client resources
  ↓ (shutdown)
close(listening_fd)                               → stops accepting new connections
unlink(path)                                      → removes socket file from filesystem
```

### Client

```
socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0)   → sockfd
  ↓
connect(sockfd, &addr, sizeof(addr))              → establishes connection
  ↓
send(sockfd, buf, len, MSG_NOSIGNAL)              → sends data
recv(sockfd, buf, len, 0)                         → receives data
  ↓
close(sockfd)                                     → terminates connection
```

### Event-driven (polling) variant

Use `poll()` before `accept()` and before each `recv()` to avoid blocking:

```c
struct pollfd pfd = { .fd = listening_fd, .events = POLLIN };
int ret = poll(&pfd, 1, timeout_ms);
if (ret > 0 && (pfd.revents & POLLIN)) {
    int cfd = accept4(listening_fd, NULL, NULL, SOCK_CLOEXEC);
}
```

---

## Connection Establishment Mechanics (AF_UNIX SOCK_STREAM)

### The single accept queue

TCP uses two queues: an incomplete connections queue (SYN received, waiting for ACK) and a completed connections queue (three-way handshake done). **AF_UNIX SOCK_STREAM has only one queue** — the completed-connections (accept) queue — because there is no network handshake. The `backlog` argument to `listen()` sizes this single queue.

### What `connect()` actually does

For a blocking `AF_UNIX SOCK_STREAM` socket:

1. The kernel creates a socket pair entirely in kernel space — no network roundtrip, no handshake, no message exchange between the two processes.
2. The server-side fd of that pair is placed into the server's accept queue.
3. `connect()` returns `0` to the client.

**The server process is not involved and is not woken up.** `connect()` returns success before the server calls `accept()`. This is the authoritative reason why a client can read a success status back from `connect()` before the server has processed the connection.

### What `accept()` actually does

`accept()` (and `accept4()`) **dequeues** the first entry from the accept queue and returns a file descriptor pointing to the already-established server-side socket. It does not establish the connection — the connection was fully established inside `connect()`.

```
Client                   Kernel accept queue          Server process
─────────────────────    ──────────────────────────   ─────────────────
connect()          ───►  connection placed in queue   (not involved)
            ◄───         returns 0
                                                  ◄── accept4() dequeues it
```

### Data buffering before `accept()`

Because the connection is established at `connect()` time, the client can call `send()` immediately after `connect()` returns — even before the server calls `accept()`. The kernel buffers the data in the socket's send/receive buffer. When the server eventually calls `accept()` and then `recv()`, the data is already waiting. There is no data loss.

### Backlog full behaviour

If `connect()` is called when the server's accept queue is already at the `backlog` limit:
- The kernel returns `ECONNREFUSED` to the client immediately.
- Unlike TCP (which may silently drop and allow the client to retry via retransmission), AF_UNIX returns the error synchronously.
- The server does not observe this event — the connection never entered the queue.

### Non-blocking `connect()` for AF_UNIX

For a non-blocking AF_UNIX SOCK_STREAM socket, if the connection cannot complete immediately:
- Returns `-1` with `errno = EAGAIN` (not `EINPROGRESS` — that is TCP-specific).
- Use `poll()` for `POLLOUT` writability to detect completion, then `getsockopt(SO_ERROR)` to check outcome.

---

## Error Catalogue

| errno                    | Syscall(s)             | Meaning                                                                                    | Correct handling                                                           |
| ------------------------ | ---------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `EADDRINUSE`             | `bind()`               | Path already exists as a socket file                                                       | Check for stale file; `unlink()` then retry, or report error               |
| `ENOENT`                 | `bind()`               | A directory component in the path does not exist                                           | Ensure the directory exists before `bind()`                                |
| `ENOENT`                 | `connect()`            | No socket file at the given path                                                           | Server is not running or path is wrong; return failure                     |
| `ECONNREFUSED`           | `connect()`            | Socket file exists but no one is listening, or the server's accept queue (backlog) is full | Server has crashed or is temporarily at capacity; return failure           |
| `EISCONN`                | `connect()`            | Socket is already connected                                                                | Application error; reject with "already connected"                         |
| `EPIPE`                  | `send()`               | Peer has closed the connection                                                             | Expected disconnect; return failure. Use `MSG_NOSIGNAL` to avoid `SIGPIPE` |
| `ECONNRESET`             | `recv()`               | Peer closed connection unexpectedly                                                        | Treat as disconnect; release resources                                     |
| `EAGAIN` / `EWOULDBLOCK` | `accept()`, `recv()`   | Non-blocking mode; no connection/data ready                                                | Not an error; schedule retry via `poll()`                                  |
| `EINTR`                  | Any blocking call      | Interrupted by signal before completion                                                    | Retry the syscall in a loop                                                |
| `EMFILE`                 | `socket()`, `accept()` | Per-process fd limit reached                                                               | Log error; return failure; do not crash                                    |
| `ENFILE`                 | `socket()`, `accept()` | System-wide fd limit reached                                                               | Log error; return failure                                                  |
| `EINVAL`                 | `bind()`               | `sockaddr_un.sun_path` is empty or `addrlen` is wrong                                      | Validate path before calling `bind()`                                      |

---

## Best Practices

1. **Always use `SOCK_CLOEXEC`** when creating sockets (`socket()`) and when accepting connections (`accept4()`). This prevents fd leaks when child processes are spawned via `exec()`.

2. **Remove stale socket files before `bind()`**. After abnormal termination, the socket file remains on the filesystem. A new server must `unlink()` it before calling `bind()`, or `EADDRINUSE` will occur.

3. **Always `unlink()` the socket file on graceful shutdown**. The kernel does not automatically remove pathname socket files. Failure to unlink leaves a stale file that will block the next server start.

4. **Use `memset(&addr, 0, sizeof(addr))` before filling `sockaddr_un`**. Some non-Linux implementations include additional fields before `sun_path`. Zero-filling ensures portability.

5. **Limit `sun_path` to 107 bytes** (107 bytes + null terminator = 108 bytes max). Paths longer than 107 characters cannot be represented. Use `strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1)`.

6. **Use `MSG_NOSIGNAL` on every `send()`**. Without it, a `SIGPIPE` is raised if the peer has closed its end. Unless `SIGPIPE` is explicitly blocked at the process level, this can silently terminate the process.

7. **Never assume `O_NONBLOCK` is inherited from `accept()`**. On Linux, the new socket returned by `accept()` does NOT inherit file status flags from the listening socket. Always use `accept4()` with `SOCK_NONBLOCK` if non-blocking I/O is required.

8. **Retry on `EINTR`**. All blocking syscalls (`poll()`, `accept()`, `send()`, `recv()`) can be interrupted by a signal. The correct response is to restart the syscall.

9. **Use `poll()` (or `epoll()`) for multiplexed servers**. Calling `accept()` in a blocking loop wastes a thread per connection. `poll()` allows a single thread to handle multiple fds.

10. **After `POLLHUP`, drain remaining data before closing**. `POLLHUP` can arrive together with `POLLIN` on a stream socket. Reading until `recv()` returns `0` ensures all data is consumed before the fd is closed.

11. **Always handle `EAGAIN`/`EWOULDBLOCK` on non-blocking sockets**. These are not errors; they indicate the operation would block. Schedule a `poll()` retry.

12. **Do not use abstract namespace sockets in production code** unless Linux-only operation is explicitly required and documented. Pathname sockets are portable to all POSIX systems.

---

## Domain Glossary

This glossary classifies terms for use in requirements. Black-box terms describe externally observable behaviour and are allowed at any requirement level. White-box terms describe internal implementation details and are restricted to SWE.3 / SWE.4 design and unit-test artefacts only.

### Black-Box Terms (approved for SWE.1 requirements)

**acceptor socket**
Definition: The socket whose role is to listen for and accept incoming client connections. Held by the server for the lifetime of the server instance.
Rationale: The acceptor socket is an observable domain entity with a defined role and lifecycle (created, bound, closed, removed). Its existence and lifecycle state are visible to both sides of the communication.

**socket path**
Definition: The filesystem path to which the acceptor socket is bound. Used by clients to locate and connect to the server.
Rationale: The path is an observable input provided by the application and appears in filesystem listings. It directly governs whether a connection attempt succeeds.

**socket file**
Definition: The filesystem object of type socket created by `bind()`. Its presence indicates that a server is listening or was previously listening at that path.
Rationale: Observable via `ls`, `stat`, and connection attempts; not an internal data structure.

**stale socket file**
Definition: A socket file left on the filesystem after abnormal server termination, with no active server behind it.
Rationale: Its presence causes `EADDRINUSE` on the next `bind()` call — an observable failure condition that drives explicit removal requirements.

**connect request**
Definition: The IPC operation by which a client initiates communication with the server.
Rationale: The connect request and its outcome (success / connection unavailable / rejected) are observable to the client application.

**event processing**
Definition: The act of triggering the library to check for and dispatch pending socket events (incoming connections, data, peer disconnections).
Rationale: Event processing is an explicit, application-triggered operation with an observable success/failure outcome. It is the mechanism through which all connection and data events are delivered to the application.

**pending connection**
Definition: A client connection that has completed the transport-level handshake but has not yet been accepted by the server.
Rationale: Observable: it sits in the server's accept queue and is visible to the application when `poll()` returns `POLLIN` on the acceptor socket.

**Client connection**
Definition: The per-client communication channel established between the server and a connected client after the server accepts the pending connection.
Rationale: The existence and state of a client connection is observable to both the server and client applications.

### White-Box Terms (restricted to SWE.3 / SWE.4 artefacts)

**`socket()` / `bind()` / `listen()` / `accept4()` / `connect()`**
Definition: POSIX system calls that implement the server and client socket lifecycle.
Rationale: These are OS-primitive calls. Naming them in a SWE.1 requirement couples the requirement to a specific OS API rather than the observable behaviour it produces.

**`sockaddr_un` / `sun_path`**
Definition: The C structure and field used to represent a UDS address.
Rationale: Data structure internals; belong in SWE.3 detailed design.

**file descriptor**
Definition: The kernel-managed integer handle returned by `socket()` and `accept4()` that refers to an open socket.
Rationale: An OS-level resource handle. Its existence is implementation detail; observable behaviour is "connection established" or "socket ready", not "file descriptor opened".

**`poll()` / `epoll()`**
Definition: System calls used to wait for I/O readiness on a set of file descriptors.
Rationale: The multiplexing mechanism is an implementation choice. The observable behaviour is "pending events are dispatched".

**`SOCK_CLOEXEC` / `FD_CLOEXEC`**
Definition: Flag that causes the socket fd to be closed automatically on `exec()`.
Rationale: A resource-safety implementation detail. Not observable at application level.

**`MSG_NOSIGNAL`**
Definition: A `send()` flag that suppresses `SIGPIPE` delivery when writing to a socket whose peer has closed.
Rationale: An implementation-level safety measure. The observable behaviour is "send returns a failure status"; the mechanism for achieving it is not SWE.1 material.

**`POLLHUP` / `POLLIN` / `POLLERR`**
Definition: Event flags returned by `poll()` indicating socket state changes.
Rationale: Internal polling primitives. Belong in SWE.3.

**dedicated communication socket**
Definition: The per-client connected socket returned by `accept4()` and used for all subsequent data exchange with that client.
Rationale: Internal architectural name for the per-client fd. The black-box term is "Client connection".

**connection slot**
Definition: Internal storage reserved for one active client connection within the server's client table.
Rationale: Internal capacity management concept. The black-box term is "server capacity" or is implicit in "compile-time maximum number of connected clients".
