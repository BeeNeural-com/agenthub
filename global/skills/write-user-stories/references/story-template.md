# User Story Template

Use this template when creating stories for epics in a Jira project or initiative.

## Summary

`<optional-prefix> <verb> <object> <context>`

Examples:
- `Implement prompt caching for LLM gateway`
- `Add retry logic for task failures`
- `Create dashboard for execution metrics`

## Description

```text
As a [role],
I want [specific goal],
So that [measurable benefit].

## Context
Briefly explain why this story exists and how it connects to the parent epic.
Reference the epic key where relevant.

## Scope
**In scope:**
- Item 1
- Item 2

**Out of scope:**
- Item explicitly excluded
```

### Roles to Use

Pick the most appropriate role for the story:
- developer
- platform engineer
- QA engineer
- product owner
- end user
- operations team

## Acceptance Criteria

Use Given/When/Then for behavior-driven criteria when helpful:

```text
### Acceptance Criteria

- [ ] **Given** <precondition>, **When** <action>, **Then** <expected result>
- [ ] **Given** <precondition>, **When** <action>, **Then** <expected result>
- [ ] <Simple checklist item for non-behavioral criteria>
```

### Guidelines
- Each criterion must be independently testable
- Do not add PI sprint headers inside story acceptance criteria
- Include edge cases and error scenarios where relevant
- Avoid implementation details when possible

## Fields

Use the current field model, but supply project-specific values from the confirmed Jira context.

| Field | Value | Custom Field ID |
|-------|-------|----------------|
| Project | `<PROJECT_KEY>` | `project_key` |
| Type | Story | `issuetype` |
| Summary | `<optional-prefix> ...` | `summary` |
| Labels | `<confirmed labels>` | `labels` |
| Epic Link | `<EPIC-KEY>` | `customfield_10000` |
| Story Points | 1 / 2 / 3 / 5 / 8 / 13 | `customfield_10006` |
| Teams | `<confirmed team>` | `customfield_10700` |
| ART | `<confirmed ART>` | `customfield_19516` |
| Acceptance Criteria | array of checklist-item objects | `customfield_10335` |
| Priority | Highest / High / Medium / Low / Lowest | `priority` |

For Jira issue creation, send Teams as an array like `["<Team Name>"]` even if Jira reads the field back as an object.

## Story Point Guide

| Points | Complexity | Example |
|--------|-----------|---------|
| 1 | Very small | Simple, well-understood change |
| 2 | Small | Limited scope with low uncertainty |
| 3 | Medium | Several moving parts or minor unknowns |
| 5 | Large | Cross-component change with notable complexity |
| 8 | Very large | Broad change with significant coordination or uncertainty |
| 13 | Extra large | Too large for a normal story and should usually be split |

Story points represent relative complexity, effort, and uncertainty. Use simple Fibonacci numbers rather than mapping points to days.

If a story exceeds `13 SP`, split it into smaller stories.