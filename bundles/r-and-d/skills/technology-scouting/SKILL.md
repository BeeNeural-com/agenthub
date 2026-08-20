---
name: technology-scouting
description: >-
  Structured technology scouting and competitive landscape analysis. Use when evaluating
  new technologies, comparing vendors or frameworks, assessing market alternatives, or
  preparing a technology recommendation for R&D or architecture decisions.
tags: [r-and-d, research, scouting, technology]
---

# Technology Scouting

Systematically evaluate technologies, vendors, and approaches before committing engineering effort.

## When to Use

- Choosing between frameworks, platforms, or vendors
- Entering a new technical domain
- Preparing input for feasibility studies or architecture decisions
- Supporting the Consultant or research-analyst agent

## Procedure

### Step 1: Define the scouting question

Document:
- Decision to be made
- Constraints (cost, latency, compliance, team skills)
- Must-have vs nice-to-have criteria
- Time horizon (prototype vs production)

### Step 2: Identify candidates

- Internal: existing stack, prior POCs, team expertise
- External: industry leaders, open source, commercial products
- Aim for 3–5 viable candidates

### Step 3: Gather evidence

For each candidate collect:
- Official documentation and release cadence
- Community size, maintenance status, license
- Case studies in similar domains
- Known limitations and failure modes
- Integration complexity with existing systems

### Step 4: Score candidates

Use a weighted matrix (see `references/scouting-matrix.md`). Minimum criteria:
- Technical fit
- Maturity / TRL
- Cost (license + ops + learning curve)
- Risk (vendor lock-in, security, compliance)
- Team readiness

### Step 5: Deliver recommendation

Output a scouting report with:
- Executive summary (1 paragraph)
- Comparison table
- Recommended option with rationale
- Risks and mitigations
- Suggested next step (spike, PoC, or reject)

## Output Format

Save as `doc/research/technology-scouting-<topic>.md` when working in a component repo.
