---
description: Runtime governance rules and pitfalls for all role agents; SIPOC chain enforcement and subagent delegation constraints
applyTo: ".github/agents/*.agent.md"
---

# Role Agent Instructions

## Purpose

Role agents act as job-function entry points that map a user's engineering role to the correct set of specialist agents. Each role agent applies a Plan-First gate — Triage, Plan, Confirm, Delegate — before invoking any specialist.

> **Creating a new agent?** See `.github/instructions/role-agent-creation.instructions.md` for required structure, section formats, SIPOC paragraph conventions, and Plan-First gate scaffolding.

---

## Rules

- **Task notation**: `T1`, `T2`, etc. in Plan sections means "Task 1", "Task 2" — sequential steps within a phase. This is a compact notation used by all role agents.
- No tables in SIPOC sections — bold-label paragraphs only, matching the use-case file format.
- The **Customers:** field of each role agent must name the downstream role(s) whose **Suppliers:** field names this role.
- Role agents are **read-only** with respect to workspace source files — all writing is delegated to specialist agents.
- Each role agent references only its own specialist layer; it must not reach across layers (e.g., a requirements engineer role must not invoke SWE.3 agents directly).
- Role agents must use the SIPOC chain: Consultant → Function Owner → Requirements Engineer → Software Architect → {Software Engineer, Integration Tester, Qualification Tester} → Auditor.
- Cross-cutting role (Auditor) lists `*all roles*` as Suppliers.
- **Scope restriction phrasing standard**: whenever a Triage step restricts access to a directory, the prohibition must name all five access tools explicitly: `read_file`, `grep_search`, `file_search`, `semantic_search`, and `list_dir`.

---

## Pitfalls & Lessons Learned

### Multi-Phase Agents Must Not Cascade

When an agent has multiple phases (e.g., specification then implementation), each phase ends at its defined exit point. Do not start the next phase automatically. With `compact_between_phases=true`: end the current phase with a carry-forward summary, prompt `/compact`, then begin the next phase.

### Todo List Must Be Initialized Before Any Execution Action

After the user approves the plan and triggers execution (e.g., "proceed"), the **very first action** must be initializing the todo list — not creating files, not calling tools, not reading context. The todo list makes progress visible and recoverable.

**Root cause of the anti-pattern**: The agent proceeds directly to file creation after approval, treating the todo list as optional or deferred. The user has to ask "where is your todo list?" before it is created. By then, multiple tasks have already been completed without tracking.

**Correct approach**: Step 1 of every Execute section initializes the todo list with all approved tasks marked `not-started`. Each task is marked `in-progress` immediately before starting it. It is marked `completed` immediately after finishing — before moving to the next task.

---

### All Access Tools Are Prohibited for Out-of-Scope Directories

When a Triage step or Critical Rule says "Do not read [directory X]", the prohibition covers **all access tools**: `read_file`, `grep_search`, `file_search`, `semantic_search`, and `list_dir`. The term "read" in any scope restriction means "do not retrieve content from or browse that path by any means."

Agent authors must phrase prohibitions explicitly: use **"Do not read, search, grep, or browse"** rather than "Do not read".

**Root cause of the anti-pattern (content tools)**: An agent receives a broad request and reaches for `grep_search` targeting an out-of-scope directory to gather more context, rationalizing it as "searching" (not "reading"). The scope boundary is bypassed despite being explicitly stated.

**Root cause of the anti-pattern (directory browsing)**: An agent uses `list_dir` on an out-of-scope directory, rationalizing that it is only "browsing structure, not reading content". Even directory listings reveal project-specific names (file names, component names, requirement topic names) and therefore constitute a scope violation. File names seen in a `list_dir` result must not be used to infer or reconstruct content that the triage scope prohibits.

**Correct approach**: Derive scope and IDs only from the documents the Triage step explicitly permits. If the permitted documents do not contain enough information, ask the user — do not silently expand scope.

---

### Agent Rules Must Not Duplicate Instruction or Skill Content

When a rule in an agent file restates logic already fully covered by an instruction file or skill, the agent and the source diverge silently whenever the source is updated. The fix: reduce the agent rule to a one-line pointer, e.g. `"See testability-design.instructions.md."`. All decision logic stays in the instruction or skill file.

---

### Dangling Named-Section References Are a Maintenance Hazard

An agent rule or workflow step that names a specific table, section, or file (e.g., "apply the **Component Classification** table") must reference an artefact that actually exists at the stated location. A dangling reference is invisible until an agent acts on it and fails silently or produces wrong output. Before saving any agent file edit that adds or retains a named cross-reference, verify the referenced artefact exists. If it does not, either remove the qualifier or create the artefact.

---

### Commit Messages Must Follow `.gitmessage`

Before composing a commit message, read `.gitmessage` at the repository root. Extract the ticket ID from the current branch name. Keep the subject to one imperative phrase. Use bullets only for distinct logical changes; omit them for single-change commits.
