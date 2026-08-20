---
name: prototype-spike
description: >-
  Time-boxed proof-of-concept and spike methodology. Use when validating a technical
  hypothesis quickly with minimal code before full implementation commitment.
tags: [r-and-d, prototype, spike, poc]
---

# Prototype Spike

Validate unknowns fast with a bounded, disposable proof of concept.

## When to Use

- Feasibility study recommends "spike first"
- High uncertainty in integration, performance, or API
- Before committing sprint capacity to full implementation

## Rules

1. **Time-box** — default 1–3 days; never exceed 1 week without re-approval
2. **Disposable** — spike code is throwaway unless explicitly promoted
3. **One question** — each spike answers exactly one critical question
4. **Measurable** — define pass/fail before starting (link to experiment-design)

## Procedure

### Step 1: Spike charter

Document in `doc/spikes/spike-<id>.md`:
- Question to answer
- Success criteria
- Time box and owner
- Out of scope (what the spike will NOT do)

### Step 2: Minimal implementation

- Smallest code path to test the hypothesis
- Hardcode config if it saves time
- No production-quality error handling required

### Step 3: Run and record

- Execute experiment per experiment-design skill
- Log results per experiment-logging rule

### Step 4: Decision

- **Promote** — create epic/requirements for real implementation
- **Pivot** — try alternative approach (new spike)
- **Stop** — document why and archive

Pair with **prototype-engineer** agent for execution.
