---
name: monitoring-setup
description: >-
  Design metrics, logs, and traces with dashboards and alerts for a service. Use for new services or observability gaps.
tags: [devops-sre, monitoring]
---

# Monitoring Setup

## When to Use

- Service lacks dashboards or actionable alerts
- On-call receives noise without clear remediation
- Migrating to OpenTelemetry or new observability stack

## Procedure

### Step 1: Instrument

- Add RED/USE metrics for each endpoint or queue
- Structured JSON logs with trace_id correlation
- Distributed tracing on critical paths

### Step 2: Dashboard design

- Golden signals overview dashboard per service
- Drill-down views for dependencies
- SLO dashboard linked to error budget

### Step 3: Alert rules

- Every alert links to runbook section
- Test alerts in staging before production
- Set severity: page vs ticket vs log-only

### Step 4: Validate

- Run failure injection to confirm alert fires
- Review cardinality and cost of high-cardinality labels
- Document ownership and on-call rotation

## Output

Save as `doc/platform/monitoring-<service>.md`.
