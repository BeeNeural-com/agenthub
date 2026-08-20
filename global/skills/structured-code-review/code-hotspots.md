# Code Hotspot Analysis

Phase 4 of the structured-code-review workflow. Hotspots are the files that change most often
over the review period — they concentrate risk and are good candidates for close inspection.

## Compliance — read first

This analysis is **file-level only**. It must never become a per-person analysis:

- Do **not** add `--format=%aN`, `--format=%aE`, `--author`, or any author field.
- Do **not** run `git blame`, `git shortlog`, or `git log --author`.
- The command output, and `appendix/code-hotspots.md`, contain **file paths and change counts
  only** — no contributor names, emails, or per-person counts.

Reason: a reusable tool that profiles individuals' output is a behavioural-monitoring system —
it conflicts with GDPR data-minimization and, in a co-determined workplace, its use requires
works-council agreement. This skill analyses code, not people.

## Command

From the repository root, for the review period, list every changed file path (the empty
`--pretty=format:` emits no commit metadata and no author):

```
git log --since="«YYYY-MM-DD»" --name-only --pretty=format:
```

Then **tally the paths yourself**: count how many times each path appears, rank descending, and
take the top ~25. Do the counting in your own reasoning — this keeps the step cross-platform, as
it needs only `git` and works identically in PowerShell, CMD, and bash. Run it once per
repository in scope.

On a Unix-style shell only (macOS, Linux, Git Bash) the tally can optionally be piped instead:
`… --pretty=format: | grep -v '^$' | sort | uniq -c | sort -rn | head -25`.

## Interpreting the result

- Rank files by change count, highest first.
- Mark generated files (lock files, `*.d.ts`, build output, vendored code) and exclude them from
  conclusions — their churn is not a code-quality signal.
- A file marked for deletion or "temporary" that is also a top hotspot is itself a finding.
- Use the ranking to prioritise which files to inspect in Phase 5; cross-reference hotspots when
  choosing where to look for findings.

## Appendix format

Write `appendix/code-hotspots.md` with this structure:

```
# Code Hotspot Analysis

**Period:** «start date» – «end date»
**Method:** file-change frequency from `git log --name-only` (file-level only; no author data)

## «Repository name»

| Changes | File | Note |
|---|---|---|
| «n» | «path» | «e.g. generated — ignore / core module / marked for deletion» |
```
