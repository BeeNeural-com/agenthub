---
name: testing-strategy
description: >-
  Define test pyramid, coverage goals, and test types for a project or release. Use when test approach is ad hoc or quality gaps appear.
tags: [software-engineering-general, testing]
---

# Testing Strategy

## When to Use

- New project test setup
- Release quality gate definition
- High escape rate from production bugs

## Procedure

### Step 1: Assess context

- System type: API, UI, batch, embedded
- Risk areas: payments, auth, data integrity
- Current test inventory and CI runtime budget

### Step 2: Design pyramid

- Unit: fast, isolated, high count
- Integration: contracts between modules/services
- E2E: critical user journeys only

### Step 3: Define policies

- Coverage targets per layer (not single global %)
- Required tests for bug fixes and new features
- Flake quarantine and SLA to fix

### Step 4: Tooling and CI

- Select frameworks aligned to stack
- Parallelize CI; cache fixtures
- Report test metrics in release checklist

## Output

Save as `doc/engineering/testing-strategy.md`.
