---
name: code-review
description: >-
  Review pull requests for correctness, readability, security, and maintainability. Use for PR-level review distinct from full-repo structured audits.
tags: [software-engineering-general, code]
---

# Code Review

## When to Use

- Reviewing a teammate's pull request before merge
- Self-review checklist before requesting review
- Teaching standards through constructive PR feedback

## Procedure

### Step 1: Understand change intent

- Read PR description, linked ticket, and test plan
- Identify scope: bugfix, feature, refactor, chore
- Note files outside expected scope for discussion

### Step 2: Evaluate correctness

- Trace happy path and edge cases mentally or via tests
- Check error handling and resource cleanup
- Verify concurrency and transaction boundaries if applicable

### Step 3: Assess quality

- Naming clarity and function size
- Duplication vs appropriate abstraction
- Test coverage for changed behavior

### Step 4: Security and performance

- Input validation, authz, injection risks
- N+1 queries, unbounded loops, memory leaks
- Flag secrets or PII in logs

### Step 5: Provide feedback

- Separate blocking vs nit vs suggestion
- Explain why, not just what
- Approve when blocking issues resolved

## Output

PR comments in tracker; optional summary in review thread.
