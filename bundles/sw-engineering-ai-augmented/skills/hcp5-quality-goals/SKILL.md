---
name: hcp5-quality-goals
description: "Machine-readable HCP5 Software Platform Quality Goals: maturity levels, KPI thresholds, and agent consumption rules. Use when performing automated quality assessment or risk evaluation for HCP5 components."
---


# HCP5 Quality Goals

## Evaluation Rules

- Assess **one component at a time** — never aggregate across the whole product in a single pass.
- Assessment scope: the component explicitly named in the current task.
- Granularity: per Program Increment (PI) and per maturity level (beta / F4 / F6 / F8).
- Deviations from thresholds: flag with `deviation: true` and require a `justification` field in the output.
- KPIs not automatically measurable: set `measured: false` and trigger `risk_analysis: required`.

---

## Maturity Levels

| key    | alias | description       |
|--------|-------|-------------------|
| beta   | —     | Development Version |
| stable | F4    | 100% Software     |
| mature | F6    | 100% Test         |
| sop    | F8    | Market Release    |

---

## ECU Component Quality Goals

| category         | KPI                    | beta  | stable | mature | sop    |
|------------------|------------------------|-------|--------|--------|------- |
| requirements     | sw_req_released        | <60%  | >=60%  | >=80%  | >=95%  |
| requirements     | swc_req_linked_source  | <60%  | >=60%  | >=80%  | >=95%  |
| testing          | req_test_coverage      | <60%  | >=60%  | >=80%  | >=95%  |
| code_coverage    | C0                     | <60%  | >=60%  | >=80%  | 100%*  |
| code_coverage    | C1                     | <60%  | >=60%  | >=80%  | 100%*  |
| defects          | blocker_critical       | —     | —      | —      | 0      |

*deviation_justification_required: true

---

## Static Code Analysis Rules

| tool              | KPI                | beta   | stable | mature | sop |
|-------------------|--------------------|--------|--------|--------|-----|
| compiler          | warnings           | —      | —      | —      | 0   |
| clang             | warnings_per_loc   | >15%   | <=15%  |  <=10% | <=5%|
| clang             | NOMV               | —      | —      | —      | 0   |
| clang             | NOSECV             | —      | —      | —      | 0   |
| misra             | high_highest       | —      | —      | —      | 0   |

---

## Security Requirements

| category   | KPI    | sop |
|------------|----------|----------|
| sanitizers | ASAN     | 0        |
| sanitizers | LSAN     | 0        |
| sanitizers | UBSAN    | 0        |
| sanitizers | TSAN     | 0        |
| checksec   | NX       | true     |
| checksec   | PIE      | true     |
| checksec   | RELRO    | true     |
| checksec   | violations | 0      |

---

## Open Source Software (OSS)

| category               | KPI              | sop |
|--------------------|--------------------|----------|
| awareness          | dev_handbook       | required |
| awareness          | foss_guide         | required |
| scan               | report_available   | true     |
| scan               | approval_required  | true     |
| policy_violations  | blocker            | 0        |
| policy_violations  | critical           | 0        |
| vulnerabilities    | critical           | 0        |
| vulnerabilities    | high               | 0        |

---

## Third-Party Software

| check                    | value |
|--------------------------|-------|
| acceptance_criteria      | must be defined if no standard criteria exist |
| defects blocker_critical | 0     |

## Process Quality Goal

| target        | value         |
|---------------|---------------|
| ASPICE level  | Level 1       |

---

## Agent Behavior Rules

| rule                  | value                        |
|-----------------------|------------------------------|
| always_validate       | maturity_level, KPI_thresholds |
| if_not_measurable     | risk_analysis                |
| output_formats        | json, yaml, markdown         |

---

## Multi-Agent Consumption Model

Each agent selects only the domains and metrics relevant to its responsibility. No global state assumption.

| agent                  | domains                                                        | metrics                                          |
|------------------------|----------------------------------------------------------------|--------------------------------------------------|
| code_quality_agent     | ECU_Component                                            | C0, C1, compiler_warnings, misra.high_highest    |
| test_quality_agent     | ECU_Component                                                  | req_test_coverage, req_coverage                  |
| security_agent         | ECU_Component, OSS_General, OSS_Modified, Third_Party_Software | ASAN, LSAN, UBSAN, TSAN, vulnerabilities         |
| oss_compliance_agent   | OSS_General, OSS_Modified                                      | policy_violations, approval_required             |
| auditor_agent  | Process_Quality                                                | ASPICE_Level                                     |

**Extraction rules:**
- Apply only the applicable maturity level thresholds.
- Do not reinterpret metric semantics, override thresholds, or infer missing data.

---

## Metrics Definitions

| id                    | name                              | domain          | unit | description |
|-----------------------|-----------------------------------|-----------------|------|-------------|
| C0                    | Line Coverage                     | Code Coverage   | %    | Executable source lines executed during testing |
| C1                    | Branch Coverage                   | Code Coverage   | %    | Decision branches executed during testing |
| sw_req_released       | Software Requirements Released    | Requirements    | %    | Share of requirements formally released and baselined |
| swc_req_linked_source | SWC Requirements Linked to Source | Traceability    | %    | Share of requirements traceably linked to source code |
| req_test_coverage     | Requirements Test Coverage        | Testing         | %    | Share of requirements covered by at least one executed test |
| compiler_warnings     | Compiler Warnings                 | Static Analysis | count | Number of unresolved compiler warnings in build output |

---

## Output Contract

- Output **must be machine-readable**
- Each assessment must contain:
  - component_id
  - maturity_level
  - passed
  - failed
  - deviations
  - risk_assessment
