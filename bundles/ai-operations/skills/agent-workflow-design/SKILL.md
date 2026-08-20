---
name: agent-workflow-design
description: >-
  Design multi-step agent workflows with tools, gates, and human checkpoints. Use for autonomous task automation.
tags: [ai-operations, agent]
---

# Agent Workflow Design

## When to Use

- Building Cursor/Agent Hub style multi-tool workflow
- Replacing brittle script chain with agent orchestration
- Adding human-in-the-loop approval steps

## Procedure

### Step 1: Decompose task

- Break into steps with clear inputs/outputs
- Identify which steps need tools vs LLM reasoning
- Mark irreversible actions for human gate

### Step 2: Tool design

- Minimal tool set; clear descriptions for model
- Idempotent tools where possible
- Timeout and retry policy per tool

### Step 3: State and memory

- What persists between steps (scratchpad, files)
- Avoid unbounded context growth
- Log trajectories for debugging

### Step 4: Validate

- Run golden-path and failure scenarios
- Measure cost and latency per workflow run
- Document escalation to human operator

## Output

Workflow spec at `doc/ai/agent-workflow-<name>.md`.
