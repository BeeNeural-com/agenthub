---
name: git-guard
description: >-
  PreToolUse hook that gates destructive or history-rewriting git operations
  behind an explicit user confirmation prompt — git push, force-push,
  reset --hard, rebase, clean, force branch delete, and orphan checkout.
tags:
  - git
  - PreToolUse
  - ask
  - confirmation
  - history-safety
---

# git-guard

## Overview

This hook intercepts agent shell calls that contain git commands capable of
destroying local work or rewriting shared remote history. Unlike a hard deny,
it returns an **`ask` decision** — the agent pauses, surfaces the command and
the reason to the user, and only proceeds if the user explicitly approves. This
keeps the agent productive while eliminating silent irreversible operations.

## Use Cases

| Scenario | Why this hook helps |
|----------|---------------------|
| Agent runs `git push` after a refactor | User sees exactly which remote/branch will be updated before it happens |
| Agent rewrites history with `git rebase -i` | Confirmation prompt prevents silently altering commits others may depend on |
| Agent cleans working tree with `git clean -fd` | Untracked files are precious; user decides before they're gone |
| Agent force-pushes a squashed branch | `--force` is flagged with a stronger warning than a normal push |
| Agent deletes a stale branch with `git branch -D` | Force-delete is irreversible; user confirms branch is truly unwanted |
| Agent creates an orphan branch as a deployment trick | Orphan checkout erases history on that branch — user confirms intent |

## How It Works

### 1. Event binding (`hooks.json`)

Registered under `PreToolUse`. The payload piped to stdin on every shell tool
call looks like:

```json
{
  "toolName": "run_in_terminal",
  "toolInput": { "command": "git push --force origin main" }
}
```

### 2. Tool filter (`git-guard.py` → `TERMINAL_TOOLS`)

Only shell-executing tools are inspected. Non-shell tools (search, file reads,
etc.) are allowed through immediately with exit `0`.

### 3. Command extraction

The script checks `command`, `cmd`, `input`, `code`, `script` in order and
uses the first non-empty string as the subject for pattern matching.

### 4. Ordered rule matching (`_RULE_SPECS`)

Rules are `(regex_pattern, flags, reason)` tuples evaluated in order — the
**first match wins** and exits early. More specific rules are placed before
broader ones to surface the most precise reason:

| Priority | Pattern | Reason surfaced |
|----------|---------|----------------|
| 1 (highest) | `git push.*--force\|-f` | Force-push can overwrite remote history — irreversible |
| 2 | `git push` (any) | Publishes commits to remote — please confirm |
| 3 | `git reset.*--hard` | Discards uncommitted changes permanently |
| 4 | `git clean.*-\S*f` | Removes untracked files permanently |
| 5 | `git rebase` | Rewrites commit history — confirm intent |
| 6 | `git branch.*-[A-Z]*D` | Force-deletes a branch — cannot be undone |
| 7 | `git checkout.*--orphan` | Creates unrelated history graph — confirm intent |

### 5. Decision output

On a match the script writes a `permissionDecision: ask` JSON block to stdout
and exits `0`. The agent pauses and presents the command + reason to the user:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "[Git Guard] git push --force can overwrite remote history and is irreversible\nCommand: git push --force origin main"
  }
}
```

If no rule matches, the script exits `0` with no output — the tool call
proceeds silently.

> **Why exit `0` for `ask`?** Exit code `2` means *block*. The `ask` decision
> is communicated entirely through the JSON payload, not the exit code. The
> agent reads the `permissionDecision` field and surfaces the confirmation UI.

### Execution flow

```
Agent proposes git command
        │
        ▼
  hooks.json (PreToolUse)
        │
        ▼
  git-guard.py
  ┌───────────────────────────────────────────────┐
  │ 1. Parse stdin JSON                           │
  │ 2. Is toolName in TERMINAL_TOOLS?  ─No──────► │ exit 0 (allow)
  │ 3. Extract command string                     │
  │ 4. Match _RULE_SPECS in priority order        │
  │    First match → ask JSON + exit 0 (gate)     │
  │    No match    → exit 0 (allow silently)      │
  └───────────────────────────────────────────────┘
        │
        ▼ (on match)
  Agent pauses → user sees command + reason
        │
   ┌────┴────┐
 Approve   Cancel
   │           │
  Tool      Aborted
  runs
```

## Files

| File | Purpose |
|------|---------|
| `hooks.json` | Binds script to `PreToolUse`, sets 5 s timeout, platform commands |
| `git-guard.py` | Detection script — ordered regex rule engine, emits `ask` |

## Testing

```sh
# Should gate — exit 0 + ask JSON (force push)
echo '{"toolName":"run_in_terminal","toolInput":{"command":"git push --force origin main"}}' \
  | python3 .github/hooks/git-guard/git-guard.py

# Should gate — exit 0 + ask JSON (normal push)
echo '{"toolName":"run_in_terminal","toolInput":{"command":"git push origin feat/my-branch"}}' \
  | python3 .github/hooks/git-guard/git-guard.py

# Should allow silently — exit 0, no output
echo '{"toolName":"run_in_terminal","toolInput":{"command":"git status"}}' \
  | python3 .github/hooks/git-guard/git-guard.py
```

## Notes

- `ask` does **not** hard-block; an informed user can still approve the command.
- Rules are ordered: `--force` is matched before the generic `git push` rule so
  the more severe warning is shown.
- To gate additional commands, append to `_RULE_SPECS` in `git-guard.py`.
  Place more specific patterns before broader ones.
