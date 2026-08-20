---
name: sop-risk-evaluation
description: "Deterministic KPI-based SOP release risk evaluation for HCP5 Compute Platform: risk classes, thresholds, aggregation logic, and mandatory output fields. Use when evaluating SOP release compliance for HCP5 components."
---


# HCP5 SWP – SOP Risk Evaluation Instruction

**Instruction ID:** HCP5_SWP_SOP_RISK_EVALUATION  
**Version:** 25  
**Export Date:** 2026-03-23  
**Scope:** HCP5 Compute Platform – SOP Releases  
**Scope Owner:** Ruckhaber, Anastasia (TX-HA)

---

## 1. Purpose

This document defines a deterministic, KPI-based risk evaluation instruction for software components to decide SOP release compliance according to the **HCP5 SWP Guideline – How to perform Risk Evaluation for SOP Releases**.

The instruction is designed to be:
- machine-readable
- audit-proof
- unambiguous
- suitable for automation (Copilot, pipelines, scripts, quality gates)

---

## 2. Input Requirements

### Mandatory Inputs

- `component_id`

### Reporting Sources

- KPI Lake
- 100% Software Report
- Static Code Analysis
- Test Management System
- Defect Tracking System
- FOSS Management

---

## 3. Risk Model

### Evaluation Type

- KPI-based
- Aggregation level: **Component**

### Risk Classes

- LOW
- MODERATE
- HIGH
- VERY_HIGH

---

## 4. KPI Evaluation

### 4.1 Requirements Coverage

| KPI | Metric | LOW | MODERATE | HIGH | VERY HIGH |
|---|---|---|---|---|---|
| Released / Accepted Requirements | % | >95 | 80–95 | 60–80 | <60 |
| Linked to SW Design | % | >95 | 80–95 | 60–80 | <60 |
| Linked to Platform Requirements | % | >95 | 80–95 (rationale) | 60–80 (rationale) | <60 (rationale) |

---

### 4.2 Test Coverage

**Evaluation Rule:**
Only *Requirements Test Coverage* is explicitly rated for risk evaluation. All other test KPIs are implicitly included.

| KPI | Metric | LOW | MODERATE | HIGH | VERY HIGH |
|---|---|---|---|---|---|
| Requirements covered by passed tests | % | >95 | 80–95 | 60–80 | <60 |

---

### 4.3 Code Test Coverage

| KPI | Metric | LOW | MODERATE | HIGH | VERY HIGH |
|---|---|---|---|---|---|
| Statement Coverage | % | >95 | 80–95 | 60–80 | <60 |
| Decision Coverage | % | >95 | 80–95 | 60–80 | <60 |
| Passed Unit Tests | % | >95 | 80–95 | 60–80 | <60 |

---

### 4.4 Security – Static Analysis (Start at Cluster 6)

#### Sanitizer Findings (ASAN, LSAN, UBSAN, TSAN)

| Findings | Risk |
|---|---|
| 0 | LOW |
| <5 | MODERATE |
| 5–10 | HIGH |
| >10 | VERY HIGH |

#### CheckSec Violations (NX, PIE, CANARY, RELRO, RPATH, RUNPATH, SYMBOLS)

| Violations | Risk |
|---|---|
| 0 | LOW |
| <5 | MODERATE |
| 5–10 | HIGH |
| >10 | VERY HIGH |

---

### 4.5 Code Quality

#### Compiler Warnings

| Warnings | Risk |
|---|---|
| <5 | LOW |
| 5–10 | MODERATE |
| >10 | HIGH |
| >20 | VERY HIGH |

#### SCA Findings

- LOW: only low findings
- MODERATE: low + medium
- HIGH: high or highest present

#### HIS Source Code Metrics (NOMV, NOSECV)

- LOW: only low findings
- MODERATE: low + medium
- HIGH: high or highest present
- VERY HIGH: more than 5 high/highest

---

### 4.6 FOSS Evaluation (Only if FOSS is used)

| Risk Level | Criteria |
|---|---|
| LOW | Security risk low AND license risk low |
| MODERATE | Security OR license risk medium |
| HIGH | Security OR license risk high / critical |

---

### 4.7 Defect Management

| Defects | Risk |
|---|---|
| 0 blocker / critical / major | LOW |
| 0 but customer impact analysis required | MODERATE |
| >=1 blocker / critical / major | HIGH |
| >5 blocker / critical / major | VERY HIGH |

---

## 5. Total Component Risk Calculation

```text
if VERY_HIGH >= 1:
    COMPONENT_RISK = VERY_HIGH
else if HIGH == 1:
    COMPONENT_RISK = MODERATE
else if MODERATE >= 3:
    COMPONENT_RISK = MODERATE
else if HIGH >= 2:
    COMPONENT_RISK = HIGH
else:
    COMPONENT_RISK = LOW
```

---

## 6. SOP Release Decision

| Component Risk | SOP Decision |
|---|---|
| LOW | SOP Release acceptable |
| MODERATE | SOP Release acceptable with monitoring |
| HIGH | SOP Release only with in-depth review |
| VERY HIGH | NOT SOP compliant |

---

## 7. Output Requirements

Mandatory output fields:
- component_id
- KPI results
- total_component_risk
- SOP release decision
- rationale
- open actions

---

## 8. Auditability

- Full traceability required
- Source links mandatory
- Rationale mandatory for MODERATE, HIGH, VERY HIGH