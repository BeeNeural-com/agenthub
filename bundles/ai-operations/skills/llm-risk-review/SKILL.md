---
name: llm-risk-review
description: >-
  Review LLM features for safety, bias, data leakage, and abuse scenarios. Use before launch or after incidents.
tags: [ai-operations, llm]
---

# LLM Risk Review

## When to Use

- Pre-launch review of customer-facing LLM feature
- Red-team findings need remediation plan
- Policy update for AI governance tier

## Procedure

### Step 1: Data risks

- Training/fine-tune data provenance and consent
- Prompt/response logging and retention
- Cross-tenant leakage in RAG indexes

### Step 2: Safety and abuse

- Jailbreak and prompt injection test cases
- Harmful content categories and refusals
- Rate limits and anomaly detection

### Step 3: Fairness and bias

- Test across demographic slices where applicable
- Document known limitations in UX
- Human review path for high-stakes outputs

### Step 4: Sign-off

- Assign risk tier T0–T3
- List required mitigations before GA
- Schedule periodic re-review

## Output

Risk assessment at `doc/ai/risk-review-<feature>.md`.
