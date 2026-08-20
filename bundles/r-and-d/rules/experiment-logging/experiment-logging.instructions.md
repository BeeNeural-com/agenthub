# Experiment Logging Standards

Apply when running spikes, benchmarks, or lab experiments.

## Required log entries

Each experiment must record:

| Field | Example |
|-------|---------|
| Experiment ID | exp-20260820-01 |
| Hypothesis | If X then Y |
| Date / time | ISO 8601 |
| Operator | Name or agent |
| Environment | HW, OS, SW versions |
| Configuration | Config files, parameters |
| Raw data location | Path or attachment |
| Outcome | pass / fail / inconclusive |
| Anomalies | Unexpected events |

## Storage

- Raw data: `doc/experiments/<experiment-id>/`
- Summary: link from spike charter or research report

## Integrity

- Do not edit raw data after collection — append corrections as notes
- Timestamp all log entries
- If experiment is repeated, create new ID; reference prior run

## Retention

Keep experiment logs for the lifetime of the associated research decision or requirement trace.
