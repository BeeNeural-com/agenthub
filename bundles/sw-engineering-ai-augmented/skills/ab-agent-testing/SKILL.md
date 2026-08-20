---
name: ab-agent-testing
description: "A/B testing methodology for comparing role agent versions. Use when evaluating agent definition changes, instruction rewrites, or skill additions by running controlled side-by-side tests with isolated output directories and statistical comparison."
---

# A/B Agent Testing Skill

Orchestrate controlled A/B tests comparing two versions of a role agent.
Prepare isolated clones, run both versions with identical inputs, collect
metrics, and report which version is better.

---

## Overview

This skill guides you through the full A/B test lifecycle for any role agent
in the ecosystem (testers, architects, requirements engineers, designers,
implementers). You will use the `ab-test` CLI tool at `tools/ab-test/ab-test`
to prepare isolated git worktrees, run agents in parallel, collect structural
(L1) and performance (L0) metrics, and produce a statistical comparison.

Each agent has a manifest at `tools/ab-test/manifests/<agent>.yaml` that
defines its cleanup patterns, output metrics, and evaluation rubric. The
framework handles agent-specific differences through these manifests.

---

## Reference (Load on Demand)

Load these files with `view` only when the specific situation arises:

| File | Load when |
|---|---|
| `reference/task-prompts.md` | Selecting or customizing the task prompt |
| `reference/tester-implementation-phase.md` | Running tester Phase 2 (spec to code) |
| `reference/metrics-interpretation.md` | Interpreting `evaluate` or `metrics` output |
| `reference/manifest-system.md` | Adding a new agent to the framework |
| `reference/failure-modes.md` | A run produces unexpected results |

---

## User Intake (Before Starting)

Before executing any test, gather requirements from the user. Use `ask_user`
to collect this information in a structured form:

### Required Information

1. **Which agent changed?**
   Detect from overlay files or branch diff, or ask directly.
   Supported agents: Integration Tester, Qualification Tester, Requirements
   Engineer, Software Architect, Software Designer, Software Implementer.

2. **What is the baseline reference?**
   Typically `develop` or `main`. Can be any git ref (branch, tag, SHA).
   For uncommitted changes, the baseline is the current branch and the
   improved version uses `--overlay` with the changed files.

3. **How many runs (N)?**
   - N=1: smoke test (verify framework works, fast iteration)
   - N=3: directional indication (is there a visible difference?)
   - N=5: minimum for statistical significance (Wilcoxon test)
   - N=10: detect small differences (0.5-point rubric delta)

4. **What is the hypothesis?**
   What should improve? Examples: "fewer view calls", "better traceability
   coverage", "faster completion", "higher structural compliance". This
   determines which metrics to highlight in the report.

5. **What evaluation scope?**
   - L0 only: performance metrics (tool calls, tokens, duration)
   - L0+L1: add structural metrics (pattern counts, trace links)
   - L0+L1+L2: add LLM-as-Judge pairwise comparison (requires N>=3)

### Propose and Confirm

After gathering answers, propose the full test configuration:

```
Test Plan:
  Agent:     <agent-name>
  Baseline:  <ref>
  Improved:  <ref or --overlay files>
  Runs:      N=<n>
  Timeout:   1200s
  Scope:     L0+L1 (or L0+L1+L2 if N>=3)
  Hypothesis: <what should improve>
```

Wait for explicit user confirmation before proceeding to Step 0.

---

## Lifecycle and Usage Pattern

### Step 0: Pre-flight

```bash
./tools/ab-test/ab-test gc --older-than 24h
```

The `prepare` command auto-GCs when clone count reaches 8+. Explicit GC is
only needed to reclaim disk space proactively.

### Step 1: Prepare

```bash
RUN_DIR=$(./tools/ab-test/ab-test prepare "<agent-name>" --refs <baseline-ref> <improved-ref> \
  | grep "Run dir:" | awk '{print $NF}')
```

For uncommitted changes, use `--overlay`:

```bash
RUN_DIR=$(./tools/ab-test/ab-test prepare "<agent-name>" \
  --overlay .github/agents/<agent>.agent.md \
  | grep "Run dir:" | awk '{print $NF}')
```

Always capture `RUN_DIR`; all subsequent commands use it.

**Verify cleanup worked** (critical for test validity):

The prepare step removes all files matching the manifest's `cleanup.delete`
patterns while preserving files listed in `cleanup.preserve`. Verify that only
input files remain in the agent's output directories:

```bash
./tools/ab-test/ab-test status "$RUN_DIR"
```

If existing output files remain, the test is invalid. The agents would read them
and get biased instead of creating from scratch.

### Step 2: Run Agents

Run both versions in parallel:

```bash
./tools/ab-test/ab-test run "$RUN_DIR" baseline --exec --runs <N> --timeout 1200 \
  > "$RUN_DIR/results/baseline-stdout.log" 2>&1 &
PID_B=$!

./tools/ab-test/ab-test run "$RUN_DIR" improved --exec --runs <N> --timeout 1200 \
  > "$RUN_DIR/results/improved-stdout.log" 2>&1 &
PID_I=$!

wait $PID_B $PID_I
```

**Critical rules:**
- Both versions MUST use the same model (pinned in `ab-test run` defaults)
- Override with `--model <m>` if needed (must be identical for both)
- `--timeout 1200` (20 min) is standard; agents with self-review loops need more

**Wait strategy:** A single run takes 3-12 minutes. Use `initial_wait: 30` with
sync mode, then `read_bash` with 180s delay to poll. Check the file system for
progress instead of relying on stdout.

### Step 2b: Monitor Progress

```bash
./tools/ab-test/ab-test status "$RUN_DIR"
```

Shows run progress, output counts, and timeout detection.

### Step 2c: Verify Output Exists

After runs complete, confirm both agents created artifacts.

For doc-producing agents (architects, requirements engineers, testers Phase 1):
```bash
find "$(readlink -f "$RUN_DIR/baseline/worktree")/doc/" -name "*.md" \
  ! -name "_briefing.md" ! -name "index.md" -newer "$RUN_DIR/baseline/worktree/.git/HEAD" -ls
```

For src-producing agents (designers, implementers):
```bash
find "$(readlink -f "$RUN_DIR/baseline/worktree")/src/" -name "*.h" -o -name "*.cpp" \
  -newer "$RUN_DIR/baseline/worktree/.git/HEAD" -ls
```

If one version produced no output, report it as a valid data point (production
failure due to context exhaustion, rate limiting, or analysis loops).

### Step 3: Evaluate

```bash
./tools/ab-test/ab-test evaluate "$RUN_DIR"
```

Collects L1 structural metrics from agent output and L0 performance metrics
from session logs. The evaluate command reads the manifest to know which
patterns and files to measure for the specific agent.

For machine-readable L0 output: `ab-test metrics "$RUN_DIR" --format json`

For interpreting results: `view reference/metrics-interpretation.md`

### Step 4: Compare and Judge

If N>=3 runs were performed:

```bash
./tools/ab-test/ab-test compare "$RUN_DIR" --judge --blind
```

Produces Wilcoxon signed-rank test, LLM-as-Judge pairwise comparison with
blinded labels, and a comparison report at `$RUN_DIR/results/comparison-report.md`.

### Step 5: Report

Present to the user, highlighting the hypothesis metric:
1. L0 performance metrics (tool calls, tokens, duration)
2. L1 metrics summary (structural checks, per-agent manifest metrics)
3. Statistical significance (if N>=5: p<0.01, p<0.05, p<0.10, or n.s.)
4. Judge verdict per dimension (if L2 scope was selected)
5. Recommendation: **ship** / **revert** / **inconclusive**

If N=1, explicitly state: "Smoke test only. No statistical conclusions possible.
Run N>=5 for significance testing."

---

## Best Practices and Anti-patterns

### Orchestrating Agent Rules

1. **Never modify the clones yourself.** Only spawned copilot instances write to clones.
2. **Pin the model.** Both versions MUST use the same `--model` value.
3. **Identical task prompts.** Any prompt difference invalidates the comparison.
4. **Report all runs.** Never cherry-pick. If one run failed, report it.
5. **Respect the N threshold.** Do not claim "improved is better" from N=1.
6. **Clean up.** Run `ab-test gc` if clones accumulate.
7. **Verify cleanup.** After prepare, confirm output artifacts are deleted.
8. **Check file system, not stdout.** The copilot CLI buffers output.

### Test Validity

The test is only valid when both conditions hold:

1. **All agent OUTPUT artifacts are deleted before the run.** The prepare step
   uses cleanup patterns from the manifest to remove the agent's output files.

2. **Both clones have identical INPUT documents.** The normalize step syncs
   `doc/` and `src/` from the improved clone to baseline, ensuring both agents
   read the same upstream inputs.

### Anti-patterns

- Claiming statistical significance from N<5
- Using different models or prompts between versions
- Discarding failed runs (they are valid data points)
- Using simple topics (produces identical output, masks differences)
- Modifying clones directly instead of letting agents work
- Skipping the User Intake step (leads to wasted runs)

---

## Domain Glossary

| Term | Definition |
|---|---|
| Clone | Isolated git worktree for one agent version |
| Baseline | The control version (e.g., develop branch) |
| Improved | The treatment version (e.g., feature branch or HEAD with overlay) |
| Manifest | YAML file defining cleanup patterns, metrics, and rubric per agent |
| Run outcome | COMPLETED, TIMEOUT, or FAILED |
| L0 | Performance tier: tool calls, tokens, duration |
| L1 | Structural tier: pattern counts, trace links, section presence |
| L2 | Quality tier: LLM-as-Judge pairwise comparison |
| L3 | Human tier: manual rubric scoring |
| N | Number of runs per version (N>=5 for statistical claims) |
| Wilcoxon | Non-parametric paired test for statistical significance |
| Overlay | Uncommitted file changes applied to the improved clone |
| Doc-producing agent | Agent whose output is .md under doc/ (architect, req eng, testers P1) |
| Src-producing agent | Agent whose output is .h/.cpp under src/ or tests/ (designer, implementer) |
