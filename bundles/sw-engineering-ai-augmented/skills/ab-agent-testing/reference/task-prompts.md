# Task Prompt Selection

The canonical source for task prompts is:
`tools/ab-test/prompts/task-definitions.md`

That file contains per-agent, per-phase prompts. The `ab-test run` command
selects the matching prompt automatically based on the manifest's `agent_name`.

For custom topics, use `--task "<prompt>"` on the run command.

---

## Prompt Specificity Requirements

- The prompt MUST name the exact INPUT documents to read (briefing section,
  architecture file, requirements file)
- The prompt MUST name the exact OUTPUT file path to create
- The output file MUST NOT exist in the clone after cleanup
- Both versions receive the identical prompt text

---

## Topic Selection Rule

Always use moderate or complex topics. Simple topics produce identical output
that masks governance differences between agent versions.
