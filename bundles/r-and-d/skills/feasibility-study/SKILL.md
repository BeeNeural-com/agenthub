---
name: feasibility-study
description: >-
  Produce a technical and economic feasibility study. Use before committing to a new
  feature, technology adoption, or R&D initiative to assess viability, risks, and effort.
tags: [r-and-d, feasibility, decision]
---

# Feasibility Study

Assess whether an idea, technology, or feature is worth pursuing before full investment.

## When to Use

- Gate between research and engineering commitment
- Evaluating a technology scouting recommendation
- Responding to "should we build this?" questions
- Preparing input for PI planning or epic creation

## Procedure

### Step 1: Problem statement

- What problem are we solving?
- Who benefits and how?
- What happens if we do nothing?

### Step 2: Technical feasibility

- Required capabilities and gaps
- Dependencies on other teams or systems
- Proof points (existing POCs, benchmarks, prototypes)
- Technical risks and unknowns

### Step 3: Economic feasibility

- Rough effort estimate (T-shirt: S/M/L/XL or person-weeks)
- Infrastructure and license costs
- Maintenance burden
- Opportunity cost vs alternatives

### Step 4: Operational feasibility

- Team skills and availability
- Timeline constraints
- Compliance, security, or safety requirements

### Step 5: Recommendation

Choose one:
- **Proceed** — with conditions and next steps
- **Spike first** — time-boxed prototype-spike before decision
- **Defer** — revisit when conditions change
- **Reject** — with documented rationale

Use `references/feasibility-template.md` for the deliverable.

## Output

Save as `doc/research/feasibility-<topic>.md`.
