---
name: write-user-stories
description: "Write and refine Jira user stories from epics for a target project or initiative. Use when creating stories from epics, breaking down epics into stories, mapping stories to epic PI sprints, writing plain story acceptance criteria, or batch-creating stories in Jira."
argument-hint: "Epic key or description, plus project context if needed."
tags: ['story', 'jira']
---

# Write User Stories

Generate well-structured user stories from Jira epics in the confirmed Jira scope.

> **Prerequisite**: The parent epic should have a complete description with all required sections.

## When to Use

- An epic exists but has no child stories yet
- An epic's stories need refinement or are incomplete
- You need to break a large epic into deliverable increments aligned to epic PI sprint checkpoints
- You want to batch-create stories across multiple epics

## Procedure

### Step 1: Confirm the Jira Scope

Before drafting stories, confirm:
- Jira project key
- Optional initiative or workstream name
- Optional summary prefix
- Optional label set
- Any required default field values such as Teams or ART

### Step 2: Fetch the Epic

Retrieve the epic using its key. Read:
- Summary and description
- Acceptance criteria and epic PI sprint checkpoints
- Existing child stories via JQL: `project = <PROJECT_KEY> AND "Epic Link" = <epic-key>`
- Priority and labels

If the epic description is incomplete or missing sections, stop and use the `write-epics` skill first.

### Step 3: Identify Story Boundaries

Analyze the epic scope and decompose it into stories by identifying:
- Distinct user-facing capabilities
- Technical enablers
- Integration points
- PI sprint alignment

Each story should be completable within a single sprint.

### Step 4: Write Each Story

Follow the [story template](./references/story-template.md) for each story. Every story must include:

1. **Summary**: follow the confirmed naming convention
2. **Description**:

```text
As a [role],
I want [specific goal],
So that [measurable benefit].

## Context
<Why this story exists, how it fits into the epic>

## Scope
- In scope: <what this story covers>
- Out of scope: <what it explicitly does not cover>
```

3. **Acceptance Criteria**: Specific, testable conditions using Given/When/Then or checklist format. Do not include PI sprint headers inside the story.
4. **Story Points**: Estimate using the current scale.
5. **Labels**: use the confirmed labels if any.
6. **Epic Link**: Parent epic key.

### Step 5: Check Coverage

After drafting all stories, validate:
- Every acceptance criterion in the epic is addressed by at least one story
- Every epic PI sprint header in scope has stories mapped to it
- No story exceeds `13 SP`
- Stories have a logical dependency order
- No duplicate or overlapping stories with existing ones

### Step 6: Present for Review

Present all proposed stories in a summary table:

| # | Summary | Points | Target Sprint | Dependencies |
|---|---------|--------|---------------|-------------|
| 1 | <summary> | 3 | PI26.2.1 | — |
| 2 | <summary> | 5 | PI26.2.2 | Story 1 |

Then show the full detail of each story below the table.

### Step 7: Create in Jira

After user approval:
1. Use `batch_create_issues` to create all stories at once
2. Link each story to its parent epic using `customfield_10000` or `link_to_epic`
3. Create issue links for story-to-story dependencies
4. Confirm creation with a summary of created ticket keys

#### Current Custom Fields for Story Creation

The current workflow assumes these custom fields remain available. Keep them unless the user tells you the mapping has changed.

| Field | Custom Field ID | Value |
|-------|----------------|-------|
| Epic Link | `customfield_10000` | `"<EPIC-KEY>"` |
| Story Points | `customfield_10006` | number |
| Teams | `customfield_10700` | `["<Team Name>"]` when required |
| ART | `customfield_19516` | `["<ART Name>"]` when required |
| Acceptance Criteria | `customfield_10335` | array of checklist-item objects |

Example `additional_fields`:

```json
{
  "customfield_10000": "<EPIC-KEY>",
  "customfield_10006": 3,
  "customfield_10700": ["<Team Name>"],
  "customfield_19516": ["<ART Name>"],
  "labels": ["<initiative-label>"]
}
```

#### Writing Acceptance Criteria — `customfield_10335`

Always use structured objects with explicit `mandatory: false`:

```json
{
  "customfield_10335": [
    {"name": "Criterion one",   "isHeader": false, "mandatory": false},
    {"name": "Criterion two",   "isHeader": false, "mandatory": false},
    {"name": "Criterion three", "isHeader": false, "mandatory": false}
  ]
}
```

Rules:
- Include `"mandatory": false` on every item.
- Send the full array every time.
- Do not add PI sprint headers inside story acceptance criteria.

## Quality Criteria

A good user story set satisfies INVEST:
- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable

## References

- [Story Template](./references/story-template.md)