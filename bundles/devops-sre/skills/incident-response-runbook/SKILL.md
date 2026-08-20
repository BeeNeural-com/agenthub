---
name: incident-response-runbook
description: >-
  Create and execute incident response runbooks for detection, mitigation, and communication. Use during active incidents or runbook authoring.
tags: [devops-sre, incident]
---

# Incident Response Runbook

## When to Use

- Active production incident (SEV1–SEV3)
- Authoring service-specific incident runbook
- On-call training and game day preparation

## Procedure

### Step 1: Detect and declare

- Confirm alert is not false positive
- Assign incident commander and severity
- Open incident channel and status page if SEV1/2

### Step 2: Mitigate

- Stop the bleeding: rollback, scale, disable feature
- Preserve evidence: logs, traces, recent deploys
- Time-box investigation spikes; prefer known fixes

### Step 3: Communicate

- Internal updates every 15–30 min for SEV1
- Customer comms via approved templates
- Document timeline in incident doc in real time

### Step 4: Resolve and handoff

- Confirm metrics restored and error budget impact
- Schedule postmortem per **incident-postmortem**
- Create follow-up tickets with owners

## Output

Active: incident doc in tracker. Runbook: `doc/runbooks/incident-<service>.md`.
