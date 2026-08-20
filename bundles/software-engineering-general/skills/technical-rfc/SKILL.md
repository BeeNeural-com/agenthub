---
name: technical-rfc
description: >-
  Author request-for-comments documents for significant technical decisions. Use when change affects multiple teams or is hard to reverse.
tags: [software-engineering-general, technical]
---

# Technical RFC

## When to Use

- Cross-team protocol or platform change
- Technology adoption with org-wide impact
- Controversial design needing consensus

## Procedure

### Step 1: RFC header

- Title, author, status (draft/proposed/accepted/deprecated)
- Reviewers and decision deadline

### Step 2: Problem and goals

- Context and motivation
- Goals and non-goals
- Success metrics post-implementation

### Step 3: Proposal

- Detailed design with diagrams
- Alternatives considered and rejected
- Migration and rollout plan

### Step 4: Review process

- Comment period and office hours
- Resolve objections or document dissent
- Final decision and ADR linkage

## Output

Save as `doc/engineering/rfc-<number>-<title>.md`.
