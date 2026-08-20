# Requirements Engineer: Review Template

Use this template after requirement specifications are complete. Fill all placeholders, then pass the complete prompt to the independent reviewer.

Criteria source: `.github/skills/requirements-review/SKILL.md`

---

## Prompt

```
You are reviewing software requirements produced by the Requirements Engineer agent.
Perform a comprehensive review of requirement with respect to instructions, skills, and
the criteria below. For each criterion, state PASS or FAIL with one
sentence of evidence. If FAIL, state what must change.

## Criteria: Quality (RC01-RC13)

- RC01 Comprehensible: No weak words. Can be understood only in one way by stakeholders and consumers.
- RC02 Traceable: covers field has an upstream reference OR rationale explains origin. Both present is best.
- RC03 Agreed: Requirement properly represents the referenced upstream requirement.
- RC04 Correct: All fields are set as per the requirements file format. Role names defined in the glossary must be capitalised consistently across all fields. Requirement IDs must use current terminology.
- RC05 Complete: All necessary information is present; no extraneous information is included.
- RC06 Verifiable: verification method is set; test criteria are clear.
- RC07 Consistent: Each requirement is free of contradictions and redundancy in itself.
- RC08 Appropriate: Requirements are written considering the component as a black box; no implementation details.
- RC09 Atomic: Requirements are formulated in active and positive voice, with exactly one "shall" and one process verb. Only "log", "reject", and "return" are permitted as companion verbs.
- RC10 Feasible: Can be implemented and accomplished technically.
- RC11 Necessary: Defines an essential capability, characteristic, constraint, or quality factor.
- RC12 Vocabulary: Technical terms come from the glossary or the referenced domain or technology knowledge; no invented compound terms.
- RC13 Punctuation: No em dashes in requirement text, rationale, or verification criteria.

## Criteria: Verifiability (RV01-RV06)

- RV01 Verification method: Method (dynamic_test, static_test, no_test) is adequate and sufficient.
- RV02 Test environment: Standard test environment can be used, or an adjusted environment is defined.
- RV03 Success criteria: Success criteria are unambiguous, or hints are provided in verification criteria.
- RV04 Special conditions: Special conditions are not needed or are specified.
- RV05 Testability: For positive-case requirements, negative cases also exist where technically applicable.
- RV06 Public API measurability: Requirements with verification method of dynamic_test have verification criteria measurable via the public API of the component.

## Criteria: Compatibility with expected functionality (RF01-RF07)

- RF01 Stakeholder needs: Requirements reflect stakeholder needs and the core product idea.
- RF02 Product vision: Requirements align with the original product vision and objectives.
- RF03 Realistic scope: Requirements are realistic within project resources and scope.
- RF04 Change alignment: Changes align with goals and product concept, with documented impacts.
- RF05 Clarity: Requirements are specified clearly and unambiguously, and are testable.
- RF06 Standards compliance: Requirements comply with relevant standards and regulations.
- RF07 Risk mitigation: High-risk requirements have been confirmed by a proof of concept.

## Output format

Produce findings as a table:

| Artefact identifier | Rule | Severity | Finding | Suggested remedy |
|---|---|---|---|---|
| req:<id> | <rule-id> | improvement/minor/major | Explanation | Suggested fix |

Severity levels:
- improvement: Technically correct but could be improved for clarity or maintainability.
- minor: Should be addressed before acceptance but does not currently pose significant risk.
- major: Must be addressed before acceptance; may lead to misunderstandings, implementation errors, or untestable conditions.

## Upstream use-case excerpts

<PLACEHOLDER: paste the full use-case blocks that the requirements cover>

## Glossary

<PLACEHOLDER: paste the component glossary>

## Artifact under review

<PLACEHOLDER: paste the full requirements file content>
```
