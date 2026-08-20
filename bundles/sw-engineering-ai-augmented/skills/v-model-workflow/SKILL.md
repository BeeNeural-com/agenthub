---
name: v-model-workflow
description: "Use when you need the repository's full ASPICE V-Model delegation map. Provides SWE.1-SWE.6 owners, skill/instruction links, output directories, and handoff flow per level."
---

# ASPICE V-Model Workflow Reference

This skill documents the complete agent delegation structure for each V-Model level. Use it to understand which role agent owns a level, which skills and instructions govern it, and how artifacts flow between levels.

For the agent discovery index (who exists, SIPOC chain, guardrails): see `.github/AGENTS.md`.

---

## SWE.1: Component Software Requirements

| Aspect | Value |
|---|---|
| **Owner** | Requirements Engineer (`requirements-engineer.agent.md`) |
| **Entry point** | `.github/prompts/requirements-engineer.prompt.md` |
| **Output** | `doc/<component>/component_requirements/` |
| **Skills** | `requirements-specification`, `requirements-gap-analysis`, `aspice-bp-reference` (SWE.1 Review) |
| **Instructions** | `requirements-specification.instructions.md` (applied to `**/component_requirements/**/*.md`) |
| **Subagent personas** | Requirements Writer, Gap Analysis, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Read existing requirements; produce task plan.
2. Run gap analysis before writing.
3. Write/edit `req:` blocks in topic files.
4. Run review (RC01-RC11) and coverage check.
5. Hand off to SWE.2 (Software Architect).

---

## SWE.2: Software Architectural Design

| Aspect | Value |
|---|---|
| **Owner** | Software Architect (`software-architect.agent.md`) |
| **Entry point** | `.github/prompts/software-architect.prompt.md` |
| **Output** | `doc/<component>/component_architecture/` |
| **Skills** | `architecture-design`, `aspice-bp-reference` (SWE.2 Review) |
| **Instructions** | `architecture-specification.instructions.md` (applied to `**/component_architecture/**/*.md`) |
| **Subagent personas** | Architecture Design, Interface Design, Dynamic Behavior, Consistency Checker, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Read all SWE.1 files; produce task plan.
2. Define `arch:` specification blocks in Markdown topic files (with `classification:` metadata).
3. Run consistency checker and review.
4. Run traceability checker (SWE.1 bidirectional) and coverage checker (SWE.5 readiness).
5. Hand off to SWE.3 (Software Designer) and SWE.5 (Integration Tester).

---

## SWE.3: Software Detailed Design and Unit Construction

| Aspect | Value |
|---|---|
| **Owner** | Software Designer (design + stubs), Software Implementer (mocks + production code) |
| **Entry points** | `.github/prompts/software-designer.prompt.md`, `.github/prompts/software-implementer.prompt.md` |
| **Output** | `src/*.h` + `src/I*.h` (Designer); `src/*.cpp` (Implementer) |
| **Skills** | `detailed-design`, `unit-construction`, `cpp-mocking-strategies`, `aspice-bp-reference` (SWE.3 Review) |
| **Instructions** | `detailed-design.instructions.md`, `testability-design.instructions.md`, `unit-construction.instructions.md`, `mock-creation.instructions.md`, `cpp-naming-conventions.instructions.md`, `sca-compliance.instructions.md` |
| **Subagent personas** | Detailed Design, Unit Construction, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Software Designer reads SWE.2, writes `@elaborates` headers + `IFoo` interfaces.
2. Software Implementer creates mocks (Stage 1), implements production `.cpp` (Stage 3).
3. Run coverage checker (all `arch:` have headers and implementations).

---

## SWE.4: Software Unit Verification

| Aspect | Value |
|---|---|
| **Owner** | Software Designer (spec + stubs), Software Implementer (AAA bodies, RED to GREEN) |
| **Entry points** | `.github/prompts/software-designer.prompt.md`, `.github/prompts/software-implementer.prompt.md` |
| **Output** | `tests/unit/*_test.cpp` (stubs by Designer; bodies by Implementer), `tests/unit/*_test_fixture.h` |
| **Skills** | `unit-test-specification`, `aspice-bp-reference` (SWE.4 Review) |
| **Instructions** | `unit-test-stub.instructions.md` (Designer), `unit-test-body.instructions.md` (Implementer) |
| **Subagent personas** | Test Specification Writer, Test Implementation Writer, Test Runner, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Software Designer reads `@elaborates` headers, writes spec blocks + `FAIL()` stubs.
2. Software Implementer creates mocks (Stage 1), implements AAA bodies to RED (Stage 2), then production code to GREEN (Stage 3).
3. Run coverage checker (XML parse, risk table).

---

## SWE.5: Software Integration Testing

| Aspect | Value |
|---|---|
| **Owner** | Integration Tester (`integration-tester.agent.md`) |
| **Entry point** | `.github/prompts/integration-tester.prompt.md` |
| **Output** | `doc/<component>/component_integration_tests/` (Markdown), `tests/integration/` (GTest) |
| **Skills** | `integration-test-specification`, `test-design-techniques`, `test-body-conventions`, `aspice-bp-reference` (SWE.5 Review) |
| **Instructions** | `test-specification.instructions.md` (shared base), `integration-test-specification.instructions.md` (SWE.5 delta), `test-implementation.instructions.md` |
| **Subagent personas** | Test Specification Writer, Test Implementation Writer, Test Runner, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Verify SWE.2 exists; validate `_briefing.md`; apply integration scope filter.
2. Phase 1: Classify coverage, design test conditions (T2a: produce design table per `test-design-techniques` skill), write TCASE specs + GTest stubs (T2b), run spec review (IR01-IR08).
3. Phase 2: Implement cross-element AAA bodies, build + run (`./build.sh --docker integration_tests`), produce coverage table.

---

## SWE.6: Software Qualification Testing

| Aspect | Value |
|---|---|
| **Owner** | Qualification Tester (`qualification-tester.agent.md`) |
| **Entry point** | `.github/prompts/qualification-tester.prompt.md` |
| **Output** | `doc/<component>/component_qualification_tests/` (Markdown), `tests/qualification/` (GTest) |
| **Skills** | `qualification-test-specification`, `test-design-techniques`, `test-body-conventions`, `aspice-bp-reference` (SWE.6 Review) |
| **Instructions** | `test-specification.instructions.md` (shared base), `qualification-test-specification.instructions.md` (SWE.6 delta), `test-implementation.instructions.md` |
| **Subagent personas** | Test Specification Writer, Test Implementation Writer, Test Runner, Review, Coverage Checker, Traceability Checker, Change Impact |

**Workflow:**
1. Read all SWE.1 files; validate `_briefing.md`; filter testable requirements; classify coverage.
2. Phase 1: Classify coverage, design test conditions (T2a: produce design table per `test-design-techniques` skill), write TCASE specs + GTest stubs (T2b, black-box); run spec review (QR01-QR08).
3. Phase 2: Implement black-box AAA bodies, build + run (`./build.sh --docker qualification_tests`), produce coverage table.

---

## Handoff Flow (SIPOC)

```
Consultant → Function Owner → Requirements Engineer (SWE.1)
  → Software Architect (SWE.2)
    → Software Designer (SWE.3 design + SWE.4 stubs)
      → Software Implementer (SWE.3 construction + SWE.4 bodies)
    → Integration Tester (SWE.5)
    → Qualification Tester (SWE.6)
  → Auditor (cross-level quality)
```

Each arrow represents a handoff that requires a human checkpoint (GR-03).
