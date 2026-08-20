# Metrics Interpretation

Reference for interpreting `ab-test evaluate` and `ab-test metrics` output.

---

## run_outcome

The `evaluate` command reports a `run_outcome` for each version before
printing per-metric scores:

| Outcome | Meaning |
|---|---|
| `COMPLETED` | Agent produced output files within the time limit |
| `TIMEOUT` | Run hit the `--timeout` threshold (forcibly killed) |
| `FAILED` | No output files found and run did not timeout (likely crash or context exhaustion) |

When a run is `FAILED` or `TIMEOUT` with no output, all metrics will be zero.
This is a valid data point (production failure rate). Report it; do not discard.

---

## Timeout Detection

The `compare` command reads the `timeout` field from each run's metadata. If
`duration_seconds >= timeout`, the run is marked `[TIMEOUT]` in the duration
table. The Run Outcomes section aggregates these counts.

If any version has >50% failures or timeouts, the compare report recommends
aborting and investigating before drawing conclusions.

---

## "no files matched" vs "no output produced"

In the evaluate output, two situations produce zero-value metrics:

1. **`run_outcome = FAILED [NO OUTPUT]`**: The agent produced nothing at all.
   All metrics are zero because there are no files to scan. This means the run
   itself failed (timeout, crash, rate limit).

2. **Metric `= 0 (no files matched)`**: Files matching the `target` glob do not
   exist, but other output may exist. This typically means the manifest's target
   pattern is too narrow or the agent wrote to an unexpected path. Check the
   `status` output for actual file counts.

---

## L0 Performance Metrics

The `metrics` command extracts operational performance data from session logs.
Key metrics and their interpretation:

| Metric | Lower is better? | Notes |
|---|---|---|
| Total tool calls | Usually yes | Fewer calls means more efficient agent behavior |
| View (read) calls | Yes | Reduced reads indicate better caching or spec-index usage |
| Bash (shell) calls | Neutral | Depends on task; builds require shell calls |
| Create/Edit calls | Neutral | Should match expected output artifact count |
| Skill invocations | Neutral | Skill loading adds context but enables better output |
| Subagent calls | Neutral | Rubber-duck calls improve quality but cost time |
| Duration (s) | Yes | Wall-clock time for the full agent session |
| Tokens in | Yes | Lower input tokens means less context consumption |
| Tokens out | Neutral | Depends on output volume requirements |
| Tokens cached | Yes (higher) | Higher cache ratio means better context reuse |

When interpreting deltas:
- A negative delta on "Total tool calls" or "View calls" indicates improved efficiency
- Token reduction without quality loss is a strong positive signal
- Duration reduction validates that efficiency gains are real (not just fewer outputs)
