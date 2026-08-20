---
name: prompt-engineering
description: >-
  Design system prompts, few-shot examples, and tool instructions for reliable LLM behavior. Use when building or tuning AI features.
tags: [ai-operations, prompt]
---

# Prompt Engineering

## When to Use

- New LLM-powered feature or agent
- Existing prompts show inconsistency or drift
- Migrating to a different model family

## Procedure

### Step 1: Define task contract

- Input/output schema and edge cases
- Tone, length, and format constraints
- Tools the model may call and when

### Step 2: Draft system prompt

- Role, rules, and refusal boundaries
- Step-by-step reasoning instruction if needed
- Examples: 2–5 diverse few-shot pairs

### Step 3: Harden

- Add anti-injection and scope limits
- Specify citation or 'I don't know' behavior
- Remove conflicting instructions

### Step 4: Iterate with eval

- Run **prompt-evaluation** regression set
- Compare models on cost/latency/quality
- Version prompts in git with changelog

## Output

Prompt files in repo + eval results in `doc/ai/prompt-<feature>.md`.
