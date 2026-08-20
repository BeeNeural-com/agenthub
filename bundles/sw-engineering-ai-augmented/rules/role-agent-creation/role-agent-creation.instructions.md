---
description: Structural rules and format conventions for creating a new role agent file from the template
applyTo: ".github/agents/_agent-template.md"
---

# Role Agent Creation Instructions

These conventions apply when creating a new role agent from `.github/agents/_agent-template.md`. They define the required structure, section formats, and content rules that every new agent must satisfy.

---

## Required Structure

Use `.github/agents/_agent-template.md` as the starting point for any new agent.

Every role agent must contain these sections in this exact order:

1. **Mandatory Reads** — three-tier load list; immediately after the opening introductory paragraph, before Role SIPOC
2. **Role SIPOC** — one paragraph per SIPOC element
3. **Scope** — what this role owns; what it explicitly does not own
4. **Plan-First Gate** — four subsections: Triage, Plan, Confirm, Execute

---

## Mandatory Reads Format

The `## Mandatory Reads` section uses exactly three bold-label subsections:

**Always load — before any other action:**
Load at the very start of every session, before reading the user's request.
Required minimum for every agent: `role-agent.instructions.md` and `agent-self-improvement.instructions.md`.
Add any instruction that applies to every artifact this role produces (e.g., `sca-compliance.instructions.md` for agents that write code or tests).

**Load at Triage — do not skip:**
Load during the Triage step, before the Plan step begins. The label "do not skip" is mandatory and must appear verbatim.
Required in every agent: `.github/skills/README.md` and `.github/instructions/README.md`. Always both. Never omit either.

**Load per stage:** *(or **Load per task:** for non-staged agents)*
Load immediately before the specific stage or task they govern. List file → purpose on one line each.

---

## SIPOC Paragraph Format

Use bold-label paragraphs. No tables. No bullet lists for SIPOC elements.

**Suppliers:** Who or what provides the inputs to this role — named roles, users, or upstream artifacts.

**Inputs:** Artifacts, requests, or context this role receives to begin its work.

**Process:** What this role does — one sentence per major activity. Write in active voice.

**Outputs:** Artifacts or decisions this role produces when the work is complete.

**Customers:** Downstream role(s) or stakeholders who consume the outputs of this role. This field must name the same role(s) whose **Suppliers:** field names this role, ensuring the chain is verifiable.

---

## Plan-First Gate Structure

Each section of the gate opens with its own compact SIPOC paragraph block, followed by a numbered **Steps** list.

### Triage

SIPOC for the triage activity.

**Steps:**
1. Read the user's request.
2. Identify the request type: new work, change, review, or demo.
3. Determine which specialist agents are relevant to this role.
4. Identify hard prerequisites — if any upstream role has not completed its work, stop and inform the user.

### Plan

SIPOC for the planning activity.

**Steps:**
1. List the specialist agents to invoke in planned order.
2. For each agent, state: what input it needs and what output is expected.
3. Flag any prerequisite that must be satisfied before a step can run.
4. Present the plan as a numbered task list (T1, T2, … Tn).

### Confirm

SIPOC for the confirmation activity.

**Steps:**
1. Present the task plan to the user as a numbered list.
2. Wait for explicit approval before proceeding.
3. If the user modifies the plan, revise the list and re-present.
4. Do not begin delegation until the user confirms.

### Execute

SIPOC for the execution activity.

**Steps:**
1. Initialize the todo list with all tasks from the approved plan, each marked `not-started`. This must be the first action in Execute, before any file creation or tool calls. Before starting each task, mark it `in-progress`. Immediately after completing it, mark it `completed`.
2. Execute each task in the planned order, applying the relevant skill and instruction files.
3. Pass outputs from each task as context into the next.
4. Report completion to the user with a summary of outputs produced.
