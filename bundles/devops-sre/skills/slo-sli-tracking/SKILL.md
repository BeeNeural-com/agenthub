---
name: slo-sli-tracking
description: >-
  Define SLIs, SLOs, error budgets, and alerting policies for services. Use when establishing or reviewing reliability targets.
tags: [devops-sre, slo]
---

# SLO/SLI Tracking

## When to Use

- New service going to production
- Error budget exhausted or alert fatigue review
- Quarterly reliability review with product

## Procedure

### Step 1: Choose SLIs

- Pick user-centric signals: availability, latency, correctness
- Define measurement window and aggregation (p99, success rate)
- Avoid monitoring only infrastructure metrics

### Step 2: Set SLO targets

- Align target with user expectations and contract SLAs
- Document rationale for chosen percentage
- Calculate error budget per period

### Step 3: Alerting policy

- Multi-window burn rate alerts for budget consumption
- Page only for SLO-threatening conditions
- Ticket for sub-SLO trends within budget

### Step 4: Review cadence

- Weekly error budget review with product owner
- Freeze features if budget exhausted (policy-dependent)
- Adjust SLOs with data, not optimism

## Output

Save as `doc/platform/slo-<service>.md` with dashboard links.
