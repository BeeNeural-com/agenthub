# Test Specification: {spec_name}

<!-- Template: SWE.5 Integration Test Specification -->
<!-- Verifies: Architecture Elements (arch:* with classification: sequence/statemachine/activity) -->
<!-- ASPICE: SWE.5 — Software Integration Testing -->

---

## Metadata

```yaml
spec: {spec_name}
feature: {feature_name}
component: {component_name}
aspice_level: SWE.5
```

<!-- Optional: Notes that apply to all test cases in this spec -->

---

## Integration Strategy

<!-- Describe the overall integration strategy for this test spec file.
     This section satisfies ASPICE SWE.5 BP1 RL.2 — integration strategy.
     Include:
     - Integration order (bottom-up, top-down, incremental, big-bang)
     - Which architectural elements are integrated in this spec
     - Key integration boundaries / interfaces under test
     - Test environment assumptions (stubs, mocks, real components)
     - Entry criteria (what must pass before these tests run)
-->

{Describe the integration approach, order, and boundaries for this spec.}

---

## Test Design

<!-- T2a output: one row per test condition derived from the upstream arch: IDs.
     Use the classification field to select the right technique:
       statemachine → State Transition (all valid + invalid transitions)
       sequence     → EP (full sequence) + Error Guessing (failure paths)
       activity     → EP (branches) + BVA (guards with limits)
       decision     → BVA (boundary conditions)
       operation    → EP (happy + error partitions)
     Verify each ID meets the minimum coverage rules from test-design-techniques skill.
-->

| arch: ID | Classification | Technique(s) | Condition Count | Conditions |
|---|---|---|---|---|
| `arch:{component}-{id}` | {statemachine/sequence/...} | {EP, BVA, State Transition, Error Guessing} | {N} | {List each condition name} |

<!-- Minimum coverage check: every in-scope ID must meet or exceed the threshold
     for its type. If any ID has fewer conditions than required, justify the gap. -->

---

## TCASE_01: {Short_Descriptive_Title}

```yaml
id: itest-{component}-{topic}-{aspect}
type: {test_type}
level: {test_level}
status: Draft
priority: {priority}
fully_automated: true
verifies: {architecture_element_id}   # Use the full arch: ID from SWE.2 (e.g., arch:libipc-seq-connection-lifecycle)
```
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
<!-- `:level:` values for SWE.5:                                            -->
<!--   Integration Test  — component-to-component interaction               -->
<!--   Interface Test    — verify data exchange across defined interfaces    -->
<!--   Scenario Test     — end-to-end behavior across multiple components   -->
<!--                                                                         -->
<!-- `:priority:` values: High | Medium | Low                               -->
<!--                                                                         -->
<!-- `:status:` values: Draft | Review | Approved                           -->

### Description

<!-- This IS the test condition. Describe:
     1. WHAT interaction/interface is being verified
     2. WHICH components are involved and their roles
     3. WHAT data flows across the boundary
     4. WHY the integration point matters
     Include the test strategy/technique if relevant.
-->

{Verify that {component_A} and {component_B} {expected_interaction} when {trigger_condition}.
Detailed description of the integration point under test, the data exchanged,
and the observable outcome at each component boundary.}

### Preconditions

<!-- Optional. Delete section if not needed. -->

- {Components deployed and reachable}
- {Communication channels established}
- {Configuration / signal environment set up}

### Postconditions

<!-- Optional. Delete section if not needed. -->

- {Integration state after test}
- {Cleanup expectations}

### Test Procedure

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | {Action description — specify which component performs it} | {Hard expected result at the receiving/observing side} |
| 2 | {Action description} | {Hard expected result} |
| 3 | {Action description} | {Hard expected result} |

<!-- Rules:
     - Each step = one observable action + one verifiable expected result
     - Expected column: concrete assertions, not vague ("works correctly")
     - For interface tests: clearly state which side sends and which observes
     - For scenario tests: indicate component boundaries crossed per step
     - Last step should be EXPECT_STEPS(N) if using step-counter pattern
     - Keep steps atomic: one action per row
-->

---

## TCASE_02: {Short_Descriptive_Title}

```yaml
id: itest-{component}-{topic}-{aspect}
type: {test_type}
level: {test_level}
status: Draft
priority: {priority}
fully_automated: true
verifies: {architecture_element_id}   # Use the full arch: ID from SWE.2
```

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
