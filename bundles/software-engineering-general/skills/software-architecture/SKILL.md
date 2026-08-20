---
name: software-architecture
description: >-
  Apply architecture principles, patterns, and trade-off analysis for maintainable systems. Use for structural decisions within a codebase.
tags: [software-engineering-general, software]
---

# Software Architecture

## When to Use

- Evaluating module boundaries in a growing codebase
- Introducing a new architectural pattern
- Architecture review before major refactor

## Procedure

### Step 1: Context and constraints

- Team size, skill mix, and delivery timeline
- Quality attributes: modifiability, performance, security
- Existing architecture style and migration cost

### Step 2: Evaluate patterns

- Layered, hexagonal, event-driven, microservices — fit to context
- Document pros/cons for this system
- Reference SOLID and coupling/cohesion analysis

### Step 3: Decision record

- Capture decision, status, consequences
- Link to **technical-rfc** for cross-team decisions
- Identify validation milestones

### Step 4: Governance

- Define architecture fitness functions or lint rules
- Schedule periodic architecture reviews
- Align with **system-design** for distributed aspects

## Output

ADR in `doc/engineering/adr-<number>-<title>.md`.
