---
name: research-to-requirements
description: >-
  Translate R&D findings into component software requirements. Use after feasibility,
  scouting, or research reports to hand off to requirements engineering and SWE.1.
tags: [r-and-d, requirements, handoff, swe]
---

# Research to Requirements

Bridge R&D outputs into actionable component requirements.

## When to Use

- Feasibility study recommends "proceed"
- Research report has actionable recommendations
- Function Owner needs structured input for SWE.1
- Closing the research → engineering gap

## Procedure

### Step 1: Gather inputs

Collect:
- Research report / feasibility study / trade study
- Stakeholder constraints
- Existing component requirements (avoid duplication)

### Step 2: Extract capability statements

Convert findings into "the system shall..." statements:
- One requirement per distinct capability
- Traceable to research evidence (source ID)
- Testable and unambiguous

### Step 3: Classify requirements

| Type | Examples |
|------|----------|
| Functional | Behaviors enabled by research |
| Non-functional | Performance, security, reliability from study |
| Constraint | Regulatory, IP, technology choices |

### Step 4: Prioritize

- Must-have for MVP vs future phase
- Link to epic or initiative if known

### Step 5: Handoff

Deliver to **function-owner** or **requirements-engineer** agent.

Use bundle skill **requirements-writing** for formatting.

Use `references/handoff-template.md`.

## Traceability

Each requirement must cite: `[research:<doc-id>:section]`
