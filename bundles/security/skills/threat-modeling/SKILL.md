---
name: threat-modeling
description: >-
  Systematic threat analysis using STRIDE or attack trees for features and systems. Use during design or security review.
tags: [security, threat]
---

# Threat Modeling

## When to Use

- New feature handling auth, payments, or sensitive data
- Architecture change with expanded attack surface
- Annual security review of critical service

## Procedure

### Step 1: Diagram system

- Data flow diagram with trust boundaries
- Entry points, assets, and external dependencies
- Identify STRIDE categories per component

### Step 2: Identify threats

- Spoofing, tampering, repudiation, info disclosure, DoS, elevation
- Prioritize by likelihood × impact
- Note existing controls

### Step 3: Mitigations

- Map threats to controls or new work items
- Accept residual risk with sign-off for low items
- Link to **owasp-top10-review** where applicable

### Step 4: Track

- Store model with version and review date
- Re-run on major design changes
- Feed findings to sprint backlog

## Output

Threat model at `doc/security/threat-model-<system>.md`.
