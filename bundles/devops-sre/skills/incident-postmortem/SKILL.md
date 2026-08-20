---
name: incident-postmortem
description: >-
  Facilitate blameless postmortems with timeline, root cause, and action items. Use within 5 business days of incident resolution.
tags: [devops-sre, incident]
---

# Incident Postmortem

## When to Use

- After SEV1–SEV3 incident closure
- Recurring incident pattern needs systemic fix
- Game day or chaos exercise debrief

## Procedure

### Step 1: Gather timeline

- Collect UTC timestamps for detect, respond, mitigate, resolve
- Include deploy events, config changes, external deps
- Use scribe notes from incident channel

### Step 2: Root cause analysis

- Apply 5-whys or fault tree without blaming people
- Distinguish trigger vs contributing factors
- Note what went well in response

### Step 3: Action items

- Each item: owner, due date, priority, verification method
- Prefer preventive fixes over manual toil
- Track in same system as engineering backlog

### Step 4: Publish and share

- Review draft with incident participants
- Share summary org-wide for SEV1
- Link related runbook updates

## Output

Save as `doc/incidents/postmortem-<id>.md`.
