---
name: uds-fd-passing
description: "UDS file descriptor passing via SCM_RIGHTS. Use when designing or implementing sendmsg/recvmsg-based FD transfer over AF_UNIX SOCK_STREAM sockets, including optional-FD protocol patterns where the sender may grant or reject an FD request."
---

# UDS File Descriptor Passing (SCM_RIGHTS)

This skill covers the `sendmsg(2)` / `recvmsg(2)` API for passing open file
descriptors over AF_UNIX sockets using the `SCM_RIGHTS` ancillary data
mechanism. It includes the exchange pattern with optional file descriptor, where the sender
may or may not attach a file descriptor to a message, and the receiver must detect
which case occurred.

---

## Overview

The Linux kernel allows a process to transfer an open file descriptor to
another process over a Unix Domain Socket (UDS). The transferred entity is
not the integer descriptor number itself, but a reference to the underlying
open file description. The receiving process obtains a new file descriptor
in its own descriptor table that refers to the same kernel file description.
The operation is semantically equivalent to calling `dup(2)` into the
receiving process's file descriptor table.

This mechanism is the standard way to hand a shared memory file descriptor
(`shm_open` result) from a server process to a client process without
exposing the shared memory object by name.

Key properties:

- Works on `SOCK_STREAM`, `SOCK_DGRAM`, and `SOCK_SEQPACKET` AF_UNIX sockets.
- The received file descriptor number is independent of the sender's file descriptor number.
- Passing is implemented through ancillary data, not through the normal
  data payload.
- On `SOCK_STREAM`, at least one byte of non-ancillary (real) data must be
  sent in the same `sendmsg(2)` call as the ancillary data. This is a
  hard requirement; a `sendmsg` with only a control message and no data
  bytes will silently discard the ancillary data on Linux.
- A sender can choose not to attach a file descriptor to a message. The receiver detects
  the absence of a file descriptor by checking whether `CMSG_FIRSTHDR` returns `NULL`
  after a successful `recvmsg(2)`.

Standard: POSIX.1-2008 (`CMSG_FIRSTHDR`, `CMSG_NXTHDR`, `CMSG_DATA`);
Linux extensions (`CMSG_SPACE`, `CMSG_LEN`, `CMSG_ALIGN`, `MSG_CMSG_CLOEXEC`).
Available on Linux >= 2.2. `MSG_CMSG_CLOEXEC` requires Linux >= 2.6.23.

---

## Reference / API

### `sendmsg(2)`

```c
#include <sys/socket.h>
ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);
```

- Sends a message that may contain both normal payload data and ancillary
  (control) data.
- `flags`: Use `MSG_NOSIGNAL` to suppress `SIGPIPE` on peer close, consistent
  with `send(2)` best practice.
- Returns: bytes of normal data sent on success; `-1` on error (`errno` set).

The `msghdr` structure used by `sendmsg(2)`:

```c
struct msghdr {
    void         *msg_name;       /* NULL for connected sockets */
    socklen_t     msg_namelen;    /* 0 for connected sockets */
    struct iovec *msg_iov;        /* Scatter-gather array for payload data */
    size_t        msg_iovlen;     /* Number of elements in msg_iov */
    void         *msg_control;    /* Pointer to ancillary data buffer */
    size_t        msg_controllen; /* Size of ancillary data buffer in bytes */
    int           msg_flags;      /* Ignored on send */
};
```

To send without a file descriptor (rejection path): set `msg_control = NULL` and
`msg_controllen = 0`. The normal data bytes are sent; no ancillary data is
attached.

### `recvmsg(2)`

```c
ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);
```

- Receives a message, filling the `msghdr` fields including any ancillary data.
- `flags`: **Always use `MSG_CMSG_CLOEXEC`** to set `FD_CLOEXEC` on any
  received file descriptors atomically. This prevents file descriptor leaks in processes
  that spawn children via `exec()`.
- On return, `msg->msg_controllen` is updated to the actual number of bytes
  of ancillary data received. If `msg->msg_flags` has `MSG_CTRUNC` set, the
  ancillary data was truncated: received file descriptors that did not fit were silently
  closed by the kernel.
- To detect that no file descriptor was attached: call `CMSG_FIRSTHDR(msg)` after a
  successful `recvmsg(2)`; a `NULL` return means no control message was
  present.
- Returns: bytes of normal data received; `0` on peer close; `-1` on error.

### `cmsg(3)` — Ancillary Data Macros

```c
#include <sys/socket.h>

struct cmsghdr *CMSG_FIRSTHDR(struct msghdr *msgh);
struct cmsghdr *CMSG_NXTHDR(struct msghdr *msgh, struct cmsghdr *cmsg);
size_t          CMSG_SPACE(size_t data_len);
size_t          CMSG_LEN(size_t data_len);
unsigned char  *CMSG_DATA(struct cmsghdr *cmsg);
size_t          CMSG_ALIGN(size_t length);
```

The control message header structure:

```c
struct cmsghdr {
    size_t cmsg_len;    /* Byte count including this header (use CMSG_LEN) */
    int    cmsg_level;  /* SOL_SOCKET for SCM_RIGHTS */
    int    cmsg_type;   /* SCM_RIGHTS */
    /* unsigned char cmsg_data[]; follows */
};
```

Macro semantics:

| Macro | Returns | Use |
| --- | --- | --- |
| `CMSG_SPACE(n)` | Total bytes for one control message with `n` bytes of data (header + padding) | Size the control buffer |
| `CMSG_LEN(n)` | Value to write into `cmsg_len` for `n` bytes of data | Set `cmsg_len` field |
| `CMSG_DATA(cmsg)` | Pointer to the data payload of the control message | Read/write the file descriptor array |
| `CMSG_FIRSTHDR(msg)` | Pointer to first `cmsghdr` in the buffer, or `NULL` if none | Detect / iterate ancillary |
| `CMSG_NXTHDR(msg, cmsg)` | Pointer to next `cmsghdr`, or `NULL` if none | Iterate multiple messages |
| `CMSG_ALIGN(n)` | `n` rounded up to alignment boundary | Internal use; rarely called directly |

`CMSG_DATA()` returns an `unsigned char *` that is not guaranteed to be
suitably aligned for all types. Always use `memcpy` to read or write the
file descriptor array through this pointer; never cast it directly to `int *`.

### `SCM_RIGHTS`

```c
#include <sys/socket.h>   /* SOL_SOCKET, SCM_RIGHTS */
```

- `cmsg_level = SOL_SOCKET`
- `cmsg_type  = SCM_RIGHTS`
- Data payload: an `int[]` array of file descriptor numbers to transfer.
- Maximum file descriptor count per `sendmsg` call: `SCM_MAX_FD` = 253 (Linux >= 2.6.38;
  255 on earlier kernels).
- The receiving process obtains new file descriptor numbers that reference the same kernel
  file descriptions as the sender's file descriptors. The sender's file descriptors are unaffected.
- If the receiver's ancillary buffer is too small or absent, excess received
  file descriptors are silently closed by the kernel. `MSG_CTRUNC` is set in
  `msg->msg_flags`.

### Alignment Union (Required Buffer Pattern)

The control buffer must be correctly aligned for `cmsghdr`. Use a union:

```c
union {
    char           buf[CMSG_SPACE(sizeof(int))];  /* one fd */
    struct cmsghdr align;
} ctrl;
```

This pattern is the canonical idiom from `cmsg(3)` examples. It guarantees
that `ctrl.buf` is aligned for `struct cmsghdr` access without requiring a
separate `aligned_alloc`.

---

## Lifecycle & Usage Pattern

### Sender: Grant (attach file descriptor)

```
Build msghdr:
  msg_iov  → {.iov_base = &tag_byte, .iov_len = 1}   /* mandatory payload */
  msg_control → ctrl.buf (union)
  msg_controllen → CMSG_SPACE(sizeof(int))

Fill cmsghdr:
  cmsg = CMSG_FIRSTHDR(&msg)
  cmsg->cmsg_level = SOL_SOCKET
  cmsg->cmsg_type  = SCM_RIGHTS
  cmsg->cmsg_len   = CMSG_LEN(sizeof(int))
  memcpy(CMSG_DATA(cmsg), &shm_fd, sizeof(int))

sendmsg(sockfd, &msg, MSG_NOSIGNAL)           → sends tag byte + FD
close(shm_fd) [optional, if sender no longer needs it]
```

### Sender: Reject (no file descriptor attached)

```
Build msghdr:
  msg_iov  → {.iov_base = &tag_byte, .iov_len = 1}   /* mandatory payload */
  msg_control    = NULL
  msg_controllen = 0

sendmsg(sockfd, &msg, MSG_NOSIGNAL)           → sends tag byte, no ancillary
```

### Receiver: Detect FD Presence

```
Provide control buffer:
  ctrl.buf[CMSG_SPACE(sizeof(int))] (union) — zero-initialize

Build msghdr:
  msg_iov  → {.iov_base = &tag_byte, .iov_len = 1}
  msg_control    = ctrl.buf
  msg_controllen = sizeof(ctrl.buf)

recvmsg(sockfd, &msg, MSG_CMSG_CLOEXEC)      → reads 1 byte + optional FD

if (msg.msg_flags & MSG_CTRUNC):
    /* ancillary was truncated; received fds (if any) were closed */
    handle_error()

cmsg = CMSG_FIRSTHDR(&msg)
if (cmsg == NULL):
    /* sender rejected; no FD attached */
    handle_rejection()
else if (cmsg->cmsg_level == SOL_SOCKET && cmsg->cmsg_type == SCM_RIGHTS):
    int received_fd;
    memcpy(&received_fd, CMSG_DATA(cmsg), sizeof(int))
    /* use received_fd; close it when done */
```

### Integration with an Existing Byte-Stream Framing Protocol

Many `SOCK_STREAM` IPC libraries use a simple length-prefixed framing
protocol: a fixed-size header (containing the payload length) followed by
the payload bytes. The existing `send(2)` / `recv(2)` helpers used for that
framing cannot carry ancillary data.

The recommended approach is to insert a dedicated **FD-exchange step** as a
separate, single-byte `sendmsg` / `recvmsg` call. This step is isolated from
the normal message framing and carries the optional FD signal.

**Protocol sequence for an FD request / response:**

```
Client → Server:  [framed request message]          (send/recv as normal)
Server → Client:  [1-byte tag via sendmsg]           (with or without SCM_RIGHTS)
Client:           recvmsg for 1 byte + control buffer → detect FD presence
```

The 1-byte payload (the "tag byte") can encode the server's decision:

| Tag value | Meaning | Ancillary data |
| --- | --- | --- |
| `0x01` | file descriptor granted | `SCM_RIGHTS` cmsghdr carrying the shm fd |
| `0x00` | file descriptor rejected | None (`msg_control = NULL`) |

The receiver always calls `recvmsg` for this step, with a fully provisioned
control buffer. It checks the tag value first (fast path), then checks
`CMSG_FIRSTHDR` to confirm ancillary presence. Both checks must agree; a
mismatch indicates a protocol error.

**Why a dedicated byte rather than embedding in the framed message:**

On `SOCK_STREAM`, the kernel anchors ancillary data to the byte(s) sent in
the same `sendmsg(2)` call. A receiver that reads the framed message first
via `recv(2)` (which cannot return ancillary data) will never see the file descriptor.
Sending the ancillary data in a separate `sendmsg` call with its own
dedicated byte avoids any overlap with the existing framing logic.

### Stream Barrier Semantics (SOCK_STREAM)

On `SOCK_STREAM`, ancillary data acts as a delivery barrier. Given three
consecutive sends:

```
sendmsg(4 bytes, no ancillary)
sendmsg(1 byte,  with SCM_RIGHTS)
sendmsg(4 bytes, no ancillary)
```

A receiver calling `recvmsg` with a 20-byte buffer receives 5 bytes (the
first 4 plus the tagged 1) and the ancillary data together. The remaining 4
bytes arrive in the next `recvmsg` call. The file descriptor cannot "leak" into a later
receive call; it is always delivered with the bytes sent in the same
`sendmsg` call.

---

## Examples

### Send With FD (Grant)

```cpp
// Generic: send shm_fd to the connected peer.
// <tag_granted> is the application-defined grant indicator byte.

static int sendWithFd(int sockfd, int shm_fd, uint8_t tag_granted) noexcept
{
    union {
        char           buf[CMSG_SPACE(sizeof(int))];
        struct cmsghdr align;
    } ctrl;

    // Zero-initialize so CMSG_NXTHDR works correctly if iterated.
    ::memset(&ctrl, 0, sizeof(ctrl));

    struct iovec iov = { .iov_base = &tag_granted, .iov_len = sizeof(tag_granted) };

    struct msghdr msg = {};
    msg.msg_iov        = &iov;
    msg.msg_iovlen     = 1;
    msg.msg_control    = ctrl.buf;
    msg.msg_controllen = sizeof(ctrl.buf);

    struct cmsghdr* cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type  = SCM_RIGHTS;
    cmsg->cmsg_len   = CMSG_LEN(sizeof(int));
    ::memcpy(CMSG_DATA(cmsg), &shm_fd, sizeof(int));

    const ssize_t sent = ::sendmsg(sockfd, &msg, MSG_NOSIGNAL);
    return (sent == static_cast<ssize_t>(sizeof(tag_granted))) ? 0 : -1;
}
```

### Send Without FD (Reject)

```cpp
// Generic: send rejection indicator with no ancillary data.
// <tag_rejected> is the application-defined rejection indicator byte.

static int sendRejection(int sockfd, uint8_t tag_rejected) noexcept
{
    struct iovec iov = { .iov_base = &tag_rejected, .iov_len = sizeof(tag_rejected) };

    struct msghdr msg = {};
    msg.msg_iov        = &iov;
    msg.msg_iovlen     = 1;
    // msg_control = NULL, msg_controllen = 0: no ancillary data.

    const ssize_t sent = ::sendmsg(sockfd, &msg, MSG_NOSIGNAL);
    return (sent == static_cast<ssize_t>(sizeof(tag_rejected))) ? 0 : -1;
}
```

### Receive and Detect FD Presence

```cpp
// Generic: receive one tag byte and an optional fd.
// Returns the received fd (>= 0) if granted; -1 if rejected or on error.

static int receiveOptionalFd(int sockfd, uint8_t* tag_out) noexcept
{
    union {
        char           buf[CMSG_SPACE(sizeof(int))];
        struct cmsghdr align;
    } ctrl;
    ::memset(&ctrl, 0, sizeof(ctrl));

    uint8_t tag_byte = 0;
    struct iovec iov = { .iov_base = &tag_byte, .iov_len = sizeof(tag_byte) };

    struct msghdr msg = {};
    msg.msg_iov        = &iov;
    msg.msg_iovlen     = 1;
    msg.msg_control    = ctrl.buf;
    msg.msg_controllen = sizeof(ctrl.buf);

    const ssize_t received = ::recvmsg(sockfd, &msg, MSG_CMSG_CLOEXEC);
    if (received != static_cast<ssize_t>(sizeof(tag_byte))) {
        return -1;   // EOF or error
    }

    if (tag_out != nullptr) {
        *tag_out = tag_byte;
    }

    // Detect truncation: fds that did not fit were silently closed.
    if ((msg.msg_flags & MSG_CTRUNC) != 0) {
        return -1;   // protocol error: buffer too small
    }

    const struct cmsghdr* cmsg = CMSG_FIRSTHDR(&msg);
    if (cmsg == nullptr) {
        return -1;   // no ancillary data: sender rejected
    }
    if (cmsg->cmsg_level != SOL_SOCKET || cmsg->cmsg_type != SCM_RIGHTS) {
        return -1;   // unexpected control message type
    }

    int received_fd = -1;
    ::memcpy(&received_fd, CMSG_DATA(cmsg), sizeof(int));
    return received_fd;
}
```

---

## Best Practices / Anti-patterns

### Best Practices

1. **Always pass `MSG_CMSG_CLOEXEC` to `recvmsg`** (Linux >= 2.6.23). This
   sets `FD_CLOEXEC` on received fds atomically. Without it, there is a
   window between `recvmsg` return and a subsequent `fcntl` call during which
   a `fork`+`exec` child inherits the fd.

2. **Always send at least one byte of real data on `SOCK_STREAM`**. A
   `sendmsg` call with `msg_iov` pointing to a zero-length buffer and only
   ancillary data does not reliably deliver the ancillary data on Linux. The
   dedicated tag-byte pattern satisfies this requirement.

3. **Zero-initialize the control buffer before building `cmsghdr`s**. The
   `CMSG_NXTHDR` macro relies on the padding bytes being zero to locate the
   next header correctly.

4. **Use the alignment union** (`union { char buf[CMSG_SPACE(...)]; struct cmsghdr align; }`)
   for all stack-allocated control buffers. Never use a plain `char[]` array.

5. **Use `memcpy` through `CMSG_DATA`**. The pointer is `unsigned char *` and
   is not guaranteed to be aligned for `int`. Direct casting to `int *` is
   undefined behavior.

6. **Check `MSG_CTRUNC` after every `recvmsg`**. If set, the ancillary data
   was truncated and any fds that did not fit were silently closed by the
   kernel. Treat `MSG_CTRUNC` as a protocol error and close the connection.

7. **Close the received fd on all error paths** immediately after `recvmsg`
   if the received fd is not needed. An unclosed received fd is a resource
   leak even if the sender's copy is closed.

8. **Do not assume the received fd number equals the sender's fd number**.
   The kernel assigns a free slot in the receiver's descriptor table. The fd
   integers are independent.

9. **Limit to `SCM_MAX_FD` (253) fds per `sendmsg` call**. Sending more
   returns `EINVAL` immediately. Send shared memory references one fd at a
   time to stay well within this limit.

10. **Close the sender's fd after `sendmsg` if no longer needed**. After
    `sendmsg` returns, the kernel has duplicated the reference into the
    receive queue. The sender retains its own reference until it calls
    `close`.

### Anti-patterns

| Anti-pattern | Consequence | Correct alternative |
| --- | --- | --- |
| Sending ancillary data with `send()` / `write()` | No ancillary channel; FD silently dropped | Use `sendmsg(2)` |
| Receiving ancillary data with `recv()` / `read()` | No ancillary channel; received FD silently closed | Use `recvmsg(2)` |
| Using a plain `char ctrl[CMSG_SPACE(...)]` buffer | Undefined behavior if misaligned | Use the alignment union |
| Casting `CMSG_DATA(cmsg)` to `int *` directly | Undefined behavior (alignment) | Use `memcpy` into an `int` variable |
| Omitting `MSG_CMSG_CLOEXEC` on `recvmsg` | fd leaks across `fork`+`exec` | Always pass `MSG_CMSG_CLOEXEC` |
| Ignoring `MSG_CTRUNC` | Silent fd loss; memory leak | Check `msg.msg_flags & MSG_CTRUNC` |
| Embedding the FD in a byte-stream read by `recv()` | The ancillary data is not returned by `recv` | Use a dedicated `recvmsg` step for the tag byte |
| Sending zero data bytes with ancillary on `SOCK_STREAM` | Ancillary data may be discarded | Include at least one real data byte |

---

## Error Catalogue

| Error | Syscall | Source | Meaning | Correct handling |
| --- | --- | --- | --- | --- |
| `EBADF` | `sendmsg(2)` | `unix(7)` | An fd in the `SCM_RIGHTS` array is not a valid open fd | Validate all fds before passing to `sendmsg`; return failure |
| `EINVAL` | `sendmsg(2)` | `unix(7)` | More than `SCM_MAX_FD` (253) fds in the array | Limit to 1 fd per call for shared memory use cases |
| `ETOOMANYREFS` | `sendmsg(2)` | `unix(7)` | In-flight fd count exceeds `RLIMIT_NOFILE` without `CAP_SYS_RESOURCE` | Rate-limit FD grants; ensure receivers call `recvmsg` promptly |
| `EMSGSIZE` | `sendmsg(2)` | `send(2)` | Message too large to send atomically | Reduce payload size or number of fds |
| `EPIPE` | `sendmsg(2)` | `send(2)` | Peer has closed the connection | Treat as disconnect; use `MSG_NOSIGNAL` to prevent `SIGPIPE` |
| `MSG_CTRUNC` in `msg_flags` | `recvmsg(2)` | `unix(7)` | Ancillary buffer too small; excess fds silently closed | Treat as protocol error; use `CMSG_SPACE(sizeof(int))` for one fd |
| `ENOMEM` | `recvmsg(2)` | `recv(2)` | Kernel cannot allocate memory for the message | Log error; return failure |
| `EINTR` | `sendmsg(2)`, `recvmsg(2)` | `send(2)`, `recv(2)` | Interrupted by signal | Retry the syscall in a loop |

---

## Domain Glossary

### Black-Box Terms (approved for SWE.1 requirements)

**file descriptor transfer**
Definition: The act of granting another process access to an already-open kernel resource by delivering an equivalent file descriptor into the receiving process's file descriptor table over a Unix Domain Socket.
Rationale: The outcome (the receiving process can access the resource) is observable. The transfer is an application-level operation with a success or rejection result.

**file descriptor grant**
Definition: The outcome of a file descriptor transfer in which the sender attaches an open file descriptor to a message and the receiver obtains a valid file descriptor for the same resource.
Rationale: The grant and its complement, the rejection, are the two observable results of a file descriptor request. Both are visible to the requesting process.

**file descriptor rejection**
Definition: The outcome of a file descriptor transfer in which the sender sends the protocol response byte without attaching a file descriptor, indicating the request was denied.
Rationale: The requesting process observes the absence of a file descriptor in the response. The absence is as observable as the presence.

**message with optional file descriptor**
Definition: A protocol message in which the sender may or may not include a file descriptor depending on the application-level decision, and the receiver detects which case occurred.
Rationale: The optionality is an observable contract between sender and receiver. Requirements can mandate that the sender shall include or omit the file descriptor based on specified conditions.

### White-Box Terms (restricted to SWE.3 / SWE.4 artefacts)

**ancillary data**
Definition: Out-of-band data carried alongside the normal payload in a `sendmsg(2)` / `recvmsg(2)` call, structured as a sequence of `cmsghdr` records.
Rationale: Ancillary data is an OS-level mechanism. The observable outcome is "file descriptor received" or "file descriptor absent"; the ancillary data channel is the implementation detail.

**control message**
Definition: A single `cmsghdr`-headed record within the ancillary data buffer, identified by `cmsg_level` and `cmsg_type`, carrying protocol-specific out-of-band information such as a set of file descriptors.
Rationale: A SWE.3 / SWE.4 concept used when specifying buffer layout and `cmsg` macro usage.

**`SCM_RIGHTS`**
Definition: The ancillary message type (`cmsg_type = SCM_RIGHTS`, `cmsg_level = SOL_SOCKET`) whose data payload is an `int[]` array of file descriptors to transfer.
Rationale: A POSIX/Linux socket API constant. Named in detailed design when specifying the exact `cmsghdr` field values to set.

**in-flight file descriptor**
Definition: A file descriptor that has been sent with `sendmsg(2)` in an `SCM_RIGHTS` control message but has not yet been received by the peer with `recvmsg(2)`.
Rationale: In-flight fds count against the sender's `RLIMIT_NOFILE` until the receiver accepts them. This is a resource management detail relevant to detailed design and unit tests.

**`MSG_CMSG_CLOEXEC`**
Definition: A `recvmsg(2)` flag that atomically sets `FD_CLOEXEC` on all file descriptors received via `SCM_RIGHTS`.
Rationale: A Linux-specific receive flag. Belongs in SWE.3 implementation detail; the SWE.1 concern is "received file descriptors shall not be inherited by child processes".

**`MSG_CTRUNC`**
Definition: A flag set in `msg->msg_flags` after `recvmsg(2)` when the ancillary data buffer was too small to receive all control messages; excess fds are silently closed.
Rationale: An OS-level error indicator for the ancillary buffer sizing logic. Belongs in SWE.3.

**alignment union**
Definition: The `union { char buf[CMSG_SPACE(...)]; struct cmsghdr align; }` idiom used to guarantee that a stack-allocated control buffer meets the alignment requirement of `cmsghdr`.
Rationale: A C/C++ implementation technique. Belongs in SWE.3 detailed design.

**stream barrier**
Definition: The property of `SOCK_STREAM` ancillary data delivery whereby the kernel delivers the ancillary data together with the bytes sent in the same `sendmsg` call, even if the receiver reads multiple sends in a single `recvmsg` call.
Rationale: A kernel scheduling and buffering detail. Relevant to SWE.3 when specifying which byte carries the ancillary data and why the FD exchange uses a dedicated single-byte `sendmsg` step.
