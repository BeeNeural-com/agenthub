---
name: kpi-definition
description: >-
  Define metrics with formula, grain, owner, and targets. Use when teams disagree on numbers or building new scorecards.
tags: [data-analytics, kpi]
---

# KPI Definition

## When to Use

- New product or business KPI needed
- Metric mismatch between teams
- OKR or executive scorecard setup

## Procedure

### Step 1: Name and purpose

- Business question the KPI answers
- Single owner accountable for definition
- Category: growth, quality, efficiency, satisfaction

### Step 2: Formula

- Numerator, denominator, filters, inclusions/exclusions
- Grain: user, account, order, day
- SQL or pseudocode for implementation

### Step 3: Targets and thresholds

- Baseline historical value
- Target and alert thresholds
- Review cadence (weekly/monthly/quarterly)

### Step 4: Governance

- Version definition changes in changelog
- Link dashboard tiles to this doc
- Align with finance definitions where overlapping

## Output

Catalog entry at `doc/analytics/kpi/<metric-id>.md`.
