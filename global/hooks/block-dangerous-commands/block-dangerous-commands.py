#!/usr/bin/env python3
"""PreToolUse security hook — block dangerous shell/cmd commands.

Reads a JSON hook payload from stdin. If the tool is a shell executor and
the command matches a known-dangerous pattern, emits a deny decision and
exits with code 2 (blocking the tool call).

Blocked categories:
  - sudo (privilege escalation)
  - rm targeting / or ~ (destructive filesystem wipe)
  - rm --no-preserve-root (bypass built-in safety guard)
  - mkfs (disk formatting)
  - dd writing to /dev/ block devices
  - Fork bombs
  - Overwriting critical /etc/ files
  - chmod -R on root-level paths
  - shred on block devices
  - curl/wget piped directly to a shell (remote code execution)
  - Windows: net user /add, net localgroup administrators
  - Windows: reg delete on HKLM
"""
import json
import re
import sys

# Tool names that execute shell commands
TERMINAL_TOOLS = {
    "run_in_terminal",
    "Bash",
    "bash",
    "shell",
    "execute_command",
    "execute_bash",
    "run_command",
    "computer",
}

# (raw_pattern, flags, human-readable reason)
_RULE_SPECS = [
    # Privilege escalation
    (r"\bsudo\b", re.IGNORECASE,
     "sudo (privilege escalation) is not permitted"),

    # rm targeting bare root or root contents
    (r"\brm\s+(?:\s*-\S+\s+)*(?:/\s*$|/\s*\*|/\s*;|/\s*\|)", re.IGNORECASE | re.MULTILINE,
     "rm targeting / or /* is not permitted"),

    # rm targeting home directory root
    (r"\brm\s+(?:\s*-\S+\s+)*~/?(?:\s*$|\s+)", re.IGNORECASE | re.MULTILINE,
     "rm targeting home directory root (~) is not permitted"),

    # Bypass rm's own safety guard
    (r"\brm\b.*--no-preserve-root", re.IGNORECASE,
     "rm --no-preserve-root bypasses the built-in safety guard and is not permitted"),

    # Disk / filesystem formatting
    (r"\bmkfs(?:\.\w+)?\b", re.IGNORECASE,
     "Filesystem formatting via mkfs is not permitted"),

    # dd writing to raw block devices
    (r"\bdd\b[^|&;\n]*\bof=/dev/", re.IGNORECASE,
     "Writing to raw block devices via dd is not permitted"),

    # Fork bombs  :(){:|:&};:
    (r":\s*\(\s*\)\s*\{[^}]*\|[^}]*:", re.DOTALL,
     "Fork bombs are not permitted"),

    # Overwriting critical system configuration files
    (r">\s*/etc/(?:passwd|shadow|sudoers|group|fstab|crontab)", re.IGNORECASE,
     "Overwriting critical system files (/etc/passwd, shadow, sudoers …) is not permitted"),

    # Recursive chmod on root-level paths
    (r"\bchmod\b[^|&;\n]*-[Rr]\b[^|&;\n]*/(?:\s|$)", re.IGNORECASE,
     "Recursive chmod on root-level paths is not permitted"),

    # Wiping block devices with shred
    (r"\bshred\b[^|&;\n]*/dev/", re.IGNORECASE,
     "Wiping block devices via shred is not permitted"),

    # Remote code execution: curl/wget piped to any shell
    (r"\b(?:curl|wget)\b[^|&;\n]*\|\s*(?:sudo\s+)?(?:ba|da|z|k|c|fi)?sh\b", re.IGNORECASE,
     "Piping a remote download directly to a shell (curl|bash, wget|sh) is not permitted"),

    # Windows: add user or grant admin
    (r"\bnet\s+(?:user\b[^|&;\n]*/add|localgroup\s+administrators)", re.IGNORECASE,
     "Adding users or granting administrator rights is not permitted"),

    # Windows: reg delete on HKLM
    (r"\breg\b\s+delete\s+HKLM", re.IGNORECASE,
     "Deleting HKLM registry keys is not permitted"),

    # Windows PowerShell: Remove-Item -Recurse on drive root
    (r"\bRemove-Item\b[^|&;\n]*-(?:Recurse|r)\b[^|&;\n]*(?:[A-Za-z]:\\\\|/\s*$)", re.IGNORECASE,
     "Recursive PowerShell Remove-Item on a drive root is not permitted"),
]

# Compile once at import time
RULES = [(re.compile(pat, flags), reason) for pat, flags, reason in _RULE_SPECS]


def extract_command(tool_input: dict) -> str:
    """Return the shell command string from the tool's input dict."""
    for key in ("command", "cmd", "input", "code", "script"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ""


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # unparseable input – allow through

    tool_name = hook_input.get("toolName", "")
    if tool_name not in TERMINAL_TOOLS:
        sys.exit(0)  # not a shell tool – nothing to check

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
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"[Security Hook] Blocked — {reason}\n"
                        f"Command: {command[:400]}"
                    ),
                }
            }
            print(json.dumps(payload))
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
