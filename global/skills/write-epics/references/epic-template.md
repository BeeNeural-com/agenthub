# Epic Template

Use this template when creating or refining epics for a Jira project or initiative.

## Jira Fields

Use the current field model, but supply project-specific values from the confirmed Jira context.

| Field | Value | Custom Field ID |
|-------|-------|----------------|
| Project | `<PROJECT_KEY>` | `project_key` |
| Type | Epic | `issuetype` |
| Summary | `<optional-prefix> <concise epic title>` | `summary` |
| Epic Name | Same as summary without any prefix | `customfield_10002` |
| Labels | `<confirmed labels>` | `labels` |
| Teams | `<confirmed team>` | `customfield_10700` |
| ART | `<confirmed ART>` | `customfield_19516` |
| Acceptance Criteria | array of checklist-item objects | `customfield_10335` |
| Priority | Highest / High / Medium / Low / Lowest | `priority` |

For Jira issue creation, send Teams as an array like `["<Team Name>"]` even if Jira reads the field back as an object.

## Description Structure

Every epic description must contain all of the following sections. Use `TBD` for unknown values.

```text
<Description — high-level summary of what the epic delivers>

## Problem Statement / Motivation
<Why this epic exists, what problem it solves>

## Stakeholders
| Team | Name |
|------|------|
| TBD  | TBD  |

## Scope (In Scope)
- <what this epic covers>

## Out of Scope
- <what is explicitly excluded>

## Business Outcomes
- <measurable business results>

## Success Criteria
- <how we know the epic is done>

## Non-Functional Requirements
- <performance, security, scalability, etc.>

## Dependencies
- <other epics, teams, systems, or external factors>

## Additional Information
<links, references, context>
```

## Section Guidelines

### Description
One to three sentences summarizing the epic deliverable.

### Problem Statement / Motivation
Explain the pain point or opportunity. Why does this matter now?

### Stakeholders
List teams and individuals with a stake in this epic.

### Scope (In Scope)
Bullet list of what this epic will deliver.

### Out of Scope
Bullet list of related things this epic will not cover.

### Business Outcomes
Measurable results expected when the epic is complete.

### Success Criteria
How the epic will be verified as done.

### Non-Functional Requirements
Performance, security, scalability, compliance, or observability requirements.

### Dependencies
Links to other epics, teams, external systems, or decisions that must happen first. Use Jira keys where known.

### Additional Information
Links to design docs, diagrams, or related references.

## Acceptance Criteria (Program Increment Sprint-Based)

Define PI sprint headers as checkpoints within the epic. First specify the Program Increment identifier and sprint count for the planning window.

```text
### Acceptance Criteria

**PI26.2.1 — <sprint objective>**
- [ ] <specific, testable criterion>
- [ ] <specific, testable criterion>

**PI26.2.2 — <sprint objective>**
- [ ] <specific, testable criterion>
- [ ] <specific, testable criterion>

**PI26.2.3 — <sprint objective>**
- [ ] <specific, testable criterion>
```

### PI Sprint Header Guidelines
- This header model applies to epics only
- Each PI sprint header is a meaningful delivery checkpoint
- Name headers descriptively after the sprint code
- Order headers by delivery sequence
- Cross-reference related epic checkpoints where dependencies exist