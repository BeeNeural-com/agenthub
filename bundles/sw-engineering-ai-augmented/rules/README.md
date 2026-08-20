# Instructions — Table of Contents

> **Agents:** Consult this index when you are unsure which instruction file governs the artifact you are about to write or review. VS Code injects instructions automatically for matching `applyTo` globs, but instructions with narrow `applyTo` patterns (e.g., `change-impact`, `traceability-checker`, `role-agent`) must be loaded explicitly. If you are adding a new file type or agent that has no explicit `> See:` pointer in your agent file, scan this table first.

Each file defines format rules, naming conventions, or structural constraints for a specific file type or agent persona.
Instructions are injected automatically by VS Code Copilot when the edited file matches the `applyTo` glob.

## Writing Quality

| File | `applyTo` | Purpose |
|---|---|---|
| [grammar.instructions.md](grammar.instructions.md) | `**/*` | Em-dash prohibition, active voice, sentence structure, and abbreviation-expansion rules for all project text |

## Agent Infrastructure

| File | `applyTo` | Purpose |
|---|---|---|
| [role-agent.instructions.md](role-agent.instructions.md) | `.github/agents/*.agent.md` | Runtime governance rules and pitfalls for all role agents; SIPOC chain enforcement and delegation constraints |
| [role-agent-creation.instructions.md](role-agent-creation.instructions.md) | `.github/agents/_agent-template.md` | Required structure, section formats, SIPOC paragraph conventions, and Plan-First gate scaffolding — injected only when creating a new agent from the template |
| [agent-self-improvement.instructions.md](agent-self-improvement.instructions.md) | `**/*.agent.md` | End-of-session self-improvement protocol for all agent files |
| [skill-authoring.instructions.md](skill-authoring.instructions.md) | `.github/skills/**/*.md` | Required structure, naming conventions, and content constraints for SKILL.md files |

## Architecture (SWE.2)

| File | `applyTo` | Purpose |
|---|---|---|
| [architecture-specification.instructions.md](architecture-specification.instructions.md) | `**/doc/*/component_architecture/**/*.md` | Consolidated conventions for writing SWE.2 architectural design documents (elements, interfaces, dynamic behavior) |

## Requirements (SWE.1)

| File | `applyTo` | Purpose |
|---|---|---|
| [requirements-specification.instructions.md](requirements-specification.instructions.md) | `**/doc/*/component_requirements/**/*.md` | Conventions for writing SWE.1 component software requirements |

## Detailed Design & Construction (SWE.3)

| File | `applyTo` | Purpose |
|---|---|---|
| [detailed-design.instructions.md](detailed-design.instructions.md) | `**/src/**/*.{h,hpp}` | SWE.3 C++ header authoring: `@elaborates` annotations and Doxygen structure |
| [unit-construction.instructions.md](unit-construction.instructions.md) | `**/src/**/*.cpp` | SWE.3 C++ source file conventions: CP01–CP13 coding principles and `SRC_FILES` registration |
| [cpp-naming-conventions.instructions.md](cpp-naming-conventions.instructions.md) | `**/src/**/*.{h,hpp,cpp}` | CP10 naming conventions, always active on all `src/` files |
| [sca-compliance.instructions.md](sca-compliance.instructions.md) | `**/src/**/*.{h,hpp,cpp},`<br>`**/tests/**/*.cpp` | Parasoft zero-findings mandate, always active on all production and test source files |
| [cpp-callbacks.instructions.md](cpp-callbacks.instructions.md) | `**/src/**/*.{h,hpp,cpp}` | Pattern selection and rules for callback extension in C++ library classes |
| [testability-design.instructions.md](testability-design.instructions.md) | `**/src/**/*.{h,hpp}` | Injectable-interface header rules and dependency classification for unit testability |

## Testing (SWE.4 / SWE.5 / SWE.6)

| File | `applyTo` | Purpose |
|---|---|---|
| [unit-test-stub.instructions.md](unit-test-stub.instructions.md) | `**/tests/unit/**/*.cpp` | SWE.4 Doxygen spec block and `FAIL()` stub format above `TEST_F` macros (Software Designer) |
| [unit-test-body.instructions.md](unit-test-body.instructions.md) | `**/tests/unit/**/*.cpp` | SWE.4 AAA test body implementation rules (Software Implementer) |
| [mock-creation.instructions.md](mock-creation.instructions.md) | `**/tests/unit/mocks/**` | GMock header creation and wiring rules for `IFoo` interfaces |
| [test-specification.instructions.md](test-specification.instructions.md) | `**/component_integration_tests/**/*.md,`<br>`**/component_qualification_tests/**/*.md` | Shared TCASE format: YAML structure, body requirements, status lifecycle, coverage model |
| [integration-test-specification.instructions.md](integration-test-specification.instructions.md) | `**/component_integration_tests/**/*.md` | SWE.5 delta: arch-ID traceability, Integration Strategy section, IR01–IR08 review criteria |
| [qualification-test-specification.instructions.md](qualification-test-specification.instructions.md) | `**/component_qualification_tests/**/*.md` | SWE.6 delta: req-ID traceability, black-box proxy patterns, QR01–QR08 review criteria |
| [test-implementation.instructions.md](test-implementation.instructions.md) | `**/tests/integration/**/*.{cpp,h},`<br>`**/tests/qualification/**/*.{cpp,h}` | Single source of truth for integration and qualification `.cpp` implementation rules |
| _(moved to skill)_ | — | Mismatch escalation protocol is now a skill: `.github/skills/test-implementation-mismatch/SKILL.md` |

## Audit & Traceability

| File | `applyTo` | Purpose |
|---|---|---|
| [traceability-checker.instructions.md](traceability-checker.instructions.md) | `**/agents/**/*traceability-checker*,`<br>`**/agents/**/*coverage-checker*` | Read-only mandate and set-arithmetic protocol for traceability and coverage checker agents |
| [change-impact.instructions.md](change-impact.instructions.md) | `**/agents/**/*change-impact*` | Read-only mandate for change impact agents; blast-radius report protocol |

## Documentation

| File | `applyTo` | Purpose |
|---|---|---|
| [use-case-writing.instructions.md](use-case-writing.instructions.md) | `**/use_cases/**/*.md` | Rules for writing use-case documents for software component stacks |
