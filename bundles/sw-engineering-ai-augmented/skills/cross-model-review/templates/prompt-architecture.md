# Software Architect: Review Template

Use this template after the architectural design specification is complete. Fill all placeholders, then pass the complete prompt to the independent reviewer.

Criteria source: `.github/skills/architecture-review/SKILL.md`

---

## Prompt

```
You are reviewing a software architectural design specification produced by the Software Architect agent.
Perform a comprehensive review of each specification fragment with respect to instruction, skills and
the criteria below.
For each criterion, state PASS or FAIL with one sentence of evidence. If FAIL, state what must change.

## Criteria (AD01-AD11)

- AD01 Traceability: Every specification fragment has a unique identifier.
- AD02 Identifier format: Specification fragment identifiers use the correct component prefix (arch:<component>-<descriptive-kebab-case-id>).
- AD03 Status: New or modified specification fragments have status draft.
- AD04 Vocabulary: All technical terms or actor names used in the specification fragment descriptions are from the requirements or glossary.
- AD05 Abstraction: No internal implementation details in specification fragment descriptions. Describe observable behavior and contracts at element boundaries, not POSIX primitives or internal data structures.
- AD06 Rationale: Rationale, if present, is meaningful (not just repeating or rephrasing the specification fragment description).
- AD07 Coverage: Every component requirement is referenced in the covers field of at least one specification fragment.
- AD08 Completeness (operations): Every operation of an element is covered in at least one sequence diagram.
- AD09 Completeness (operation outcomes): Every normal outcome and every distinct error outcome of an operation of an element is covered in at least one sequence diagram.
- AD10 Completeness (state transitions): Every state transition of a stateful element is observable in at least one sequence diagram.
- AD11 Completeness (external trigger states): Every state transition that can be triggered or provoked by an external element has those external triggers covered in at least one sequence diagram.

## Severity levels

- improvement: The specification is technically correct as is but could be improved for clarity or maintainability.
- minor: The finding should be addressed before the specification is accepted but does not currently pose a significant risk.
- major: The finding must be addressed before the specification can be accepted, as it may lead to misunderstandings, implementation errors, or untestable conditions.

## Output format

Produce findings as a table:

| Artefact identifier | Rule | Severity | Finding | Suggested remedy |
|---|---|---|---|---|
| arch:<id> | <rule-id> | improvement/minor/major | Explanation of why the fragment violates the rule | Suggested update |

After the table, provide:
1. A per-criterion summary (PASS/FAIL with one sentence of evidence).
2. A count of findings by severity.
3. A list of any uncovered requirements (AD01 check).

## Component requirements (upstream)

<PLACEHOLDER: paste all component requirement files content>

## Glossary

<PLACEHOLDER: paste the component glossary>

## Artifact under review

<PLACEHOLDER: paste all component_architecture/*.md file contents>
```
