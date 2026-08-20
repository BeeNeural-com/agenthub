---
name: ci-cd-pipeline
description: >-
  Design and review CI/CD pipelines with build, test, security gates, and artifact promotion. Use when creating or improving delivery automation.
tags: [devops-sre, ci]
---

# CI/CD Pipeline

## When to Use

- New service needs automated build and deploy
- Pipeline is slow, flaky, or bypassed by teams
- Adding security or compliance gates to delivery

## Procedure

### Step 1: Map current flow

- Document trigger events (PR, main merge, tag)
- List stages: lint, unit, integration, build, deploy
- Identify manual steps and mean time to feedback

### Step 2: Design pipeline stages

- Fail fast: cheapest checks first
- Parallelize independent jobs; cache dependencies
- Pin tool versions and use reproducible builds

### Step 3: Add quality gates

- Block merge on test coverage threshold if policy exists
- Run SAST/secret scan per **secrets-scanning**
- Require approval for production promotion

### Step 4: Operationalize

- Define artifact naming and retention
- Document rollback via **deployment-strategy**
- Monitor pipeline metrics (duration, flake rate)

## Output

Save pipeline spec as `doc/platform/ci-cd-<service>.md` and implement in CI config.
