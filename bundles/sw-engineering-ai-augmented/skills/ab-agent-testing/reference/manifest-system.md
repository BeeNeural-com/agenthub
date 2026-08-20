# Manifest System

Each agent has an evaluation manifest at `tools/ab-test/manifests/<agent>.yaml`.
The evaluate command reads metrics definitions from this file. A documented
template is available at `tools/ab-test/manifests/_template.yaml`.

---

## Supported Metric Entry Fields

| Field | Purpose |
|---|---|
| `name` | Unique metric identifier (snake_case) |
| `pattern` | Regex to count matches (one match = one hit) |
| `fallback_pattern` | Alternative regex if primary yields zero matches |
| `extract` | Regex with `\K` to capture a value (for validation) |
| `target` | Glob pattern for files to scan (find -path) |
| `exclude` | Filename pattern to skip within target (find ! -name) |
| `required` | If true, zero matches is a failure |
| `validate_against` | Glob for upstream files to cross-check extracted IDs |

---

## Manifest Structure

```yaml
agent_name: "Integration Tester"
agent_file: ".github/agents/integration-tester.agent.md"

cleanup:
  delete:
    - "doc/*/component_integration_tests/*.md"   # Glob patterns for find -path
    - "tests/integration/*.cpp"
  preserve:
    - "_briefing.md"    # Input files to keep
    - "CMakeLists.txt"

metrics:
  phase1:
    - name: spec_count
      pattern: '^#{2,3}\s+TCASE[_: -]'    # Regex (single-quoted in YAML)
      target: "doc/*/component_integration_tests/*.md"  # find -path glob
      exclude: "_briefing.md"              # ! -name filter
```

---

## Adding a New Agent

1. Create `tools/ab-test/manifests/<agent-name>.yaml` (copy `_template.yaml`)
2. Define: cleanup patterns (find -path globs), metrics per phase, rubric weights
3. Add task prompt to `tools/ab-test/prompts/task-definitions.md`
