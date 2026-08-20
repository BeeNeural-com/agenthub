---
name: prd-writer
description: >-
  Write product requirements documents with problem context, goals, scope, and acceptance criteria. Use when defining a new feature or major enhancement for engineering handoff.
tags: [product-management, prd]
---

# PRD Writer

## When to Use

- Starting a new feature from validated discovery
- Consolidating stakeholder input into a single source of truth
- Preparing handoff from product to engineering sprint

## Procedure

### Step 1: Problem and goals

- State user problem, target persona, and business outcome
- Define success metrics (primary + guardrails)
- List non-goals explicitly to prevent scope creep

### Step 2: Solution overview

- Describe user journey at high level (not UI mockups unless ready)
- Identify dependencies on other teams or systems
- Note technical constraints from engineering preview

### Step 3: Requirements

- Number functional requirements (FR-001…)
- Add acceptance criteria in Given/When/Then format
- Include edge cases, error states, and accessibility needs

### Step 4: Rollout and analytics

- Define launch phases (internal, beta, GA)
- List events and dashboards for success measurement
- Document support and documentation implications

## Output

Save as `doc/product/prd-<feature>.md` and link from roadmap item.
