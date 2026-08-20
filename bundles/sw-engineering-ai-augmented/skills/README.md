# Skills: Table of Contents

> **Agents:** Read this file during Triage to discover skills relevant to the component being designed or implemented. Match the component's IPC mechanism, memory model, protocol, or SCA requirements against the skills below. Load every matching SKILL.md before starting construction (Stage 2) or test implementation (Stages 2 and 4).

Each skill file (`SKILL.md`) provides reusable worked examples and format patterns for a specific topic.
Skills are component-agnostic; they contain generic examples, never project-specific data.
The `description` frontmatter field is the routing signal Copilot uses to decide when to inject a skill.

All skills use a **flat layout**: `.github/skills/<skill-name>/SKILL.md`. This is required for GitHub Copilot skill discovery in both VS Code and the CLI.

## Platform Constraints

| Path | Name | Description |
|---|---|---|
| [parasoft-vwos-ruleset/SKILL.md](parasoft-vwos-ruleset/SKILL.md) | `parasoft-vwos-ruleset` | VW.os C++ Parasoft SCA ruleset with forbidden patterns and compliance rules. Use when reviewing C++ source files for SCA compliance. |

## ASPICE V-Model Engineering

| Path | Name | Description |
|---|---|---|
| [v-model-workflow/SKILL.md](v-model-workflow/SKILL.md) | `v-model-workflow` | Full ASPICE V-Model delegation map: SWE.1-SWE.6 owners, skill/instruction links, output directories, and handoff flow. Use when you need the complete workflow reference. |
| [aspice-bp-reference/SKILL.md](aspice-bp-reference/SKILL.md) | `aspice-bp-reference` | Canonical ASPICE PAM 4.0 Base Practice (BP) descriptions for all six V-Model levels. Use when writing or reviewing agents, instructions, or documentation that references ASPICE BP compliance criteria. |
| [requirements-specification/SKILL.md](requirements-specification/SKILL.md) | `requirements-specification` | SWE.1 requirements authoring reference: format patterns, abstraction level guidance, `info:` vs `req:` rules, BP3/BP4 evidence attributes, and anti-patterns. |
| [requirements-gap-analysis/SKILL.md](requirements-gap-analysis/SKILL.md) | `requirements-gap-analysis` | Gap analysis taxonomy, standard topic files table, 7-step workflow, and gap report template for SWE.1 software requirements. |
| [architecture-design/SKILL.md](architecture-design/SKILL.md) | `architecture-design` | Worked examples of SWE.2 architectural design artifacts: arch: blocks (elements, interfaces, sequences), Mermaid diagrams, and SWE.3 implementation notes. |
| [detailed-design/SKILL.md](detailed-design/SKILL.md) | `detailed-design` | Worked examples for SWE.3 detailed design: Doxygen-documented C++ class and struct headers with `@elaborates arch:` annotations. |
| [unit-construction/SKILL.md](unit-construction/SKILL.md) | `unit-construction` | CP01-CP13 coding principle patterns, clang-tidy naming rules, `SRC_FILES` registration, and a worked example for SWE.3 C++ `.cpp` implementation files. |
| [unit-test-specification/SKILL.md](unit-test-specification/SKILL.md) | `unit-test-specification` | Worked examples for SWE.4: Doxygen spec blocks, GTest fixture classes, and Arrange-Act-Assert test bodies in `tests/unit/`. |
| [integration-test-specification/SKILL.md](integration-test-specification/SKILL.md) | `integration-test-specification` | Worked examples for SWE.5: Markdown TCASE test-spec template, integration fixture conventions, and cross-boundary GTest patterns. |
| [qualification-test-specification/SKILL.md](qualification-test-specification/SKILL.md) | `qualification-test-specification` | Worked examples for SWE.6: Markdown TCASE test-spec template, qualification fixture header, and black-box GTest bodies. |
| [quality-summarizer/SKILL.md](quality-summarizer/SKILL.md) | `quality-summarizer` | V-Model quality aggregation logic: V-Model Checker Map, cross-level ID registry, broken-chain reconstruction, heat-map formula, and consolidated quality report template. |
| [traceability-dashboard/SKILL.md](traceability-dashboard/SKILL.md) | `traceability-dashboard` | Use when generating or reviewing human-readable KPI dashboards for ASPICE V-Model traceability and quality summarization. Provides KPI definitions, page sections, data-model guidance, and visual/reporting patterns for static HTML dashboards built from traceability artifacts and checker outputs. |
| [coverage-workflow/SKILL.md](coverage-workflow/SKILL.md) | `coverage-workflow` | gcovr coverage measurement workflow for SWE.3 unit construction: local build with COVERAGE=ON, test execution, and report generation. |
| [use-case-writing/SKILL.md](use-case-writing/SKILL.md) | `use-case-writing` | Format patterns for use case `.md` files and `doc/<component>/index.md` navigation hubs; worked calculator example. |
| [test-body-conventions/SKILL.md](test-body-conventions/SKILL.md) | `test-body-conventions` | GTest test body conventions for AAA pattern, assertion selection, and fixture usage. |
| [test-design-techniques/SKILL.md](test-design-techniques/SKILL.md) | `test-design-techniques` | Systematic test design techniques: equivalence partitioning, boundary value analysis, and decision table coverage. |
| [test-implementation-mismatch/SKILL.md](test-implementation-mismatch/SKILL.md) | `test-implementation-mismatch` | Escalation protocol when a test build reveals an API mismatch between spec prose and current `src/` headers. Use when a compiler or linker error indicates a missing or changed symbol. |

## Technology Reference

| Path | Name | Description |
|---|---|---|
| [posix-shared-memory/SKILL.md](posix-shared-memory/SKILL.md) | `posix-shared-memory` | POSIX shared memory API reference (`shm_open`, `mmap`, `munmap`, `shm_unlink`, `ftruncate`) with usage patterns and pitfalls. |
| [unix-domain-sockets/SKILL.md](unix-domain-sockets/SKILL.md) | `unix-domain-sockets` | Unix Domain Sockets (UDS) API reference and C++ implementation patterns. |
| [uds-fd-passing/SKILL.md](uds-fd-passing/SKILL.md) | `uds-fd-passing` | `sendmsg`/`recvmsg` API reference and patterns for passing file descriptors over AF_UNIX sockets using `SCM_RIGHTS`. |
| [vlan-kmatrix/SKILL.md](vlan-kmatrix/SKILL.md) | `vlan-kmatrix` | E3 VLAN K-Matrix reference data for CARIAD SE TX-XN VLAN connectivity and module configuration. |

## C++ Reference

| Path | Name | Description |
|---|---|---|
| [cpp-mocking-strategies/SKILL.md](cpp-mocking-strategies/SKILL.md) | `cpp-mocking-strategies` | Worked examples for IFoo+GMock, template policy injection, and link-seam substitution. |
| [cpp-callbacks/SKILL.md](cpp-callbacks/SKILL.md) | `cpp-callbacks` | Code examples for all four C++ callback patterns with CP10 naming and `.clang-format` brace style. |

## Agent Quality Assurance

| Path | Name | Description |
|---|---|---|
| [ab-agent-testing/SKILL.md](ab-agent-testing/SKILL.md) | `ab-agent-testing` | A/B testing orchestration skill. Instructs the agent to prepare isolated clones, spawn background copilot instances for baseline/improved versions, collect metrics, run statistical comparison, and report results. |
| [cross-model-review/SKILL.md](cross-model-review/SKILL.md) | `cross-model-review` | Protocol for invoking an independent reviewer (different model family) at workflow milestones. Defines invocation contract, independence invariants, fallback behavior, and output schema. Role-specific review templates live in templates/ alongside the skill file. |
| [integration-tester-workflow/SKILL.md](integration-tester-workflow/SKILL.md) | `integration-tester-workflow` | Phase 1 (specification) and Phase 2 (implementation) execution steps for the Integration Tester agent. Load this skill at the start of each phase to get the full T-step procedure, triage gates, and phase transition rules. |
| [qualification-tester-workflow/SKILL.md](qualification-tester-workflow/SKILL.md) | `qualification-tester-workflow` | Phase 1 (specification) and Phase 2 (implementation) execution steps for the Qualification Tester agent. Load this skill at the start of each phase to get the full T-step procedure, triage gates, and phase transition rules. |

## Process & Quality Assessment

| Path | Name | Description |
|---|---|---|
| [hcp5-quality-goals/SKILL.md](hcp5-quality-goals/SKILL.md) | `hcp5-quality-goals` | Machine-readable HCP5 Quality Goals: maturity levels, KPI thresholds, and agent consumption rules. Use when performing quality assessment for HCP5 components. |
| [sop-risk-evaluation/SKILL.md](sop-risk-evaluation/SKILL.md) | `sop-risk-evaluation` | Deterministic KPI-based SOP release risk evaluation for HCP5 Compute Platform: risk classes, thresholds, aggregation logic. Use when evaluating SOP release compliance. |

## Skill-to-Instruction Mapping

Skills listed below provide worked examples that illustrate rules defined in their corresponding instruction files.
Load them on demand when the instruction file alone is insufficient.

| Skill | Governing instruction file(s) |
|---|---|
| [requirements-specification/SKILL.md](requirements-specification/SKILL.md) | [requirements-specification.instructions.md](./../instructions/requirements-specification.instructions.md) |
| [architecture-design/SKILL.md](architecture-design/SKILL.md) | [architecture-specification.instructions.md](./../instructions/architecture-specification.instructions.md) |
| [detailed-design/SKILL.md](detailed-design/SKILL.md) | [detailed-design.instructions.md](./../instructions/detailed-design.instructions.md) |
| [unit-construction/SKILL.md](unit-construction/SKILL.md) | [unit-construction.instructions.md](./../instructions/unit-construction.instructions.md) |
| [unit-test-specification/SKILL.md](unit-test-specification/SKILL.md) | [unit-test-stub.instructions.md](./../instructions/unit-test-stub.instructions.md), [unit-test-body.instructions.md](./../instructions/unit-test-body.instructions.md) |
| [integration-test-specification/SKILL.md](integration-test-specification/SKILL.md) | [integration-test-specification.instructions.md](./../instructions/integration-test-specification.instructions.md) |
| [qualification-test-specification/SKILL.md](qualification-test-specification/SKILL.md) | [qualification-test-specification.instructions.md](./../instructions/qualification-test-specification.instructions.md) |
| [test-implementation-mismatch/SKILL.md](test-implementation-mismatch/SKILL.md) | [test-implementation.instructions.md](./../instructions/test-implementation.instructions.md) |
| [use-case-writing/SKILL.md](use-case-writing/SKILL.md) | [use-case-writing.instructions.md](./../instructions/use-case-writing.instructions.md) |
| [cpp-mocking-strategies/SKILL.md](cpp-mocking-strategies/SKILL.md) | [mock-creation.instructions.md](./../instructions/mock-creation.instructions.md), [testability-design.instructions.md](./../instructions/testability-design.instructions.md) |
| [cpp-callbacks/SKILL.md](cpp-callbacks/SKILL.md) | [cpp-callbacks.instructions.md](./../instructions/cpp-callbacks.instructions.md) |
