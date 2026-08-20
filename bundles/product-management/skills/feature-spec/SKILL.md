---
name: feature-spec
description: >-
  Detailed feature specification with user flows, data model, and API touchpoints. Use when PRD is approved and engineering needs implementation detail.
tags: [product-management, feature]
---

# Feature Spec

## When to Use

- Engineering kickoff for a scoped feature
- Breaking an epic into implementable specification
- Aligning design and engineering on behavior

## Procedure

### Step 1: Context

- Link parent PRD and related user stories
- Summarize scope boundary for this spec
- List open questions with owners

### Step 2: User flows

- Document happy path and primary alternates
- Include state diagrams for complex interactions
- Define empty, loading, and error states

### Step 3: Technical design

- Outline data model changes and migrations
- List API endpoints or events with payloads
- Note performance, security, and i18n requirements

### Step 4: Test plan

- Map acceptance criteria to test types (unit, integration, E2E)
- Identify feature flags and rollback plan
- Define demo script for sprint review

## Output

Save as `doc/product/spec-<feature>.md`.
