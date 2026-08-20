#!/usr/bin/env python3
"""PreToolUse hook — require confirmation before destructive git operations.

Destructive operations gated:
  - git push       (any variant: --force, -u, origin ..., etc.)
  - git push --force / -f  (flagged even more strongly)
  - git reset --hard
  - git clean -f / -fd / -fdx
  - git rebase    (any — rebasing shared history is risky)
  - git checkout --orphan (destroys entire history on that branch)
  - git branch -D (force-delete branch)

For all of these the hook returns permissionDecision = "ask", which makes the
agent pause and present the command to the user for explicit approval before
proceeding.
"""
import json
import re
import sys

TERMINAL_TOOLS = {
    "run_in_terminal",
    "Bash",
    "bash",
    "shell",
    "execute_command",
    "execute_bash",
    "run_command",
}

# (pattern, flags, reason shown to user)
_RULE_SPECS = [
    # git push --force / -f — highest risk
    (
        r"\bgit\b[^|&;\n]*\bpush\b[^|&;\n]*(?:--force|-f)\b",
        re.IGNORECASE,
        "git push --force can overwrite remote history and is irreversible",
    ),
    # any git push (including --force covered above, matched first)
    (
        r"\bgit\b[^|&;\n]*\bpush\b",
        re.IGNORECASE,
        "git push will publish commits to the remote — please confirm",
    ),
    # git reset --hard
    (
        r"\bgit\b[^|&;\n]*\breset\b[^|&;\n]*--hard\b",
        re.IGNORECASE,
        "git reset --hard discards uncommitted changes permanently",
    ),
    # git clean (any -f variant)
    (
        r"\bgit\b[^|&;\n]*\bclean\b[^|&;\n]*-\S*f",
        re.IGNORECASE,
        "git clean -f removes untracked files permanently",
    ),
    # git rebase
    (
        r"\bgit\b[^|&;\n]*\brebase\b",
        re.IGNORECASE,
        "git rebase rewrites commit history — confirm intent",
    ),
    # git branch -D (force delete)
    (
        r"\bgit\b[^|&;\n]*\bbranch\b[^|&;\n]*-[A-Za-z]*D",
        re.IGNORECASE,
        "git branch -D force-deletes a branch and cannot be undone",
    ),
    # git checkout --orphan
    (
        r"\bgit\b[^|&;\n]*\bcheckout\b[^|&;\n]*--orphan\b",
        re.IGNORECASE,
        "git checkout --orphan creates an unrelated history — confirm intent",
    ),
]

RULES = [(re.compile(pat, flags), reason) for pat, flags, reason in _RULE_SPECS]


def extract_command(tool_input: dict) -> str:
    for key in ("command", "cmd", "input", "code", "script"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ""


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = hook_input.get("toolName", "")
    if tool_name not in TERMINAL_TOOLS:
        sys.exit(0)

    tool_input = hook_input.get("toolInput") or {}
    if not isinstance(tool_input, dict):
        sys.exit(0)

    command = extract_command(tool_input)
    if not command:
        sys.exit(0)

    for pattern, reason in RULES:
        if pattern.search(command):
            payload = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"[Git Guard] {reason}\n"
                        f"Command: {command[:400]}"
                    ),
                }
            }
            print(json.dumps(payload))
            sys.exit(0)  # exit 0 — "ask" surfaces as a confirmation prompt, not a hard block

    sys.exit(0)


if __name__ == "__main__":
    main()
