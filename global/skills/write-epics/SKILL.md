---
name: write-epics
description: "Write and refine Jira epics for a target project or initiative. Use when creating new epics, completing epic descriptions, filling missing sections, defining stakeholders, scope, business outcomes, success criteria, non-functional requirements, dependencies, and Program Increment sprint-based epic acceptance criteria."
argument-hint: "Epic key or goal, plus project context if needed."
tags: ['epic', 'jira']
---

# Write Epics

Create and refine epics for the Jira project or initiative the user specifies.

## When to Use

- A new epic needs to be created
- An existing epic has an incomplete or missing description
- Epic sections need to be filled in
- Epics need Program Increment sprint-based acceptance criteria
- Cross-epic PI sprint alignment is needed

## Procedure

### Step 1: Confirm the Jira Scope

Before writing or refining anything, confirm:
- Jira project key
- Optional initiative or workstream name
- Optional summary prefix
- Optional label set
- Any required default field values such as Teams or ART

### Step 2: Discover Existing Epics

Query current epics for context using the confirmed Jira scope. Example patterns:

```jql
project = <PROJECT_KEY> AND issuetype = Epic ORDER BY rank ASC
```

If the scope includes a label:

```jql
project = <PROJECT_KEY> AND issuetype = Epic AND labels = "<LABEL>" ORDER BY rank ASC
```

This builds a picture of the initiative so new or refined epics fit coherently.

### Step 3: Fetch or Draft the Epic

If refining an existing epic, retrieve it by key and review which sections of the description are missing or incomplete.

If creating a new epic, gather the goal from the user and prepare a summary using the confirmed naming convention:
- **Summary**: `<optional-prefix> <concise epic title>`
- **Labels**: use the confirmed labels if any
- **Project**: use the confirmed project key

### Step 4: Write the Epic Description

The description field must follow this structure exactly. Use the [epic template](./references/epic-template.md) as reference.

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

Rules:
- All sections are required. If information is unknown, mark it `TBD`.
- Derive scope, outcomes, and dependencies from the epic summary and conversation context.
- Cross-reference related epics when filling Dependencies.

### Step 5: Define Epic Acceptance Criteria with Program Increment Sprint Headers

Before writing epic acceptance criteria, determine the PI planning specification for the epic:
- PI identifier, for example `PI26.2`
- Sprint count for that PI planning window
- Sprint naming convention, defaulting to `<PI>.<sprint-number>`

Write epic acceptance criteria using PI sprint headers:

```text
### Acceptance Criteria

**PI26.2.1 — <sprint objective>**
- [ ] <criterion 1>
- [ ] <criterion 2>

**PI26.2.2 — <sprint objective>**
- [ ] <criterion 3>
- [ ] <criterion 4>
```

Guidelines:
- This PI sprint header model applies to epics only.
- Each sprint header represents a meaningful delivery checkpoint.
- Criteria must be specific and verifiable.
- Do not assume a fixed number of sprints per PI.

### Step 6: Validate Completeness

Check that the epic has:
- A summary following the confirmed naming convention
- The confirmed label set if one is required
- All description sections filled or explicitly marked `TBD`
- PI sprint-based epic acceptance criteria defined
- Dependencies referencing actual epic keys where known
- No overlap with existing epics in scope

### Step 7: Present for Review

Show the complete epic summary, description, and acceptance criteria for user review. Highlight any `TBD` fields that need follow-up.

### Step 8: Create or Update in Jira

After user approval:
- **New epic**: Use `create_issue` with `issuetype: Epic`
- **Existing epic**: Use `update_issue` to set the description and acceptance criteria
- If PI sprint checkpoints should be represented as Jira versions, use `create_version`
- Confirm the update with the ticket key

#### Current Custom Fields for Epic Creation

The current workflow assumes these custom fields remain available. Keep them unless the user tells you the mapping has changed.

| Field | Custom Field ID | Value |
|-------|----------------|-------|
| Epic Name | `customfield_10002` | `"<Epic Title>"` |
| Teams | `customfield_10700` | `["<Team Name>"]` when required |
| ART | `customfield_19516` | `["<ART Name>"]` when required |
| Acceptance Criteria | `customfield_10335` | array of checklist-item objects |

Example `additional_fields`:

```json
{
  "customfield_10002": "Epic Title",
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
    {"name": "PI26.2.1 — Foundation",  "isHeader": true,  "mandatory": false},
    {"name": "Criterion one",          "isHeader": false, "mandatory": false},
    {"name": "Criterion two",          "isHeader": false, "mandatory": false},
    {"name": "PI26.2.2 — Integration", "isHeader": true,  "mandatory": false},
    {"name": "Criterion three",        "isHeader": false, "mandatory": false}
  ]
}
```

Rules:
- Include `"mandatory": false` on every item.
- Send the full array every time.
- Do not put acceptance criteria in the description body when this field is available.

## Cross-Epic PI Sprint Alignment

When refining multiple epics:
1. List all epic PI sprint headers across the target scope
2. Identify which sprint checkpoints must complete before others can start
3. Flag conflicting or redundant sprint sequencing
4. Propose a unified PI timeline

## References

- [Epic Template](./references/epic-template.md)