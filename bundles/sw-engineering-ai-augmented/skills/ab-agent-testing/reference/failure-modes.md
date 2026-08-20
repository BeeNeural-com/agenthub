# Failure Modes

Troubleshooting reference for common A/B test failures.

| Symptom | Cause | Action |
|---|---|---|
| Agent hangs | No timeout set | Kill after 20 min; report as failed run |
| Identical outputs | Topic too simple | Re-run with complex topic |
| Clone not found | /tmp cleaned | Re-run `ab-test prepare` |
| Max clones reached | Old runs not cleaned | `ab-test gc --older-than 24h` |
| Judge disagrees across orderings | Position bias | Report "inconclusive" |
| Agent produces no output | Context exhaustion or rate limit | Report as failed run; check if skills consume too much context |
| Existing specs still in clone | Cleanup bug | Verify `find -path` patterns match; check prepare log for "deleted N file(s)" |
| `git checkout --detach` fails | Branch name not in local clone | Refs are resolved to SHAs before checkout (handled by prepare) |
