---
description: Rules for traceability and coverage checker agents that audit bidirectional ID consistency and coverage ratios across V-Model levels
applyTo: "**/agents/**/*traceability-checker*,**/agents/**/*coverage-checker*"
---

# Traceability and Coverage Checker Rules

## Read-only declaration

Traceability checkers and coverage checkers **never modify any files**. They produce reports only. If an edit is required to fix a gap, the checker names the responsible writer agent and stops. The user decides whether to invoke that agent.

## Set-arithmetic template

All traceability checks follow this pattern. Apply it consistently for each direction being checked:

```
SOURCE_IDS  = all <tag> IDs in <source location>
TARGET_IDS  = all <tag> IDs in <target location>
MISSING     = SOURCE_IDS − TARGET_IDS    ← CRITICAL: source has no target entry
ORPHANED    = TARGET_IDS − SOURCE_IDS    ← CRITICAL: target has no source entry
```

Report every ID in MISSING and ORPHANED as a CRITICAL finding. Report the file and line number where the orphaned ID appears.

## Risk classification symbols

Use these symbols consistently across all findings tables and TODO lists:

**🔴 CRITICAL** — Traceability chain is broken; the ASPICE audit will fail; must be fixed before the next V-Model level can proceed.

**🟡 WARNING** — Traceability is present but incomplete or ambiguous; should be fixed; does not block the next level but will appear in the Quality Summarizer heat-map.

**🟢 INFO** — Minor annotation inconsistency; no chain breakage; fix at next opportunity.

## Report format

Every checker report opens with a summary block:

```
## <SWE.X> Traceability Report — <Component>

**<Tag A> IDs (source)**: <N>
**<Tag B> IDs (target)**: <N>
**Coverage**: <N>/<N> (<P>%)
**CRITICAL findings**: <N>
**WARNING findings**: <N>
```

Followed by CRITICAL findings, then WARNING findings, each as a flat list with file:line references.

## Self-improvement protocol

1. Complete the audit first.
2. Propose improvements explicitly before modifying any agent file.
3. Never delete existing checks — only extend or correct.
