---
name: test-design-techniques
description: "ISO 29119 test design techniques and minimum coverage rules for integration and qualification test specification. Use when applying EP, BVA, State Transition, or Error Guessing to derive test conditions from upstream IDs (arch: or req:). Provides technique definitions, minimum coverage table, and test design table format."
---

# Test Design Techniques Skill

This skill provides component-agnostic guidance for applying ISO 29119-4 test design techniques during the T2a (Test Design) phase of integration and qualification test specification. It is used by the Integration Tester and Qualification Tester role agents to determine how many test conditions each upstream ID requires and which partitions to cover.

---

## Overview

Test design is the deliberate process of determining **how many** test conditions an upstream ID needs and **what** each condition verifies. Without a design step, agents default to "1 test per ID" — which under-tests complex interactions and over-tests simple ones.

Test design techniques are not mutually exclusive — a single upstream ID may require multiple techniques applied in combination.

---

## Reference / API

### Technique Definitions

**Equivalence Partitioning (EP):** Divide the interaction's input domain into classes where behavior is equivalent. Each class produces one test condition. Always include at least one valid (happy-path) and one invalid (error) partition.

**Boundary Value Analysis (BVA):** For any parameter with a specified range or limit, test at min, max, min−1, max+1. Each boundary produces one test condition.

**State Transition Testing:** For interactions involving state machines or lifecycle sequences, create one test condition per valid transition and one per invalid transition (transition that should be rejected). Read the `arch:` block with `classification: statemachine` (integration) or use-case steps (qualification) to identify the state graph.

**Error Guessing:** Based on the interaction type and component domain, add test conditions for common failure modes not covered by EP/BVA/State Transition. Examples: connection loss mid-operation, resource exhaustion, protocol violation, concurrent access, empty/null inputs, timeout expiry.

### Minimum Coverage Rules

| Upstream ID type | Min test conditions | Rationale |
|---|---|---|
| Simple interaction (1 path, no state) | 2 (1 happy + 1 error) | EP minimum |
| Interaction with specified limits | 2 + BVA conditions at each boundary | EP + BVA |
| State-machine / lifecycle sequence | 1 per valid transition + 1 per invalid transition | State Transition |
| Protocol / message exchange | 1 per message type × (1 happy + 1 error) | EP per message |
| Resource management (alloc/dealloc) | 3 (alloc + dealloc + exhaustion) | EP + Error Guessing |
| Error recovery / resilience | 1 per distinct error class | Error Guessing |

If the design table produces fewer conditions than the minimum for an ID's type, flag and justify the gap before proceeding to spec writing.

---

## Lifecycle & Usage Pattern

### When to Apply

T2a (Test Design) runs after T1 (Classify) and before T2b (Spec Writing) in both integration (Stage 1) and qualification (Stage 3) specification stages.

### Input

- **Integration (Stage 1):** The `arch:` block prose (with `classification: sequence`, `statemachine`, or `activity`) from SWE.2 artifacts. Read the block to identify the interaction's states, inputs, error paths, and boundary conditions.
- **Qualification (Stage 3):** The `req:` block prose — especially `:verification_criteria:` — from SWE.1 artifacts. Identify the requirement's input classes, state preconditions, error paths, and boundary conditions. Enforce black-box perspective: partitions must be derivable from the public API contract, not from implementation knowledge.

### Process

1. For each Uncovered in-scope ID, read the upstream block prose.
2. Classify the ID type using the Minimum Coverage Rules table.
3. Apply the appropriate technique(s) to identify partitions.
4. Produce the test design table.

### Output — Test Design Table

One row per test condition:

| Upstream ID | Technique | Condition name | Partition description |
|---|---|---|---|
| `arch:<component>-<sequence>` | EP | Happy path — normal connection | Valid client connects to listening server |
| `arch:<component>-<sequence>` | EP | Error — connection refused | Client connects when server not listening |
| `arch:<component>-<sequence>` | BVA | Max clients boundary | Connect client N+1 when N clients already connected |

---

## Examples

### Simple interaction (EP only)

Upstream: `arch:<component>-<lifecycle>` (classification: sequence) — describes a client connecting to a server.

| Upstream ID | Technique | Condition name | Partition description |
|---|---|---|---|
| `arch:<component>-<lifecycle>` | EP | Happy path — successful connect | Valid client connects to running server |
| `arch:<component>-<lifecycle>` | EP | Error — server not available | Client attempts connection when no server is listening |

Result: 2 conditions (meets minimum for simple interaction).

### State-machine interaction (State Transition + Error Guessing)

Upstream: `arch:<component>-<state-machine>` (classification: statemachine) — describes states: IDLE → CONNECTED → REGISTERED → ACTIVE.

| Upstream ID | Technique | Condition name | Partition description |
|---|---|---|---|
| `arch:<component>-<state-machine>` | State Transition | IDLE → CONNECTED | Valid forward transition |
| `arch:<component>-<state-machine>` | State Transition | CONNECTED → REGISTERED | Valid forward transition |
| `arch:<component>-<state-machine>` | State Transition | REGISTERED → ACTIVE | Valid forward transition |
| `arch:<component>-<state-machine>` | State Transition | IDLE → REGISTERED (invalid) | Skip CONNECTED state — should be rejected |
| `arch:<component>-<state-machine>` | Error Guessing | Forced disconnect from ACTIVE | Unexpected connection break in ACTIVE state |

Result: 5 conditions (meets minimum: 3 valid + 1 invalid + 1 error guess).

### Requirement with limits (EP + BVA)

Upstream: `req:<component>-<topic>-<payload>` — "payload size shall be 0–1024 bytes".

| Upstream ID | Technique | Condition name | Partition description |
|---|---|---|---|
| `req:<component>-<topic>-<payload>` | EP | Happy path — valid payload | Payload within 0–1024 range |
| `req:<component>-<topic>-<payload>` | EP | Error — oversized payload | Payload exceeds 1024 bytes |
| `req:<component>-<topic>-<payload>` | BVA | Min boundary (0) | Empty payload |
| `req:<component>-<topic>-<payload>` | BVA | Max boundary (1024) | Payload at maximum size |
| `req:<component>-<topic>-<payload>` | BVA | Max+1 boundary (1025) | Payload one byte over maximum |

Result: 5 conditions (meets minimum: 2 EP + 3 BVA).

### Error recovery interaction (Error Guessing + EP)

Upstream: `arch:<component>-seq-<disconnection>` (classification: sequence) describes: client or server may disconnect at any lifecycle phase; the surviving side must detect the loss, invoke the registered callback, and clean up resources without leaking file descriptors.

| Upstream ID | Technique | Condition name | Partition description |
|---|---|---|---|
| `arch:<component>-seq-<disconnection>` | EP | Happy path: graceful shutdown | Server calls shutdown(); clients receive disconnect callback |
| `arch:<component>-seq-<disconnection>` | EP | Error: peer vanishes mid-transfer | Client process terminates while server is sending a message |
| `arch:<component>-seq-<disconnection>` | Error Guessing | Disconnect during accept | Client connects then immediately disconnects before server calls processEvents() |
| `arch:<component>-seq-<disconnection>` | Error Guessing | Multi-client partial disconnect | One of N clients disconnects; remaining clients unaffected |
| `arch:<component>-seq-<disconnection>` | Error Guessing | Resource cleanup after disconnect | After disconnect, file descriptors and socket file are released (no leak) |

Result: 5 conditions (1 happy EP + 1 error EP + 3 error guesses; meets minimum for error recovery).

---

## Best Practices / Anti-patterns

**Do:**
- Read the upstream block prose before selecting techniques — the text reveals which techniques apply.
- Combine techniques: EP provides the base partitions, BVA refines boundaries, Error Guessing adds domain-specific negatives.
- Classify the ID type first, then check the minimum coverage table, then design to meet or exceed it.
- For qualification (Stage 3): derive partitions only from the public API contract and requirement text — never from implementation knowledge.

**Don't:**
- Apply "1 test per ID" without analysis — this under-tests complex IDs and wastes effort on simple ones.
- Invent partitions not grounded in the upstream block prose — every condition must trace back to a documented behavior, constraint, or error path.
- Skip the design table — T2b (Spec Writing) consumes this table. Without it, spec blocks are ad-hoc.
- Apply BVA when no limits are specified — BVA requires a documented range or count.
