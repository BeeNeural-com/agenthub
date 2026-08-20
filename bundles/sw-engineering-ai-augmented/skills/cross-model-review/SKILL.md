---
name: cross-model-review
description: "Use this skill at defined workflow milestones to invoke an independent reviewer from a different model family, avoiding confirmation bias from the same reasoning context that produced the artifact. Triggers: any agent reaching a review checkpoint. Supports three execution branches: rubber-duck sub-agent (Copilot CLI), general sub-agent (API/orchestrator), and self-critique fallback. Role-specific review templates live in templates/ alongside this file."
---

# Cross-Model Review Protocol

Agents invoke an independent reviewer at defined workflow milestones.
The reviewer uses a different model family to avoid confirmation bias
from the same reasoning context that produced the artifact.

---

## Invariants

1. **Independence**: the reviewer must be a different model family than the producing agent.
2. **Deterministic input**: the review prompt is built from a versioned template plus the actual artifact. Same template + same artifact = identical prompt.
3. **Criteria are not owned here**: review criteria live in the normative instruction files for each role. Templates reference them; they do not redefine them.
4. **Auditability**: every review records its mode (independent, independent-subagent, or self-critique), template version, and per-criterion verdict.

---

## Invocation contract

The contract is a strict priority ladder. Execute the **first** branch whose
precondition holds. Never skip to a lower branch when a higher one is available.

---

### Branch 1 — Rubber-duck sub-agent (preferred, Copilot CLI users)

**Precondition:** the `task` tool is available AND supports `agent_type: rubber-duck`.

**Action:**

Invoke `task`:
- `agent_type`: `rubber-duck`
- `model`: a different model family than the producing agent
  - Producer is Claude → use `gpt-5.4`
  - Producer is GPT → use `claude-sonnet-4-6`
- `prompt`: the fully filled template (all placeholders replaced — no raw `{{…}}` tokens)

---

### Branch 2 — General sub-agent (all users without rubber-duck)

**Precondition:** the `task` tool is NOT available or does NOT support
`agent_type: rubber-duck`, AND the environment supports spawning a sub-agent
via any other mechanism (e.g. a direct API call to a different model, a
secondary agent invocation in the orchestrator).

**Action:**

Spawn a sub-agent with:
- A system prompt that frames it exclusively as an independent reviewer with
  no knowledge of the producing agent's reasoning context
- The fully filled template as the user message
- A different model family than the producing agent (same model mapping as Branch 1)

Mark the critique block header:

```markdown
> Mode: independent-subagent (model: <model-used>)
```

---

### Branch 3 — Self-critique (absolute fallback)

**Precondition:** neither Branch 1 nor Branch 2 is executable in the current
environment.

**Action:**

Apply the template criteria to your own output. This branch MUST be marked
explicitly so reviewers can flag it during audits:

```markdown
> Mode: self-critique (no independent agent available — audit required)
```

A self-critique review does NOT satisfy the independence invariant. Flag it
in the artifact and raise it as a process gap to the pipeline owner.

---

### Steps common to all branches

**Step A: Build the prompt.**
Fill the role's template from `templates/`. Replace every placeholder with
actual content. Do not pass a template with raw `{{…}}` tokens.

**Step B: Record findings.**
Write findings into the artifact using the output schema (see below).

**Step C: Address FAIL findings.**
- Fixable locally → fix the artifact, re-assess the criterion.
- Requires upstream changes or environment constraints → mark BLOCKED with evidence.
- Proceed only when all criteria are PASS or BLOCKED.

BLOCKED applies only to upstream or environment constraints. Local defects
must be fixed, not marked BLOCKED.

**Step D: Summarize findings.**
Provide the user with a summary of findings and required actions.

---

## Output schema

Place the `## Critique` section at the location defined by the workflow skill
(typically after all content, before any Coverage Table).

```markdown
## Critique (<criteria-range>)

> Mode: independent (model: <model-used>) | independent-subagent (model: <model-used>) | self-critique (no independent agent available — audit required)
> Template: <template-file-path> @ <git-short-hash>

| ID | Verdict | Evidence |
|---|---|---|
| <id> | PASS | <one-sentence evidence> |
| <id> | FAIL | <what must change> |

### Findings requiring action

- **<id>**: <description of required change and resolution>

### Blocked findings

- **<id>**: <upstream or environment constraint preventing resolution>
```

---

## Templates

Role-specific and phase-specific prompt templates live in `templates/` alongside
this file. The producing agent selects the template that matches its role and
current workflow phase.

| Template | Role | Phase |
|---|---|---|
| `templates/prompt-requirements.md`  | Requirements Engineer | Review |
| `templates/prompt-architecture.md`  | Architect             | Review |
| `templates/integration-phase1.md`   | Integration Tester    | Phase 1 (Specification)  |
| `templates/integration-phase2.md`   | Integration Tester    | Phase 2 (Implementation) |
| `templates/qualification-phase1.md` | Qualification Tester  | Phase 1 (Specification)  |
| `templates/qualification-phase2.md` | Qualification Tester  | Phase 2 (Implementation) |

To add review support for another role agent, create a new template file following
the same pattern: system preamble, criteria reference, upstream context placeholder,
artifact placeholder.

---

## Anti-patterns

- Do not duplicate criteria text in templates; reference the instruction file section instead.
- Do not skip the review even if confident the artifact is correct.
- Do not mark local defects as BLOCKED.
- Do not invoke the review on partial work; wait until the milestone is complete.
- Do not use the same model family for the reviewer (defeats independence).
- Do not omit upstream context excerpts from the filled template.
- Do not treat Branch 3 (self-critique) as an acceptable steady state; surface it as a process gap.
- Do not pass a template containing raw `{{…}}` placeholder tokens to the reviewer.
