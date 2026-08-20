---
name: requirements-gap-analysis
description: "Gap analysis taxonomy, workflow, and report template for software requirements. Use to detect structural and content gaps in a component requirement specification."
---

# Requirements gap analysis

This skill defines the gap categories, analysis workflow, and report template for requirements gap detection.

## Gap categories

Gap categories are grouped into the following severity levels:

### Major

Major gaps must be fixed before any requirement can be approved.

| ID | Gap | Detection |
|---|---|---|
| G01 | **Missing failure path** | A functional requirement describes a successful operation but no corresponding requirement for the failure path exists |
| G02 | **Missing success path** | A requirement for the failure path exists but no corresponding requirement for the success path exists |
| G03 | **Missing upstream reference** | A requirement's upstream references are empty or include a TODO placeholder |
| G04 | **Missing or generic verification criteria** | A requirement with verification method `dynamic_test` or `static_test` has no verification criteria, has generic verification criteria (i.e., criteria that just restate the requirement), or includes a TODO placeholder |
| G05 | **Missing rationale for requirements without upstream references** | A requirement's upstream reference is missing or includes a TODO placeholder, but no rationale explains its origin |
| G06 | **Unresolved TODO in requirement text** | The requirement text contains a TODO placeholder |

### Minor

Minor gaps should be fixed before final approval.

| ID | Gap | Detection |
|---|---|---|
| G07 | **Rationale restates the requirement** | The rationale text is semantically equivalent to the requirement sentence, i.e., adds no new information |
| G08 | **Verification criteria restates the requirement** | The verification criteria are semantically equivalent to the requirement sentence, i.e., they do not specify test setup, trigger, and expected outcome |
| G09 | **Missing resource cleanup requirement** | A component acquires a system resource (e.g., file descriptor, memory, socket) but has no requirement for releasing it on destruction or error |
| G10 | **Missing sensitive-data exclusion constraint** | A logging requirement exists but no corresponding constraint exists on what data must be excluded from logs (e.g., personally identifiable information, passwords) |

### Improvement

Gaps categorized as improvements would improve the clarity and maintainability of the requirement, which is technically correct as written.

| ID | Gap | Detection |
|---|---|---|
| G11 | **Information block reads like a requirement** | An informational block contains language that implies a testable behavioral obligation; make the text non-normative |
| G12 | **Topic file with a single requirement** | A topic file contains only one requirement; consider moving to another topic unless the topic is expected to grow |

---

## Gap analysis workflow

### Step 1: Collect all requirement and information blocks

Read every topic file `doc/<component>/component_requirements/*.md` and the requirement and information blocks they contain.

### Step 2: Check requirements and information blocks for gaps

For each requirement and information block, check for the presence of gaps in the categories above.

### Step 3: Produce gap report

Produce a gap report in the format described below, with a summary and a detailed list of findings for each defined gap and gap category. Within each gap category, list the finding groups in the order of the corresponding gap identifier (e.g., G01 before G02).

---

## Gap report template

```markdown
# Requirements gap report: <Component> - <date>

## Summary

| Severity    | Count |
|-------------|-------|
| Major       | N     |
| Minor       | N     |
| Improvement | N     |

## Major gaps

**[<gap-identifier>] <gap name>**
| Artefact ID | Gap description | Solution |
|-------------|-----------------|----------|
| <requirement-identifier> | <describe the problem with the given requirement with respect to the identified gap> | <proposed solution> |

## Minor gaps

<same format as major gaps>

## Improvements

<same format as major gaps>
```
