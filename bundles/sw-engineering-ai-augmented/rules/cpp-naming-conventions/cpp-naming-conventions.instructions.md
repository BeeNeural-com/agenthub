---
description: C++ naming conventions (CP10) for variables, functions, classes, and file descriptors in all C++ files (production, tests, and examples)
applyTo: "**/*.{h,hpp,cpp,tpp}"
---

# C++ Naming Conventions (CP10)

These rules are enforced by `.clang-tidy` and apply to all production source files under `src/`.

## Member naming

Private members use `m`-prefix `CamelCase`. Do not use trailing underscores. Each member name must be globally unique across all classes to enable unambiguous grepping.

Correct: `mFileDescriptor`, `mServerConnection`, `mBoundSocketPath`
Wrong: `fd_`, `m_fd`, `mConnection` (ambiguous if used in multiple classes)

## Constants

Constants use `k`-prefix `CamelCase`.

Correct: `kMaxConnections`, `kDefaultTimeout`
Wrong: `MAX_CONNECTIONS`, `defaultTimeout`

## Methods and local variables

Methods and local variables use `camelBack`. Prefer full descriptive names over abbreviations. Never use truncations like `err`, `msg`, `ctx`, `cfg`, `cb`, `evt`, `req`, `res`, `val`, `len`, `cnt`, `idx`, `iter`, `param`. Always spell out the word.

Correct: `handleRequest()`, `bytesReceived`, `sendError`, `socketPath`, `payloadSize`
Wrong: `HandleRequest()`, `bytes_received`, `err`, `msg`, `sz`

## Abbreviation expansions

Common abbreviations must be expanded to full descriptive words. The following expansions are mandatory:

**addr** → `address` (e.g., `socketAddress`, `serverAddress`)
**buf** → `buffer` (e.g., `receiveBuffer`, `writeBuffer`)
**cb** → `callback` (e.g., `messageCallback`, `disconnectedCallback`)
**cfg** → `configuration` (e.g., `serverConfiguration`)
**cnt** → `count` (e.g., `connectionCount`, `byteCount`)
**ctx** → `context` (e.g., `requestContext`)
**errno** / `Errno` → `errorNumber` / `ErrorNumber` (e.g., `systemErrorNumber`)
**err** → `error` (e.g., `sendError`, `connectError`)
**evt** → `event` (e.g., `pollEvent`, `clientEvent`)
**fd** → contextual name (e.g., `socketFd`, `acceptorFd`, `clientFd`); never bare `fd`
**fds** → `pollDescriptors` (e.g., `activePollDescriptors`)
**idx** → `index` (e.g., `clientIndex`, `slotIndex`)
**iter** → `iterator` (e.g., `clientIterator`)
**len** → `length` or `size` (e.g., `payloadLength`, `bufferSize`)
**msg** → `message` (e.g., `logMessage`, `errorMessage`)
**n** → contextual (e.g., `bytesReceived`, `connectionCount`)
**param** → `parameter` (e.g., `configurationParameter`)
**pfd** → `pollDescriptor` (e.g., `serverPollDescriptor`)
**ptr** → `Pointer` suffix (e.g., `writePointer`, `dataPointer`)
**req** → `request` (e.g., `connectRequest`)
**res** → `result` or `response` (e.g., `pollResult`, `serverResponse`)
**sz** → `size` (e.g., `bufferSize`, `payloadSize`)
**tmp** → contextual (e.g., `temporaryBuffer`, `pendingResult`)
**val** → `value` (e.g., `returnValue`, `configValue`)

See `doc/coding_principles.adoc` §CP10 for the authoritative list.

## File naming

All `.h`, `.hpp`, `.cpp`, and `.tpp` files use PascalCase matching the primary type they declare. Link-seam wrappers use `<Domain>Posix` (e.g., `IpcPosix.h`, `ShmPosix.cpp`). Interfaces use `I`-prefix (`IEventDispatcher.h`). Mocks use `Mock`-prefix (`MockIpcPosix.h`).

## Checklist

- [ ] Private members use `m`-prefix `CamelCase` (not trailing underscores)
- [ ] Constants use `k`-prefix `CamelCase`
- [ ] Methods and locals use `camelBack`
- [ ] No bare abbreviations: no `addr`, `buf`, `fd` (bare), `pfd`, `ptr`, `n`; all expanded
- [ ] File names use PascalCase matching the primary type or module
