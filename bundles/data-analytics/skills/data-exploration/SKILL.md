---
name: data-exploration
description: >-
  Exploratory data analysis workflow: profiling, distributions, anomalies. Use when understanding a new dataset.
tags: [data-analytics, data]
---

# Data Exploration

## When to Use

- New data source for analytics project
- Unexpected metric movement investigation
- Pre-modeling data understanding

## Procedure

### Step 1: Understand schema

- Column types, null rates, cardinality
- Primary keys and relationship guesses
- Sample rows and time range coverage

### Step 2: Profile distributions

- Histograms for numeric; value counts for categorical
- Detect outliers and impossible values
- Compare segments (region, product, cohort)

### Step 3: Hypothesis sketch

- Note patterns worth deeper **statistical-analysis**
- Document data quality issues for upstream fix
- Avoid concluding causation from correlation alone

### Step 4: Share findings

- Executive summary with 3 key charts
- Reproducible notebook or SQL scripts
- Recommend next analysis steps

## Output

Notebook or report at `doc/analytics/eda-<topic>.md`.
