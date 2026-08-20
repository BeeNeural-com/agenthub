---
name: dashboard-design
description: >-
  Spec KPI dashboards with layout, filters, and drill paths. Use when building BI dashboards for teams or executives.
tags: [data-analytics, dashboard]
---

# Dashboard Design

## When to Use

- New Looker/Tableau/Power BI dashboard request
- Redesign of unused or confusing dashboard
- Executive metrics review preparation

## Procedure

### Step 1: Audience and decisions

- Who views daily vs weekly; what decisions they make
- One primary question per dashboard
- Mobile vs desktop usage

### Step 2: Metric selection

- Use **kpi-definition** for each tile
- Leading vs lagging indicators balance
- Max 7±2 tiles above fold

### Step 3: Layout and interaction

- F-pattern: summary top-left
- Global filters: date, region, product
- Drill to detail with row-level security

### Step 4: Validation

- Reconcile totals to source reports
- User test with 2 representative viewers
- Document refresh schedule and owner

## Output

Spec at `doc/analytics/dashboard-<name>.md`.
