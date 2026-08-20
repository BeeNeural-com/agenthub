---
name: detailed-design
description: "Generic worked examples for ASPICE detailed design artifacts: Doxygen-documented C++ class and struct headers with @elaborates arch: annotations in src/. Use when writing or reviewing @elaborates-tagged header files for E3 Software Platform components."
---

# SWE.3 Detailed Design — Skill Reference

This skill provides generic worked examples for SWE.3 detailed design outputs.

Scope:
- Design artifacts are Doxygen-documented C++ headers in src/.
- Implementation artifacts are matching .cpp files.
- This file contains reusable patterns only (no project-specific operational data).

---

## Generic Traceability Pattern

SWE.1 req: IDs
→ SWE.2 arch: IDs via :covers:
→ SWE.3 headers via @elaborates
→ SWE.4 unit tests via @covers

---

## Example 1 — Manager Class Header Pattern

```cpp
#pragma once

#include <cstddef>
#include <cstdint>
#include <system_error>
#include <unordered_map>
#include <vector>

namespace <project>::<component> {

struct ManagerConfig {
    std::size_t maxItemSize{1024U};
    std::size_t maxItemsPerClient{8U};
};

/*!
 * @brief Manages per-client resources with deterministic error reporting.
 *
 * @details
 * Stores client-to-resource ownership in an internal map. Public methods are
 * expected to be called from one execution context unless external
 * synchronization is provided.
 *
 * @elaborates arch:<component>-<service-element>
 * @req req:<component>-<topic>-<validation>
 * @req req:<component>-<topic>-<limit>
 */
class ResourceManager final {
public:
    explicit ResourceManager(ManagerConfig config) noexcept;

    /*!
     * @brief Allocates a resource for a client.
     *
     * @param[in] clientId      Client identifier.
     * @param[in] requestedSize Requested size in bytes.
     * @param[out] handleOut    Valid handle on success.
     * @return std::error_code{} on success, or domain-specific failure code.
     *
     * @pre clientId references an active client context.
     * @post On success, caller owns the returned handle according to API policy.
     *
     * @req req:<component>-<topic>-<validation>
     */
    std::error_code allocate(
        int clientId,
        std::size_t requestedSize,
        int& handleOut) noexcept;

    /*!
     * @brief Releases all resources associated with a client.
     *
     * @param[in] clientId Client identifier.
     *
     * @post No resource remains associated with clientId.
     *
     * @req req:<component>-<topic>-<lifecycle>
     */
    void releaseClientResources(int clientId) noexcept;

private:
    ManagerConfig mConfig;
    std::unordered_map<int, std::vector<int>> mClientResources;
};

} // namespace <project>::<component>
```

---

## Example 2 — Interface Data Types Pattern

```cpp
#pragma once

#include <cstdint>

namespace <project>::<component> {

/*!
 * @brief Request message for a resource operation.
 *
 * @details
 * Fixed-size message layout. Field semantics and versioning are owned by the
 * interface contract.
 *
 * @elaborates arch:<component>-<wire-contract>
 */
struct RequestMessage {
    std::uint32_t magic{0U};
    std::uint32_t version{1U};
    std::uint64_t requestedSize{0U};
};

/*!
 * @brief Response message for a resource operation.
 *
 * @elaborates arch:<component>-<wire-contract>
 */
struct ResponseMessage {
    std::uint32_t magic{0U};
    std::uint32_t errorCode{0U};
    std::uint64_t grantedSize{0U};
};

} // namespace <project>::<component>
```

---

> **Before writing any `.cpp` file:** See `.github/skills/unit-construction/SKILL.md` — CP01–CP13 coding principles, clang-tidy naming rules, file-level comment block format, SRC_FILES registration, and a worked Calculator implementation example.

---

## Example 3 — State Machine / Dynamic Aspects Pattern (ASPICE BP2)

ASPICE SWE.3 BP2 requires that **dynamic aspects** (state transitions, interrupt handling, scheduling) are documented in the detailed design. For classes with internal state, document the state machine in the class Doxygen block using `@details`.

```cpp
#pragma once

#include <system_error>

namespace <project>::<component> {

/*!
 * @brief Manages the lifecycle state of a resource handle.
 *
 * @details
 * State machine:
 * @code
 *   [Idle] --create()--> [Active] --release()--> [Idle]
 *                            |
 *                         error()
 *                            v
 *                         [Failed] --reset()--> [Idle]
 * @endcode
 *
 * All state transitions are guarded by `std::error_code` return values.
 * The object is **not** thread-safe; external synchronisation is required
 * for concurrent access.
 *
 * @elaborates arch:<component>-<handle-element>
 * @req req:<component>-<create-success>
 * @req req:<component>-<create-failure>
 * @req req:<component>-<cleanup>
 */
class ResourceHandle final {
public:
    enum class State { Idle, Active, Failed };

    ResourceHandle() noexcept = default;

    /*!
     * @brief Transitions from Idle to Active.
     * @return std::error_code{} on success; domain error on failure.
     * @post State is Active on success; Failed on error.
     * @req req:<component>-<create-success>
     * @req req:<component>-<create-failure>
     */
    std::error_code create() noexcept;

    /*!
     * @brief Transitions from Active to Idle, releasing all resources.
     * @pre State is Active.
     * @post State is Idle. No resources are held.
     * @req req:<component>-<cleanup>
     */
    void release() noexcept;

    /*!
     * @brief Resets from Failed to Idle.
     * @post State is Idle.
     */
    void reset() noexcept;

    [[nodiscard]] State state() const noexcept
    {
        return mState;
    }

private:
    State mState{State::Idle};
    int mResourceFd{-1};
};

} // namespace <project>::<component>
```

**Key rules for state machine documentation:**
- The `@details` block must show every state and every transition as an ASCII diagram or enumerated list.
- Document the thread-safety model explicitly ("not thread-safe; external synchronisation required" or "all methods callable from any thread").
- Every transition must be covered by at least one `@req` on the corresponding method.

---

## Checklist

- `@elaborates` must exactly match an existing SWE.2 ID.
- `@req` must reference valid SWE.1 IDs.
- Use clear `@pre`/`@post` on externally visible methods.
- Keep headers declaration-only; place behavior in .cpp.
- Document private members sufficiently for white-box review.
- Private member names use `m`-prefix CamelCase — never trailing underscores (CP10).
- For the matching `.cpp` implementation, see `.github/skills/unit-construction/SKILL.md`.

## ASPICE Rating Guidelines

For the official Automotive SPICE rating rules that govern SWE.3 process assessment (what a software unit is, code metrics vs unit boundaries, dynamic behavior description, coding principles at CL1), see:

- [aspice-rating-guidelines.adoc](./aspice-rating-guidelines.adoc) — VDA Automotive SPICE Guidelines, 2nd Edition 2023, Section 3.10: rating rules RL.1–RL.3 with conditions and consequences.

---

## Coverage Classification

Before starting, classify each `arch:` ID:

| State        | Criteria                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| **COMPLETE** | Header with `@elaborates` exists AND corresponding `.cpp` is implemented AND `SRC_FILES` entry present |
| **DESIGNED** | Header with `@elaborates` exists but no `.cpp` OR `.cpp` not in `SRC_FILES`                            |
| **MISSING**  | No header with `@elaborates` references this arch: ID                                             |

---

## Design Input Sources

Before writing any header, read in order:

1. `doc/component_architecture/<component>/architecture.md` — `arch:` block for the target element
2. `doc/component_architecture/<component>/interfaces.md` — `arch:` blocks and `[#info:...-swe3-note]` design hints
3. `doc/component_requirements/<component>/*.md` — `req:` IDs allocated to this element
4. `.github/skills/detailed-design/SKILL.md` — worked examples (this file)
5. `doc/coding_principles.md` — project coding principles (if absent, flag CRITICAL and stop)

---

## Calculator Example

Component: `libcalculator`. File: `src/libcalculator/Calculator.h`

```cpp
#pragma once

#include <cstdint>
#include <system_error>

namespace libcalculator {

/*!
 * @brief Performs integer arithmetic with overflow detection.
 *
 * @details
 * Single-method element. All operations are stateless.
 * Not thread-safe; external synchronization is required for concurrent use.
 *
 * @elaborates arch:libcalculator-adder
 * @req req:libcalculator-add-success
 * @req req:libcalculator-add-overflow-failure
 */
class Calculator final {
public:
    Calculator() noexcept = default;

    /*!
     * @brief Adds two integers, detecting overflow before computation.
     *
     * @param[in]  firstOperand   First integer operand.
     * @param[in]  secondOperand  Second integer operand.
     * @param[out] result         Sum on success; unchanged on error.
     * @return std::error_code{} on success; std::errc::value_too_large on overflow.
     *
     * @pre No preconditions; callable on a default-constructed instance.
     * @post On success, result == firstOperand + secondOperand. On error, result is unchanged.
     *
     * @req req:libcalculator-add-success
     * @req req:libcalculator-add-overflow-failure
     */
    std::error_code add(
        std::int32_t firstOperand,
        std::int32_t secondOperand,
        std::int32_t& result) const noexcept;

private:
    // Stateless element; no member fields required.
};

} // namespace libcalculator
```
