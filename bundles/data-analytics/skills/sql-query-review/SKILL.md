---
name: sql-query-review
description: >-
  Review and improve SQL for correctness, performance, and safety. Use before running analytics or production queries.
tags: [data-analytics, sql]
---

# SQL Query Review

## When to Use

- Analyst-generated query before production run
- Slow query optimization request
- Preventing accidental full table scans or PII exposure

## Procedure

### Step 1: Correctness

- Verify joins preserve intended grain
- Check NULL handling and duplicate row risk
- Validate filters match business definition

### Step 2: Performance

- EXPLAIN plan review for large tables
- Push filters early; avoid SELECT *
- Consider materialized views or pre-aggregation

### Step 3: Safety

- Read-only role for analytics
- LIMIT on exploratory queries
- No PII columns unless authorized

### Step 4: Documentation

- Comment non-obvious business logic
- Save canonical query to repo or dbt
- Link to **kpi-definition** if metric query

## Output

Reviewed query in repo or `doc/analytics/queries/<name>.sql`.
