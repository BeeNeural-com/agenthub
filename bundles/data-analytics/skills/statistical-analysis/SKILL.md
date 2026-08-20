---
name: statistical-analysis
description: >-
  Apply appropriate statistical tests and interpret results with uncertainty. Use for experiments and hypothesis testing.
tags: [data-analytics, statistical]
---

# Statistical Analysis

## When to Use

- A/B test or experiment readout
- Comparing groups with significance testing
- Forecast confidence intervals

## Procedure

### Step 1: Frame hypothesis

- Null and alternative hypotheses
- Primary metric and guardrail metrics
- Minimum detectable effect if power analysis needed

### Step 2: Check assumptions

- Sample size and randomization quality
- Normality or use non-parametric tests
- Multiple comparison correction if many tests

### Step 3: Run analysis

- Report effect size, not only p-value
- Include confidence intervals
- Segment analysis with multiplicity caution

### Step 4: Interpret

- Practical vs statistical significance
- Limitations and confounders
- Recommendation: ship, extend test, or stop

## Output

Report at `doc/analytics/analysis-<experiment>.md`.
