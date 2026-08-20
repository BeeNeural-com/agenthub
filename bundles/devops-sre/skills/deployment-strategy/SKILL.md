---
name: deployment-strategy
description: >-
  Plan deployment approaches: rolling, blue/green, canary, and feature flags. Use before production releases or architecture changes.
tags: [devops-sre, deployment]
---

# Deployment Strategy

## When to Use

- Launching a high-risk or high-traffic change
- Designing zero-downtime deployment for a service
- Choosing rollback strategy before release day

## Procedure

### Step 1: Assess change risk

- Classify: config, code, schema, infrastructure
- Estimate blast radius and user impact
- Define success metrics for first hour/day

### Step 2: Select strategy

- Rolling: default for stateless services
- Blue/green: instant switch with double capacity cost
- Canary: progressive traffic shift with automated rollback
- Feature flags: decouple deploy from release

### Step 3: Plan execution

- Write step-by-step runbook with owners
- Define health checks and automatic abort criteria
- Schedule comms for customer-facing changes

### Step 4: Validate rollback

- Test rollback in staging or game day
- Document data migration rollback if applicable
- Set monitoring dashboards for release window

## Output

Save as `doc/platform/deployment-<release>.md`.
