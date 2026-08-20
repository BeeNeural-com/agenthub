---
name: test-driven-development
description: >-
  Apply red-green-refactor cycle when implementing behavior. Use for new logic where tests clarify requirements.
tags: [software-engineering-general, test]
---

# Test-Driven Development

## When to Use

- Implementing well-defined business logic
- Bug fix that needs regression test
- Refactoring with safety net

## Procedure

### Step 1: Red — write failing test

- One behavior assertion per test when possible
- Use descriptive test names (should_X_when_Y)
- Confirm test fails for right reason

### Step 2: Green — minimal implementation

- Write simplest code to pass
- Avoid speculative features
- Run full relevant test suite

### Step 3: Refactor — improve design

- Remove duplication while tests stay green
- Improve names and extract functions
- Do not change behavior during refactor

### Step 4: Repeat

- Take next smallest behavior slice
- Keep commits small: test + implementation pairs
- Document any untestable seams for follow-up

## Output

Tests in repo test directory; behavior documented in PR.
