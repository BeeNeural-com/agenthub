---
name: aspice-bp-reference
description: "Canonical ASPICE PAM 4.0 Base Practice (BP) descriptions and review criteria (RC/RV/RF, AR, DR, VR). Load only when a role agent explicitly requests it for a review task — Requirements Engineer (RC01–RC11), Software Architect (AR01–AR08), Software Engineer (DR01–DR08, VR01–VR08), or Auditor. Not needed by Integration Tester or Qualification Tester (their review criteria are in instructions)."
---

# ASPICE PAM 4.0 — Base Practice Reference

This skill is the canonical reference for ASPICE Base Practice (BP) descriptions across all six SWE levels. Agents cite a specific section instead of repeating BP prose inline.

---

## SWE.1 — Software Requirements Analysis

**BP1 — Specify software requirements**
Identify software requirements from system requirements and system architectural design. Every requirement must include verification criteria that define qualitative or quantitative conditions needed to verify it. Verification criteria are an inherent part of BP1 — not a separate activity.

**BP2 — Structure software requirements**
Categorize requirements using classification criteria beyond merely "functional" and "non-functional". Using only those two as the sole criterion is insufficient and rates BP2 as N. Apply classification to enable prioritization and overview.

**BP3 — Analyze software requirements**
Analyze requirements for correctness, technical feasibility, verifiability, and consistency with each other and with system requirements. Analysis supports project management on scope and estimates. Tool-based attributes or comments (`:analysis_note:`) constitute valid analysis evidence.

**BP4 — Analyze impact on the operating environment**
Analyze the impact of software requirements on interfaces and the operating environment (hardware, OS, other software) to identify constraints or required changes.

**BP5 — Establish bidirectional traceability**
Establish bidirectional traceability between software requirements and either system requirements (SYS.2) or the system architectural design (SYS.3). Maintain consistency through changes. Only one traceability path per requirement is needed — not both simultaneously.

**Rating Rules**
- RL.1: Software-only development may trace directly to stakeholder requirements instead of SYS.2/SYS.3 — BP5 not downrated.
- RL.2: Deriving from platform requirements instead of system requirements — BP1 not downrated.

---

## SWE.2 — Software Architectural Design

**BP1 — Develop software architecture**
Develop and document the software architectural design including static structure (modules, components, executables, libraries) and dynamic aspects (execution sequences, concurrency model, interrupt handling). The architecture must show how software requirements are realized. Third-party software must have its license analyzed — omitting this risks BP1 downrating.

**BP2 — Allocate software requirements**
Assign every software requirement to at least one architectural element. No `req:` ID may be unallocated. The `:covers:` attribute on `arch:` blocks implements this.

**BP3 — Analyze software architecture**
Analyze the software architecture to ensure it satisfies the software requirements and is correct, feasible, and consistent. Analysis must address cybersecurity, safety, and robustness concerns. Non-quantitative (qualitative) analysis is sufficient — RL.1 explicitly permits this. Each `arch:` block should have an associated `[#arch-analysis:...]` info block documenting correctness, feasibility, and relevant safety/cybersecurity considerations.

**BP4 — Establish bidirectional traceability**
Establish bidirectional traceability between software requirements and software architecture. Maintain consistency through changes.

**Rating Rules**
- RL.1: Non-quantitative (qualitative) analysis is sufficient for BP3.

---

## SWE.3 — Software Detailed Design and Unit Construction

**BP1 — Develop software detailed design**
Develop and document the detailed design for each software unit: behavior, static structure, relationships, and interfaces. A software unit is a logical/domain concept defined by the architecture — not a metric-based division of files or functions. Unit boundaries are determined by design coherence, not by file count or line count.

**BP2 — Specify dynamic aspects of the detailed design**
Document the dynamic aspects: states, transitions, sequences of operations, and the concurrency model for each software unit. `@details` blocks in Doxygen headers carry this documentation.

**BP3 — Develop software units**
Develop and document software units in source code, applying project-defined coding principles documented in `doc/coding_principles.md`. Implementation must be consistent with the detailed design. The absence of `doc/coding_principles.md` means BP3 cannot be assessed.

**BP4 — Establish bidirectional traceability**
Establish bidirectional traceability between software architectural design elements and software units. `@elaborates arch:<id>` in headers and `// Elaborates:` in `.cpp` files implement this. A discrepancy between a header declaration and its `.cpp` implementation is a BP4 finding.

**Rating Rules**
- RL.1: Unit boundaries are defined by design coherence, not code metrics. Never demand class splitting purely on size grounds.
- RL.2: Coding principles must be documented. If `doc/coding_principles.md` does not exist, flag CRITICAL before starting unit construction.

---

## SWE.4 — Software Unit Verification

**BP1 — Define software unit verification measures**
Define the strategy for verifying each software unit: verification types, tools, environments, and entry/exit criteria. Automated test scripts must have their correctness addressed (RL.2). Entry/exit criteria are stated in fixture `SetUp`/`TearDown` contracts or spec block `@pre`/`@post` tags.

**BP2 — Select software unit test cases**
Select test cases based on the detailed design. Code coverage is accompanying information only — 100% coverage is not a verification objective (RL.1). Test case selection must cover success, failure, and boundary conditions from the detailed design.

**BP3 — Execute software unit verification**
Execute verification measures and record results. `FAIL()` stubs are specification-complete but execution-incomplete — they satisfy T1 (specification) but not T4 (execution).

**BP4 — Establish bidirectional traceability**
`@covers arch:<id>` and `@req req:<id>` Doxygen tags above each `TEST_F` implement this. Test result XML provides the traceability from results back to test cases.

**Rating Rules**
- RL.1: Code coverage is accompanying information — never rate BP2 N because coverage is below a threshold.
- RL.2: Automated test scripts must have correctness addressed — a test body with no assertions is a BP1 violation.

---

## SWE.5 — Software Integration Testing

**BP1 — Define integration verification strategy**
Define which elements to integrate first, entry/exit criteria for each integration set, and the verification environment. Entry/exit criteria may be per integration set, not per individual measure (RL.2). Document the strategy in a `## Integration Strategy` section in each integration test spec file (`.md` in `doc/<component>/component_integration_tests/`).

**BP2 — Define verification measures for software integration**
Specify how each integration boundary is verified: measure type, tools, and environment. Automated test correctness must be addressed (RL.3).

**BP3 — Select verification measures**
Select specific test cases covering cross-element interactions. Single-element behavior belongs in SWE.4 (RL.1).

**BP4 — Integrate software**
Demonstrate incremental integration order consistent with the strategy.

**BP5 — Execute integration tests**
Execute measures against integrated software; record results. Explorative tests are acceptable with `@arch` traceability (RL.4).

**BP6 — Establish bidirectional traceability**
`verifies: arch:<id>` in TCASE YAML and `@arch` on GTest functions implement this.

**Rating Rules**
- RL.1: Integration scope is cross-element interactions. Single-element behavior is SWE.4 scope.
- RL.2: Entry/exit criteria per integration set are acceptable.
- RL.3: Automated test correctness must be addressed.
- RL.4: Explorative tests are acceptable when traceability annotations are present.

---

## SWE.6 — Software Qualification Testing

**BP1 — Define software verification measures**
Define measures to verify integrated software against SW requirements from a black-box perspective. Any verification environment (lab, HIL, simulation, production target) is applicable. Automated script correctness must be addressed (RL.3).

**BP2 — Select software verification measures**
Select test cases covering SW requirements. Static test methods require concrete review checklists. `no_test` exemptions require specific justification.

**BP3 — Execute software verification**
Execute measures; record results. `FAIL()` stubs are specification-complete but not execution-complete.

**BP4 — Establish bidirectional traceability**
`verifies: req:<id>` in TCASE YAML and `@req` on GTest functions implement this.

**Rating Rules**
- RL.1: Black-box view only — tests must not access private implementation details.
- RL.2: Entry/exit criteria per verification set are acceptable.
- RL.3: Automated test correctness must be addressed.

---

## Review Criteria

### SWE.1 Review Criteria

**RC01** — `:description:` uses SHALL (normative) or SHOULD (advisory); no ambiguous language (may, might, could, etc.)
**RC02** — Exactly one observable behavior per requirement; no compound requirements joined by "and"
**RC03** — `:description:` describes the component's own behavior, not the behavior of external systems
**RC04** — `:verification_criteria:` defines a concrete Arrange/Act/Assert scenario; not a restatement of the description
**RC05** — `:verification_method:` is one of: `dynamic_test`, `static_test`, `review`, `analysis`
**RC06** — `:classification:` is present and uses defined categories (functional, performance, reliability, security, etc.)
**RC07** — `:status:` is present; no accepted requirements have `TODO` in any field
**RC08** — `:covers:` references valid upstream IDs (`uc-*` or system requirement ID); no dangling references
**RC09** — Requirement is technically feasible; no contradiction with SWE.2 architectural constraints
**RC10** — No em dashes in normative prose
**RC11** — `:analysis_note:` (if present) adds genuine insight; not a restatement of `:description:`

**RV01** — `:verification_criteria:` covers the success path
**RV02** — `:verification_criteria:` covers at least one failure/error path (where applicable)
**RV03** — `:verification_criteria:` specifies observable outcome, not internal state
**RV04** — `:verification_criteria:` is specific enough to write a GTest `TEST_F` body directly from it
**RV05** — No orphaned `no_test` exemption without explicit justification

**RF01** — Requirement ID follows naming convention: `req:<component>-<topic>-<aspect>`
**RF02** — Topic file name matches the topic segment of the `req:` IDs it contains
**RF03** — `[#info:...]` blocks are present for design context; not mistaken for requirements
**RF04** — No duplicate `req:` IDs across all topic files
**RF05** — `:covers:` uses `uc-*` prefix for use case references; not `uc:uc-*`
**RF06** — Block anchor format: `[#req:<id>]` — no spaces, correct prefix
**RF07** — Title line follows the anchor immediately; no blank line between anchor and title

---

### SWE.2 Review Criteria

**AR01** — `arch:` `:responsibilities:` is a black-box statement; no implementation detail; no mention of POSIX functions or internal data structures
**AR02** — `arch:` `:covers:` references at least one `req:` ID; no unallocated elements
**AR03** — `arch-analysis:` block exists for each `arch:`; addresses correctness, feasibility, safety/cybersecurity
**AR04** — `arch:` `:contract:` is precise enough to write a mock or stub from; no circular descriptions
**AR05** — Sequence arch: IDs have steps covering both normal flow and at least one error path
**AR06** — Sequence arch: IDs have classification one of: `lifecycle`, `error-flow`, `ipc-interaction`, `resource-management`, `concurrency`
**AR07** — No em dashes in normative prose
**AR08** — Vocabulary is grounded in SWE.1 requirement terms and domain skills; no invented terminology

---

### SWE.3 Review Criteria

**DR01** — `@elaborates` present; `@brief` is a white-box description (not a restatement of SWE.2 black-box responsibility); `@details` covers internal data layout, POSIX functions used, concurrency model, error-signaling strategy, and ownership semantics
**DR02** — For stateful elements: `@details` documents valid states, transitions, and invalid-state behavior; for sequential elements: key operation order, concurrency model, and hazards
**DR03** — No raw `new`/`delete`; RAII for all FDs and resources; `std::error_code` returns; no exceptions; all rules in `doc/coding_principles.md` satisfied
**DR04** — Every `arch:` ID has exactly one `@elaborates` header; every `@elaborates` value matches a real SWE.2 `arch:` ID; every `@req` tag matches a real SWE.1 `req:` ID
**DR05** — Method signatures in `.h` exactly match `.cpp`; no undeclared public methods in `.cpp`; no declared-but-unimplemented methods (unless `= delete`)
**DR06** — `@details` describes white-box internal design; no implementation code or logic in headers; `@brief` does not restate SWE.2 black-box responsibility
**DR07** — Every `.cpp` is listed in `SRC_FILES` in `src/CMakeLists.txt` with a `# SWE.3: arch:<id>` trailing comment
**DR08** — Zero Parasoft findings at any severity level (see sca-compliance instruction)

---

### SWE.4 Review Criteria

**VR01** — Every `TEST_F` has a Doxygen `/*!` spec block above it with `@brief`, `@req`, and `@covers`
**VR02** — `@brief` uses indicative mood ("verifies that…"); does not use imperative mood ("verify…")
**VR03** — `@covers arch:<id>` matches a real `@elaborates` ID in `src/**/*.{h,hpp}`
**VR04** — `@req req:<id>` matches a real `req:` ID in `doc/component_requirements/<component>/`
**VR05** — Test body follows Arrange-Act-Assert with clear section comments; no `FAIL()` stub remaining
**VR06** — Each `TEST_F` tests exactly one behavior; no compound assertions that test multiple unrelated behaviors
**VR07** — Fixture `SetUp`/`TearDown` covers all resource acquisition and release; no resource leaks
**VR08** — Zero Parasoft findings at any severity level (see sca-compliance instruction)

---

### SWE.5 Review Criteria

**IR01** — A `## Integration Strategy` section exists in the integration test spec file documenting: integration order, entry/exit criteria, and verification environment
**IR02** — Each TCASE has `verifies:` referencing a real SWE.2 `arch:` ID
**IR03** — Each TCASE covers a cross-element interaction; single-element behavior belongs in SWE.4
**IR04** — Description describes a complete cross-element flow: precondition → action → observable outcome
**IR05** — Each `TEST_F` in `tests/integration/` has `@arch` annotation referencing a real SWE.2 ID
**IR06** — `TEST_F` body uses only the public API (no access to private implementation details)
**IR07** — Fixture `SetUp`/`TearDown` covers all inter-element resource setup and teardown; no stale resource leaks
**IR08** — TCASE `type:` is one of the ISO 25010 quality characteristics: `Functional Suitability`, `Performance Efficiency`, `Reliability`, `Security`, `Compatibility`, `Fault Injection`, `Stress Testing`, `Resource Usage`, or `Back-to-Back Testing`

---

### SWE.6 Review Criteria

**QR01** — Each TCASE has `verifies:` referencing exactly one real SWE.1 `req:` ID (one TCASE per req, except for split-test justification)
**QR02** — Description corresponds directly to the `:verification_criteria:` of the covered `req:`; not a restatement of the description
**QR03** — `type:` is one of the ISO 25010 quality characteristics: `Functional Suitability`, `Performance Efficiency`, `Reliability`, `Security`, `Compatibility`, `Fault Injection`, `Stress Testing`, `Resource Usage`, or `Back-to-Back Testing`; `req:` IDs with `:verification_method: no_test` must have a justification comment
**QR04** — `TEST_F` bodies use only the public API; no access to private implementation details (strict black-box)
**QR05** — Each `TEST_F` has `@req req:<id>` annotation referencing a real SWE.1 `req:` ID
**QR06** — `TEST_F` body follows Arrange-Act-Assert; `FAIL()` stub not present
**QR07** — Fixture `SetUp`/`TearDown` uses the same deployment configuration as production; no test-specific shortcuts that would not exist in a real deployment
**QR08** — Failure paths from the `req:` `:verification_criteria:` are exercised by proxy methods (mocking/injection) where direct injection is unavailable; not silently skipped
