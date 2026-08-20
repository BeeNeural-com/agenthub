---
description: Rules for the agent self-improvement protocol that triggers when an agent detects a reusable pattern or correctable workflow gap during execution
applyTo: "**/*.agent.md"
---

# Agent Self-Improvement Protocol

This protocol applies to every agent file in `.github/agents/`. Follow it at the end of every session in which you identify a systematic correction, new pattern, or reusable example.

---

## Trigger → Action

| Trigger | Action |
|---|---|
| User corrects a workflow step, rule, or format | Update **this agent file** to fix the root cause |
| Correction reveals a gap in format/syntax conventions | Update the relevant **`.github/instructions/*.instructions.md`** |
| New reusable pattern, pitfall, or example discovered | Create or update **`.github/skills/<topic>/SKILL.md`** |
| Component worked on has no project documentation yet | Propose creating `doc/<component>/index.md` and linked concept docs |
| Particularly good artifact produced (example, template) | Add it to the relevant skill's **`examples/`** directory |
| New pitfall confirmed during work | Add it to `## Pitfalls & Lessons Learned` in the relevant `.github/instructions/*.instructions.md` |

---

## Protocol

1. **Complete the main task first.** Never interrupt work-in-progress to self-improve.
2. After completing the task, identify improvements discovered during the session.
3. **Propose each improvement explicitly**: _"I noticed [X] — should I update [file] to capture this?"_
4. On user confirmation, apply with the edit tool immediately.
5. If the same mistake occurred more than once in a session, propose the fix **proactively**.

---

## Skill Creation Rules

- Front-matter: `name` (kebab-case) + `description` (one sentence, when to use it).
- Prefer concrete worked examples over abstract rules.
- File: `.github/skills/<skill-name>/SKILL.md`; examples in `.github/skills/<skill-name>/examples/`.
- **Check `.github/skills/README.md` before creating** — consult the index to avoid duplicating an existing skill. If no README exists yet, scan `.github/skills/` directly.
- All skills use a flat layout: direct children of `.github/skills/`. Do not create category or group subdirectories.
- **After creating or renaming a skill, update `.github/skills/README.md`** — add or update the row in the correct section with the file link, `name`, and `description`.

## Instruction File Creation Rules

- `applyTo` glob must be as narrow as possible — do not use `**/*` unless the rule genuinely applies everywhere.
- **After creating a new `.github/instructions/*.instructions.md`, update `.github/instructions/README.md`** — add a row to the correct section table with the file link, `applyTo` value, and a one-line purpose statement.

## Template Sync Rule

Whenever a **structural change** is made to any `*.agent.md` — new section, renamed section, new Mandatory Reads tier, new Plan-First gate step, new optional section pattern — update `.github/agents/_agent-template.md` to reflect the change.

Examples of changes that require a template sync:
- A new section (e.g., `## Coverage State Models`) is added to one or more agents.
- The three-tier Mandatory Reads format gains a new tier or changes its bold labels.
- A new optional section pattern becomes common enough to warrant a stub.
- The Plan-First gate steps change (e.g., a new step is added to Triage).

The template must remain the canonical starting point. If it drifts from the actual agent structure, new agents will be created with stale scaffolding.

---

## Constraints

- **Never silently modify files** without proposing to the user first.
- **Never delete existing rules** — only extend or correct them.
- **Never introduce project-specific data** (component names, req: IDs, file lists) into agent, instruction, or skill files. Those belong in `doc/`.
