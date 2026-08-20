# Test Specification: {spec_name}

<!-- Template: SWE.6 Software Qualification Test Specification -->
<!-- Verifies: Software Requirements (req:*) -->
<!-- ASPICE: SWE.6 — Software Qualification Testing -->

---

## Metadata

```yaml
spec: {spec_name}
feature: {feature_name}
component: {component_name}
aspice_level: SWE.6
```

<!-- Optional: Notes that apply to all test cases in this spec -->
<!-- Example: Log level constraint, numbering offset, shared signals, etc. -->

---

## Qualification Strategy

<!-- Describe the overall qualification strategy for this test spec file.
     Include:
     - Which requirements this spec covers (topic / feature scope)
     - Black-box perspective: tests verify observable behavior only
     - Test environment assumptions (target platform, simulators, proxies)
     - Entry criteria (what must pass before these tests run)
     - Any verification_method constraints (e.g. static_test items excluded)
-->

{Describe the qualification approach, scope, and constraints for this spec.}

---

## Test Design

<!-- T2a output: one row per test condition derived from the upstream req: IDs.
     Classify each requirement type and select technique(s) accordingly:
       Simple interaction (1 path)  → EP (1 happy + 1 error)
       Requirement with limits      → EP + BVA at each boundary
       State-machine / lifecycle    → State Transition (valid + invalid)
       Protocol / message exchange  → EP per message type
       Resource management          → EP + Error Guessing (exhaustion)
       Error recovery               → Error Guessing per error class
     Verify each ID meets the minimum coverage rules from test-design-techniques skill.
     Black-box perspective: partitions must be derivable from the public API contract.
-->

| req: ID | Requirement Type | Technique(s) | Condition Count | Conditions |
|---|---|---|---|---|
| `req:{component}-{id}` | {simple/limits/statemachine/...} | {EP, BVA, State Transition, Error Guessing} | {N} | {List each condition name} |

<!-- Minimum coverage check: every in-scope ID must meet or exceed the threshold
     for its type. If any ID has fewer conditions than required, justify the gap. -->

---

## TCASE_01: {Short_Descriptive_Title}

```yaml
id: qtest-{component}-{topic}-{aspect}
type: {test_type}
level: Component Acceptance
status: Draft
priority: {priority}
fully_automated: true
verifies: {requirement_id}
```

<!-- `:type:` values (ISO 29119 / ISO 26262 / ISO 25010):                  -->
<!--   Functional Suitability  — correct behavior per spec                  -->
<!--   Performance Efficiency  — timing, throughput, resource usage          -->
<!--   Reliability             — fault tolerance, recoverability, maturity   -->
<!--   Security                — access control, integrity, confidentiality  -->
<!--   Compatibility           — coexistence, interoperability               -->
<!--   Fault Injection         — forced error paths (ISO 26262)             -->
<!--   Stress Testing          — behavior at/beyond limits (ISO 26262)      -->
<!--   Resource Usage          — memory, CPU, handle exhaustion (ISO 26262) -->
<!--   Back-to-Back Testing    — compare two implementations (ISO 26262)    -->
<!--                                                                         -->
<!-- `:priority:` values: High | Medium | Low                               -->
<!--                                                                         -->
<!-- `:status:` values: Draft | Review | Approved                           -->

### Description

<!-- This IS the test condition. Describe:
     1. WHAT is being verified (component behavior)
     2. WHEN / under what trigger condition
     3. WHY it matters (the expected outcome)
     Include the test strategy/technique if relevant.
-->

{Verify that {component} {expected_behavior} when {trigger_condition}.
Detailed description of what is being verified and the test strategy used.}

### Preconditions

<!-- Optional. Delete section if not needed. -->

- {System state before test execution}
- {Dependencies that must be set up}

### Postconditions

<!-- Optional. Delete section if not needed. -->

- {System state after test execution}
- {Cleanup expectations}

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | {Action description} | {Hard expected result, e.g. `returns true`, `== 4`} |
| 2 | {Action description} | {Hard expected result} |
| 3 | {Action description} | {Hard expected result} |

<!-- Rules:
     - Each step = one observable action + one verifiable expected result
     - Expected column: concrete assertions, not vague ("works correctly")
     - Last step should be EXPECT_STEPS(N) if using step-counter pattern
     - Keep steps atomic: one action per row
-->

---

## TCASE_02: {Short_Descriptive_Title}

```yaml
id: qtest-{component}-{topic}-{aspect}
type: {test_type}
level: Component Acceptance
status: Draft
priority: {priority}
fully_automated: true
verifies: {requirement_id}
```

### Description

{Test condition description}

### Preconditions

<!-- Optional. Delete section if not needed. -->

- {precondition}

### Postconditions

<!-- Optional. Delete section if not needed. -->

- {postcondition}

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | {Action description} | {Hard expected result} |
| 2 | {Action description} | {Hard expected result} |

---

<!-- Copy TCASE section above to add more test cases. -->
<!-- Numbering: TCASE_NN where NN is sequential within this spec file. -->
