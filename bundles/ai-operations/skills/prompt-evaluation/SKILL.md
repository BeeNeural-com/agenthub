---
name: prompt-evaluation
description: >-
  Build test sets and metrics to regression-test prompts and models. Use before promoting prompt changes to production.
tags: [ai-operations, prompt]
---

# Prompt Evaluation

## When to Use

- Before deploying prompt or model change
- Investigating quality regression in production
- Comparing model candidates

## Procedure

### Step 1: Define eval set

- Cover happy path, edge cases, adversarial inputs
- Include real anonymized production samples
- Label expected outputs or rubric criteria

### Step 2: Choose metrics

- Exact match, LLM-judge, human rubric as appropriate
- Track latency, token cost, refusal rate
- Separate safety eval from task accuracy

### Step 3: Run experiments

- Baseline current production prompt
- A/B candidate prompts on same set
- Statistical note if sample size small

### Step 4: Gate release

- Define pass thresholds per metric
- Document failures and mitigations
- Schedule periodic re-eval as model updates

## Output

Save eval report as `doc/ai/eval-<feature>-<date>.md`.
