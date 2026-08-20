# Research Report: Agent Hub Skills Expansion Catalog

**Author:** Agent Hub R&D (via Cursor + Agent Hub MCP)  
**Date:** 2026-08-20  
**Version:** 1.0  
**Status:** final — research only (no repo changes)  
**Confidence:** High on taxonomy and gap analysis; Medium on prioritization weights (org-specific)

---

## Executive summary

Agent Hub today ships **49 skills** across **2 bundles** (`sw-engineering-ai-augmented`, `r-and-d`) plus **5 global skills**. Coverage is deep in **ASPICE-aligned embedded C++ software engineering** and **R&D methodology**, but thin or absent in **marketing, finance, HR, sales, legal, operations, customer success, product management, DevOps/SRE, design, and general enterprise workflows**.

Industry benchmarks (Skills.sh category volumes, corporate skill libraries, enterprise agent marketplaces) show **business-function skills growing faster than pure coding skills** in 2025–2026, with regulated domains (finance, legal) carrying high per-skill value despite lower volume.

**Recommendation:** Expand Agent Hub through **department bundles** (8–15 skills each) rather than one monolithic catalog. Prioritize **P0 bundles** that complement existing strengths: Product Management, DevOps/SRE, Data & Analytics, Security (general), and Document Processing. Defer highly regulated skills (tax, legal advice, investment banking) until governance, disclaimers, and human-in-the-loop review workflows exist.

**Estimated expansion scope:** ~280–350 net-new skills across 20 department domains, of which ~60–80 are **P0 must-have** for a credible “full company Agent Hub.”

---

## 1. Background and motivation

### 1.1 Problem

Agent Hub positions itself as an **R&D department MCP** and universal skill catalog. Current content reflects CARIAD/E3 automotive software engineering heritage. Users downloading `--full` or department-specific bundles will expect skills for **their function** — not only SWE and R&D.

### 1.2 Goal

Identify **all plausible Agent Hub skills** from software development through marketing, finance, HR, legal, operations, and adjacent domains — as a **research catalog** for future bundle authoring. This document does **not** implement skills; it inventories and prioritizes candidates.

### 1.3 Research questions

1. What skills exist today in Agent Hub, and where are the gaps?
2. What skills do peer catalogs and enterprise marketplaces offer by department?
3. How should new skills be grouped into bundles without duplicating global/R&D/SWE content?
4. Which skills are safe for autonomous agents vs require human review?

---

## 2. Methodology

Research followed Agent Hub **`r-and-d-workflow`** and **`research-report`** structure:

| Step | Agent Hub skill / tool | Action |
|------|------------------------|--------|
| 1 | `list_skills`, `list_bundles`, `list_agents` (MCP) | Baseline inventory of 49 skills, 2 bundles, 21 agents |
| 2 | `technology-scouting` | Survey external catalogs and marketplace patterns |
| 3 | `literature-review` | Cross-reference open skill libraries (corporate, role-based) |
| 4 | Gap analysis | Map current → proposed by department |
| 5 | `trade-study` (lightweight) | Prioritize bundles by value, overlap, governance risk |

**External sources consulted:**

- Skills.sh category volumes (Agent Skills Ecosystem Report 2026)
- [awesome-claude-corporate-skills](https://github.com/ununununium/awesome-claude-corporate-skills) — 166 skills, 14 corporate categories
- [skill-library](https://github.com/wangzaiwang-hub/skill-library) — 418 skills, 31 plugins, 54 roles
- Enterprise internal marketplace patterns (Wavect, Tata Elxsi annual report references)
- Anthropic Team/Enterprise stock plugins (finance, legal, HR — Feb 2026)

---

## 3. Current Agent Hub inventory

### 3.1 Summary

| Layer | Skills | Agents | Rules | Prompts |
|-------|--------|--------|-------|---------|
| **Global** | 5 | 14 | 3 | 2 |
| **sw-engineering-ai-augmented** | 32 | 9 | 27 | 0 |
| **r-and-d** | 13 | 4 | 3 | 2 |
| **Total (deduplicated)** | **49** | **21** | **32** | **4** |

### 3.2 Global skills (cross-cutting)

| ID | Domain | Notes |
|----|--------|-------|
| `software-engineer` | SWE general | Code style, workflow |
| `structured-code-review` | SWE audit | Multi-doc architecture review |
| `write-epics` | Product / Agile | Jira epics |
| `write-user-stories` | Product / Agile | Jira stories from epics |
| `some-skill` | Meta | Authoring template |

### 3.3 SW Engineering bundle — strength areas

Already covered in depth:

- ASPICE V-Model (SWE.1–SWE.6): requirements, architecture, detailed design, unit/integration/qualification testing
- C++ platform patterns: callbacks, mocking, tail arrays, UDS, POSIX shm, Parasoft rules
- Traceability, quality summarization, cross-model review
- SAFe/PI-adjacent agents: `pi-planner`, `atlassian-pi-planning`

**Implicit domain:** Automotive embedded / E3 platform (HCP5, VLAN K-matrix, SOP risk).

### 3.4 R&D bundle — strength areas

| Skill | Purpose |
|-------|---------|
| `r-and-d-workflow` | Pipeline orchestration |
| `technology-scouting` | Vendor/tech evaluation |
| `literature-review` | Prior work synthesis |
| `feasibility-study` | Go/no-go |
| `trade-study` | Weighted decision analysis |
| `innovation-ideation` | TRL-scored ideation |
| `experiment-design` | Hypothesis / controls |
| `data-analysis` | R&D experiment interpretation |
| `prototype-spike` | Time-boxed PoC |
| `research-report` | Stakeholder report structure |
| `research-to-requirements` | Handoff to SWE.1 |
| `prior-art-search` | Patent/publication search (non-legal) |
| `ip-landscape` | IP mapping (non-legal) |

### 3.5 Agents without matching skill depth

Several agents exist globally but lack dedicated skill libraries:

| Agent | Gap |
|-------|-----|
| `python-developer` | No Python-specific skill (typing, pytest, FastAPI, etc.) |
| `security-code-reviewer` | Partial overlap with SWE; no OWASP/threat-model skill |
| `it-security-assessment` | Draft only; no CAIS/assessment skill |
| `consultant` | Relies on R&D skills; no general consulting skill |
| `function-owner` | No product discovery / stakeholder skill |

---

## 4. Industry taxonomy — skills by department

Benchmark catalogs organize skills into **12–31 domains**. Consolidated taxonomy for Agent Hub expansion:

| # | Department / domain | Benchmark skill count (indicative) | Skills.sh growth signal |
|---|---------------------|-------------------------------------|-------------------------|
| 1 | Software Engineering & IT | 45–80 | High volume, mature |
| 2 | DevOps / SRE / Cloud | 17–25 | High |
| 3 | QA & Testing (general) | 14–20 | Medium |
| 4 | Product Management | 17–25 | **Fastest-growing business function** |
| 5 | R&D & Innovation | 13–20 | Covered (Agent Hub strength) |
| 6 | Data & Analytics | 17–25 | High |
| 7 | AI Operations & MLOps | 13–18 | Emerging |
| 8 | Security (AppSec, GRC) | 15–22 | High value |
| 9 | Design & UX | 11–18 | Medium |
| 10 | Marketing & Growth | 13–20 | **Fast-growing** |
| 11 | Sales & Revenue | 13–20 | High |
| 12 | Customer Success & Support | 20–25 | Medium |
| 13 | Finance & FP&A | 15–45 | Regulated, high value |
| 14 | HR & People Ops | 15–20 | Medium |
| 15 | Legal & Compliance | 12–20 | Regulated, high value |
| 16 | Operations & ITSM | 15–25 | Medium |
| 17 | Program / Portfolio Mgmt | 11–15 | Medium |
| 18 | Procurement & Supply Chain | 11–20 | Medium |
| 19 | Strategy & Executive | 12–20 | Medium |
| 20 | Communications | 14–18 | Medium |
| 21 | Partnerships & Alliances | 11 | Niche |
| 22 | Risk Management | 11 | Cross-cutting |
| 23 | Sustainability / ESG | 9 | Emerging |
| 24 | Document Processing | 4–8 | **Enabler for all departments** |
| 25 | Meta (skill authoring) | 1–5 | Required for scale |

---

## 5. Proposed skills catalog by domain

Each subsection lists **candidate skill IDs** (kebab-case, Agent Hub convention), **priority** (P0 = must for v1 department bundle, P1 = should, P2 = nice), and **notes** on overlap with existing content.

Legend: ✅ = already in Agent Hub | 🔶 = partial overlap | ⬜ = net new

---

### 5.1 Software Engineering (general — beyond ASPICE/C++)

*Bundle candidate: `software-engineering-general` or extend global*

| Skill ID | Priority | Status | Description |
|----------|----------|--------|-------------|
| `code-review` | P0 | 🔶 | PR-level review (distinct from `structured-code-review` repo audit) |
| `test-driven-development` | P0 | ⬜ | Red-green-refactor workflow |
| `testing-strategy` | P0 | 🔶 | General test pyramid (SWE bundle is ASPICE-specific) |
| `system-design` | P0 | ⬜ | General distributed systems design |
| `software-architecture` | P0 | 🔶 | SOLID, patterns (complement `architecture-design`) |
| `api-design` | P0 | ⬜ | REST/GraphQL/gRPC conventions |
| `database-design` | P1 | ⬜ | Schema, indexing, migrations |
| `refactor-plan` | P1 | ⬜ | Safe refactoring strategy |
| `tech-debt-assessment` | P1 | ⬜ | Prioritized debt backlog |
| `legacy-code-assessment` | P1 | ⬜ | Strangler fig, migration |
| `microservices-decomposition` | P1 | ⬜ | Service boundary analysis |
| `monorepo-strategy` | P2 | ⬜ | Mono vs polyrepo |
| `feature-flag-plan` | P2 | ⬜ | Rollout and kill switches |
| `changelog-generator` | P1 | ⬜ | User-facing release notes |
| `technical-rfc` | P1 | ⬜ | RFC / ADR authoring |
| `decision-record` | P1 | ⬜ | Architecture decision records |
| `dependency-audit` | P1 | ⬜ | Supply chain / CVE triage |
| `performance-profiling` | P1 | ⬜ | Profiling methodology |
| `i18n-strategy` | P2 | ⬜ | Localization planning |
| `accessibility-implementation` | P1 | ⬜ | WCAG implementation patterns |

**Language-specific extensions (P1–P2):**

| Skill ID | Language / stack |
|----------|------------------|
| `python-development` | Python — types, pytest, packaging (pairs with `python-developer` agent) |
| `typescript-development` | TS/Node — strict mode, testing |
| `react-development` | React — components, hooks, a11y |
| `go-development` | Go — idioms, concurrency |
| `rust-development` | Rust — ownership, async |
| `java-development` | Spring / enterprise Java |
| `mobile-ios-development` | Swift/SwiftUI |
| `mobile-android-development` | Kotlin/Jetpack |
| `flutter-development` | Cross-platform mobile |

**Estimated net new:** ~25–35 skills (P0: ~8)

---

### 5.2 DevOps, SRE & Cloud

*Bundle candidate: `devops-sre`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `ci-cd-pipeline` | P0 | Pipeline design, gates, artifacts |
| `deployment-strategy` | P0 | Blue/green, canary, rolling |
| `incident-response-runbook` | P0 | On-call, comms, mitigation |
| `incident-postmortem` | P0 | Blameless postmortem (also Operations) |
| `slo-sli-tracking` | P0 | Error budgets, alerting |
| `monitoring-setup` | P0 | Metrics, logs, traces |
| `observability-design` | P1 | OpenTelemetry, dashboards |
| `chaos-engineering` | P1 | Game days, fault injection |
| `disaster-recovery` | P1 | RTO/RPO, failover |
| `cloud-cost-review` | P1 | FinOps optimization |
| `container-strategy` | P1 | Docker/K8s patterns |
| `gitops-review` | P2 | ArgoCD/Flux workflows |
| `infrastructure-as-code` | P1 | Terraform/Pulumi review |
| `secrets-management` | P0 | Vault, rotation, scanning |
| `rollback-plan` | P1 | Safe rollback procedures |
| `service-catalog` | P2 | Internal developer portal |
| `on-call-handoff` | P1 | Shift handoff template |
| `capacity-planning` | P1 | Load forecasting |

**Estimated net new:** ~18 skills (P0: ~7)

---

### 5.3 QA & Testing (general)

*Bundle candidate: merge into `software-engineering-general` or standalone `qa-testing`*

| Skill ID | Priority | Overlap |
|----------|----------|---------|
| `test-plan` | P0 | 🔶 SWE bundle has ASPICE-specific specs |
| `exploratory-testing` | P1 | ⬜ |
| `test-automation-strategy` | P0 | ⬜ |
| `accessibility-testing` | P1 | ⬜ |
| `load-testing` | P1 | ⬜ |
| `security-testing` | P1 | ⬜ |
| `mobile-testing` | P2 | ⬜ |
| `api-test-plan` | P1 | ⬜ |
| `regression-checklist` | P1 | ⬜ |
| `release-signoff` | P1 | ⬜ |
| `bug-report-triage` | P0 | ⬜ |

**Estimated net new:** ~12 skills (P0: ~3)

---

### 5.4 Product Management

*Bundle candidate: `product-management`*

| Skill ID | Priority | Status |
|----------|----------|--------|
| `prd-writer` | P0 | ⬜ |
| `feature-spec` | P0 | ⬜ |
| `roadmap-builder` | P0 | ⬜ |
| `feature-prioritization` | P0 | ⬜ RICE, MoSCoW, Kano |
| `user-research-synthesis` | P0 | ⬜ |
| `product-discovery` | P0 | ⬜ Problem interviews, assumptions |
| `go-to-market` | P1 | ⬜ |
| `product-launch-playbook` | P1 | ⬜ |
| `beta-program` | P2 | ⬜ |
| `ab-test-plan` | P1 | ⬜ |
| `product-analytics` | P1 | ⬜ |
| `competitive-product-brief` | P1 | 🔶 overlaps `technology-scouting` |
| `stakeholder-update` | P1 | ⬜ |
| `sprint-planning` | P0 | 🔶 `pi-planner` agent exists |
| `metrics-review` | P1 | ⬜ |
| `release-notes-product` | P1 | ⬜ |
| `user-story-mapping` | P1 | 🔶 `write-user-stories` is Jira-specific |

**Estimated net new:** ~17 skills (P0: ~7)

---

### 5.5 R&D & Innovation (extensions)

*Extend existing `r-and-d` bundle*

| Skill ID | Priority | Status |
|----------|----------|--------|
| `benchmark-design` | P1 | ⬜ Standardized perf benchmarks |
| `survey-design` | P2 | ⬜ User/market surveys |
| `meta-analysis` | P2 | ⬜ Research synthesis stats |
| `grant-proposal` | P2 | ⬜ Funding applications |
| `research-ethics-checklist` | P1 | 🔶 rule exists; skill for procedure |
| `technology-readiness-assessment` | P1 | 🔶 part of `innovation-ideation` |
| `vendor-proof-of-concept` | P1 | ⬜ Structured vendor PoC |
| `standards-tracking` | P1 | ⬜ ISO, IEEE, industry standards |
| `regulatory-horizon-scan` | P2 | ⬜ Non-legal regulatory watch |

**Estimated net new:** ~8 skills (P0: 0 — bundle already strong)

---

### 5.6 Data & Analytics

*Bundle candidate: `data-analytics`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `sql-query-review` | P0 | Safe SQL generation/review |
| `data-exploration` | P0 | EDA workflow |
| `statistical-analysis` | P0 | 🔶 overlaps R&D `data-analysis` — generalize |
| `dashboard-design` | P0 | KPI dashboard specs |
| `kpi-definition` | P0 | Metric hierarchy |
| `data-visualization` | P1 | Chart selection, integrity |
| `data-quality-assessment` | P1 | Profiling, anomalies |
| `data-governance` | P1 | Lineage, catalog, ownership |
| `cohort-analysis` | P1 | Retention, LTV |
| `funnel-analysis` | P1 | Conversion diagnostics |
| `attribution-modeling` | P2 | Marketing/sales attribution |
| `predictive-analytics` | P2 | Forecasting overview |
| `experiment-readout` | P1 | A/B test interpretation |
| `data-storytelling` | P1 | Narrative for stakeholders |
| `dbt-model-review` | P2 | Analytics engineering |

**Estimated net new:** ~15 skills (P0: ~5)

---

### 5.7 AI Operations & MLOps

*Bundle candidate: `ai-operations`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `prompt-engineering` | P0 | System prompt design, eval |
| `prompt-evaluation` | P0 | Test sets, regression |
| `rag-pipeline-design` | P0 | Chunking, retrieval, rerank |
| `model-selection` | P1 | Cost/latency/quality tradeoffs |
| `llm-risk-review` | P0 | Safety, bias, leakage |
| `agent-workflow-design` | P0 | Multi-step agent orchestration |
| `mcp-server-design` | P1 | MCP tool/resource design |
| `fine-tuning-plan` | P2 | When to fine-tune vs RAG |
| `model-monitoring` | P1 | Drift, quality in production |
| `synthetic-data-review` | P2 | Quality gates |
| `ai-governance` | P1 | Policy, approval tiers |
| `workflow-automation-review` | P2 | n8n/Zapier agent flows |

**Estimated net new:** ~12 skills (P0: ~5)

---

### 5.8 Security (AppSec, GRC, beyond code review)

*Bundle candidate: `security`*

| Skill ID | Priority | Status |
|----------|----------|--------|
| `threat-modeling` | P0 | STRIDE, attack trees |
| `owasp-top10-review` | P0 | 🔶 `security-code-reviewer` agent |
| `secrets-scanning` | P0 | ⬜ |
| `security-architecture-review` | P1 | ⬜ |
| `cloud-security-review` | P1 | ⬜ |
| `zero-trust-assessment` | P2 | ⬜ |
| `pen-test-plan` | P2 | ⬜ |
| `vulnerability-triage` | P0 | ⬜ CVE prioritization |
| `security-incident-response` | P1 | ⬜ |
| `third-party-risk-review` | P1 | ⬜ Vendor security |
| `compliance-audit-prep` | P2 | SOC2, ISO27001 |
| `privacy-impact-assessment` | P1 | ⬜ DPIA workflow |
| `security-awareness-content` | P2 | Training material |

**Estimated net new:** ~13 skills (P0: ~4)

---

### 5.9 Design & UX

*Bundle candidate: `design-ux`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `design-critique` | P0 | Structured critique |
| `wireframe-review` | P1 | IA, flows |
| `design-system-audit` | P1 | Token, component consistency |
| `accessibility-review-ux` | P0 | WCAG from design |
| `usability-test-plan` | P1 | Moderated/unmoderated |
| `user-interview-guide` | P1 | Script, synthesis |
| `ux-copy-review` | P1 | Microcopy, tone |
| `design-handoff` | P1 | Specs for engineering |
| `design-sprint` | P2 | Facilitation |
| `motion-design-spec` | P2 | Animation specs |
| `heuristic-evaluation` | P1 | Nielsen heuristics |

**Estimated net new:** ~11 skills (P0: ~2)

---

### 5.10 Marketing & Growth

*Bundle candidate: `marketing`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `campaign-plan` | P0 | End-to-end campaign |
| `content-marketing` | P0 | Blog, whitepaper workflow |
| `content-calendar` | P1 | Editorial planning |
| `seo-audit` | P0 | Technical + content SEO |
| `seo-content-optimization` | P0 | On-page optimization |
| `email-marketing` | P0 | Sequences, compliance (CAN-SPAM/GDPR) |
| `social-media-strategy` | P1 | Platform-specific plans |
| `paid-media-plan` | P1 | Budget, channels, creatives |
| `brand-messaging` | P1 | Voice, positioning |
| `brand-guidelines` | P2 | Visual/verbal standards |
| `landing-page-copy` | P0 | Conversion-focused copy |
| `conversion-optimization` | P1 | CRO experiments |
| `marketing-analytics` | P1 | Channel ROI |
| `competitor-marketing-analysis` | P1 | 🔶 overlaps scouting |
| `influencer-strategy` | P2 | Partnership outreach |
| `market-research` | P1 | Sizing, personas |
| `product-marketing-launch` | P1 | PMM launch kit |

**Estimated net new:** ~17 skills (P0: ~6)

---

### 5.11 Sales & Revenue

*Bundle candidate: `sales`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `discovery-call-prep` | P0 | Questions, hypothesis |
| `account-research` | P0 | Account intelligence |
| `call-prep` | P0 | Meeting brief |
| `draft-outreach` | P0 | Cold/warm email |
| `proposal-draft` | P1 | SOW, pricing narrative |
| `competitive-battlecard` | P0 | vs competitor talk tracks |
| `objection-handling` | P1 | Response frameworks |
| `demo-prep` | P1 | Demo storyline |
| `pipeline-review` | P1 | Forecast hygiene |
| `sales-forecast` | P2 | ⬜ Requires CRM context |
| `territory-plan` | P2 | ⬜ |
| `win-loss-analysis` | P1 | Post-deal review |
| `pricing-strategy` | P1 | Packaging, discount guardrails |
| `sales-enablement` | P2 | One-pagers, training |
| `renewal-risk` | P1 | Expansion/churn signals |
| `lead-qualification` | P0 | BANT/MEDDIC frameworks |

**Estimated net new:** ~16 skills (P0: ~6)

---

### 5.12 Customer Success & Support

*Bundle candidate: `customer-success`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `ticket-triage` | P0 | Routing, priority |
| `support-response-draft` | P0 | Empathetic replies |
| `kb-article-writer` | P0 | Help center content |
| `csat-analysis` | P1 | Survey interpretation |
| `qbr-prep` | P0 | Quarterly business review |
| `customer-health-score` | P1 | Risk indicators |
| `churn-analysis` | P0 | Retention playbook |
| `onboarding-playbook` | P1 | Time-to-value |
| `escalation-management` | P1 | Severity, comms |
| `customer-research` | P1 | Interview synthesis |
| `renewal-plan` | P1 | Expansion strategy |
| `customer-advocacy` | P2 | Case study, reference |

*Support sub-bundle:*

| Skill ID | Priority |
|----------|----------|
| `chatbot-intent-design` | P1 |
| `self-service-optimization` | P2 |
| `support-metrics-review` | P1 |

**Estimated net new:** ~15 skills (P0: ~5)

---

### 5.13 Finance & Accounting

*Bundle candidate: `finance`* — **high governance tier**

| Skill ID | Priority | Risk tier | Description |
|----------|----------|-----------|-------------|
| `budget-plan` | P0 | Medium | Annual/quarterly budgets |
| `financial-forecast` | P0 | Medium | Rolling forecasts |
| `variance-analysis` | P0 | Medium | Budget vs actual |
| `unit-economics` | P0 | Medium | CAC, LTV, margins |
| `cash-flow-review` | P1 | Medium | Liquidity |
| `cost-optimization` | P1 | Low | OpEx review |
| `financial-modeling` | P1 | **High** | Generic 3-statement |
| `dcf-model` | P2 | **High** | Valuation — disclaimer required |
| `investment-analysis` | P2 | **High** | Not investment advice |
| `expense-review` | P1 | Low | T&E, policy |
| `invoice-processing` | P1 | Low | AP workflow |
| `audit-preparation` | P2 | Medium | Control evidence |
| `tax-planning-overview` | P2 | **High** | Not tax advice |
| `pricing-model` | P1 | Medium | SaaS pricing |
| `revenue-analysis` | P1 | Medium | ARR, churn finance view |
| `financial-report-narrative` | P1 | Medium | MD&A style |
| `scenario-planning-finance` | P1 | Medium | Sensitivity tables |

**IB/PE-specific (P2, optional sub-bundle `finance-capital-markets`):**  
`comps-analysis`, `lbo-model`, `merger-model`, `pitch-deck`, `cim-builder`, `ic-memo` — 20+ skills from corporate catalogs; require **strict human review** and jurisdiction disclaimers.

**Estimated net new:** ~15 core + ~20 optional capital-markets (P0: ~4)

---

### 5.14 Human Resources & People Ops

*Bundle candidate: `human-resources`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `job-description-writer` | P0 | Inclusive JDs |
| `interview-kit-builder` | P0 | Structured interviews |
| `interview-scorecard` | P0 | Rubrics |
| `onboarding-plan` | P0 | 30-60-90 |
| `performance-review` | P1 | Calibration guidance |
| `compensation-benchmarking` | P2 | Pay equity — data sensitive |
| `employee-engagement-survey` | P1 | Design + analysis |
| `workforce-planning` | P1 | Headcount modeling |
| `succession-planning` | P2 | ⬜ |
| `dei-program-design` | P2 | ⬜ |
| `exit-interview` | P2 | ⬜ |
| `policy-drafting` | P2 | HR policy — legal review |
| `offer-letter-draft` | P2 | Legal review required |
| `learning-path-design` | P1 | Pairs with L&D bundle |

**Estimated net new:** ~14 skills (P0: ~4)

---

### 5.15 Legal & Compliance

*Bundle candidate: `legal-compliance`* — **highest governance tier**

| Skill ID | Priority | Risk | Description |
|----------|----------|------|-------------|
| `contract-review-checklist` | P0 | High | Clause checklist — **not legal advice** |
| `nda-triage` | P0 | High | Standard vs non-standard |
| `legal-risk-assessment` | P1 | High | Issue spotting |
| `compliance-tracking` | P1 | Medium | Obligation calendar |
| `privacy-policy-review` | P2 | High | GDPR/CCPA checklist |
| `dpa-review` | P2 | High | Data processing agreements |
| `terms-of-service-review` | P2 | High | |
| `regulatory-tracking` | P1 | Medium | Horizon scanning |
| `ip-review-checklist` | P1 | High | 🔶 complements `prior-art-search` |
| `license-review` | P2 | Medium | OSS/commercial |
| `litigation-hold-notice` | P2 | High | Template only |
| `corporate-governance-checklist` | P2 | High | Board materials |

**Estimated net new:** ~12 skills (P0: ~2 with disclaimers)

---

### 5.16 Operations & ITSM

*Bundle candidate: `operations`*

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `sop-builder` | P0 | Standard operating procedures |
| `process-optimization` | P0 | Lean, value stream |
| `business-case` | P0 | ROI, NPV narrative |
| `status-report` | P0 | RAG project reports |
| `okr-tracking` | P1 | OKR check-ins |
| `resource-planning` | P1 | Capacity allocation |
| `vendor-management` | P1 | SLA, performance |
| `sla-review` | P1 | Breach analysis |
| `workflow-design` | P1 | BPMN-level |
| `change-request` | P1 | CAB-ready CR |
| `kaizen-event` | P2 | Continuous improvement |
| `runbook-operations` | P1 | Non-technical runbooks |

*ITSM sub-skills (pairs with `devops-sre`):*

| Skill ID | Priority |
|----------|----------|
| `incident-management-itsm` | P1 |
| `problem-management` | P1 |
| `change-management-itsm` | P1 |
| `service-catalog-design` | P2 |

**Estimated net new:** ~16 skills (P0: ~4)

---

### 5.17 Program & Portfolio Management

*Bundle candidate: `program-management`*

| Skill ID | Priority |
|----------|----------|
| `raid-log` | P0 |
| `stakeholder-analysis` | P0 |
| `program-status-report` | P0 |
| `dependency-mapping` | P1 |
| `benefits-realization` | P1 |
| `lessons-learned` | P1 |
| `portfolio-governance` | P2 |
| `steerco-update` | P1 |
| `milestone-review` | P1 |
| `resource-allocation` | P1 |

**Estimated net new:** ~10 skills (P0: ~3)

---

### 5.18 Procurement & Supply Chain

*Bundle candidate: `procurement-supply-chain`*

| Skill ID | Priority |
|----------|----------|
| `rfp-draft` | P0 |
| `vendor-evaluation` | P0 | 🔶 overlaps scouting |
| `supplier-scorecard` | P1 |
| `spend-analysis` | P1 |
| `contract-negotiation-prep` | P1 |
| `procurement-compliance` | P2 |
| `demand-planning` | P2 |
| `inventory-optimization` | P2 |
| `logistics-review` | P2 |
| `supply-chain-risk` | P2 |

**Estimated net new:** ~10 skills (P0: ~2)

---

### 5.19 Strategy & Executive

*Bundle candidate: `strategy-executive`*

| Skill ID | Priority |
|----------|----------|
| `strategic-planning` | P0 | OKR, SWOT |
| `swot-analysis` | P0 |
| `business-model-canvas` | P1 |
| `competitive-landscape` | P0 | 🔶 overlaps scouting |
| `growth-strategy` | P1 |
| `market-entry-analysis` | P2 |
| `digital-transformation-roadmap` | P1 |
| `strategic-scenario-planning` | P2 |
| `board-meeting-prep` | P2 |
| `executive-briefing` | P1 |
| `ma-due-diligence-checklist` | P2 | High risk |
| `kpi-executive-dashboard` | P1 |

**Estimated net new:** ~12 skills (P0: ~3)

---

### 5.20 Communications

*Bundle candidate: `communications`*

| Skill ID | Priority |
|----------|----------|
| `internal-comms` | P0 |
| `executive-email` | P1 |
| `press-release` | P1 |
| `crisis-comms` | P1 |
| `change-communication` | P1 |
| `town-hall-script` | P2 |
| `newsletter` | P2 |
| `presentation-outline` | P1 |
| `stakeholder-messaging` | P1 |
| `meeting-agenda` | P1 |

**Estimated net new:** ~10 skills (P0: ~1)

---

### 5.21 Partnerships, Risk, Sustainability (cross-cutting)

**Partnerships (`partnerships`):**  
`partner-evaluation`, `channel-strategy`, `co-marketing-brief`, `integration-readiness`, `partner-qbr` — ~8 skills, P1–P2

**Risk Management (`risk-management`):**  
`risk-register`, `risk-assessment`, `bcp-plan`, `crisis-simulation`, `third-party-risk`, `fraud-risk` — ~10 skills, P1

**Sustainability (`sustainability`):**  
`esg-report`, `carbon-footprint`, `sustainability-strategy`, `dei-reporting` — ~9 skills, P2

---

### 5.22 Document Processing (enabler bundle)

*Bundle candidate: `document-processing`* — high leverage for all departments

| Skill ID | Priority | Description |
|----------|----------|-------------|
| `docx-authoring` | P0 | Word create/edit |
| `xlsx-analysis` | P0 | Spreadsheet formulas, charts |
| `pptx-generation` | P0 | Slide decks |
| `pdf-extraction` | P0 | Tables, text, merge |
| `markdown-to-deck` | P1 | Report → slides |
| `csv-insights` | P1 | Quick analysis |

**Estimated net new:** ~6 skills (P0: ~4) — enables finance, marketing, executive workflows

---

### 5.23 Meta & Authoring

| Skill ID | Priority | Status |
|----------|----------|--------|
| `skill-authoring` | P0 | 🔶 `some-skill` template |
| `agent-authoring` | P1 | ⬜ |
| `rule-authoring` | P1 | ⬜ |
| `bundle-manifest-authoring` | P1 | ⬜ |
| `skill-quality-review` | P1 | ⬜ Lint, description, triggers |

**Estimated net new:** ~4 skills (P0: ~1 upgrade of template)

---

## 6. Gap summary — current vs proposed

| Domain | Current skills | Proposed P0 | Proposed total | Coverage today |
|--------|----------------|-------------|----------------|----------------|
| SWE (ASPICE/C++) | ~37 | — | +25 general | **Strong (niche)** |
| R&D | 13 | — | +8 | **Strong** |
| Product | 2 (epics/stories) | 7 | 17 | **Weak** |
| DevOps/SRE | 0 | 7 | 18 | **None** |
| QA (general) | 0 | 3 | 12 | **None** |
| Data & Analytics | 1 (R&D overlap) | 5 | 15 | **Weak** |
| AI Ops | 0 | 5 | 12 | **None** |
| Security (general) | 1 (agent) | 4 | 13 | **Weak** |
| Design/UX | 0 | 2 | 11 | **None** |
| Marketing | 0 | 6 | 17 | **None** |
| Sales | 0 | 6 | 16 | **None** |
| Customer Success | 0 | 5 | 15 | **None** |
| Finance | 0 | 4 | 15–35 | **None** |
| HR | 0 | 4 | 14 | **None** |
| Legal | 0 | 2 | 12 | **None** |
| Operations | 0 | 4 | 16 | **None** |
| Program Mgmt | 2 (PI agents) | 3 | 10 | **Weak** |
| Procurement/SC | 0 | 2 | 10 | **None** |
| Strategy/Executive | 0 | 3 | 12 | **None** |
| Communications | 0 | 1 | 10 | **None** |
| Document Processing | 0 | 4 | 6 | **None** |
| Meta | 1 | 1 | 4 | Template only |
| **Total** | **49** | **~76 P0** | **~280–350** | |

---

## 7. Recommended bundle architecture

Proposed bundles avoid duplicating global/R&D/SWE content. Bundles compose via `AGENTHUB_BUNDLE` comma list.

```
global/                          # Cross-cutting (expand slowly)
├── software-engineer
├── write-epics / write-user-stories
├── structured-code-review
└── skill-authoring

bundles/
├── sw-engineering-ai-augmented/ # Keep — automotive ASPICE (existing)
├── r-and-d/                     # Keep — extend lightly (existing)
├── software-engineering-general/ # NEW — language-agnostic SWE
├── devops-sre/                  # NEW
├── product-management/          # NEW
├── data-analytics/              # NEW
├── ai-operations/               # NEW
├── security/                    # NEW
├── marketing/                   # NEW
├── sales/                       # NEW
├── customer-success/            # NEW
├── finance/                     # NEW (governed)
├── human-resources/             # NEW
├── legal-compliance/            # NEW (governed)
├── operations/                  # NEW
├── program-management/          # NEW
├── design-ux/                   # NEW
├── document-processing/         # NEW (enabler)
├── communications/              # NEW
├── strategy-executive/          # NEW
├── procurement-supply-chain/    # NEW (P2)
├── risk-management/             # NEW (P2)
└── sustainability/              # NEW (P2)
```

### 7.1 Download presets (user-facing)

| User profile | Suggested install |
|--------------|-------------------|
| Full company | `--full` |
| Engineering org | `--bundle sw-engineering-ai-augmented,software-engineering-general,devops-sre,security` |
| R&D department | `--bundle r-and-d,data-analytics` |
| Go-to-market team | `--bundle product-management,marketing,sales,customer-success` |
| Back office | `--bundle finance,human-resources,legal-compliance,operations` |
| Single skill | `--skill campaign-plan` |

---

## 8. Prioritization — phased rollout

### Phase 0 (already shipped)

- `sw-engineering-ai-augmented`, `r-and-d`, global agile skills

### Phase 1 — P0 bundles (highest ROI, lowest regulatory risk)

| Bundle | P0 skills | Rationale |
|--------|-----------|-----------|
| `document-processing` | 4 | Unblocks all departments |
| `product-management` | 7 | Complements epics/stories; high demand |
| `devops-sre` | 7 | Natural extension of SWE users |
| `software-engineering-general` | 8 | Python/TS/web — broadens beyond C++ |
| `ai-operations` | 5 | Agent Hub product alignment |
| `data-analytics` | 5 | Shared with R&D and product |
| `security` | 4 | Pairs with `security-code-reviewer` |
| `meta: skill-authoring` | 1 | Scale authoring |

**Phase 1 total:** ~41 P0 skills

### Phase 2 — Revenue & customer functions

| Bundle | P0 skills |
|--------|-----------|
| `marketing` | 6 |
| `sales` | 6 |
| `customer-success` | 5 |

**Phase 2 total:** ~17 P0 skills

### Phase 3 — Business operations (governed)

| Bundle | P0 skills | Governance |
|--------|-----------|------------|
| `finance` | 4 | Medium — disclaimers, no advice |
| `human-resources` | 4 | Medium — PII sensitivity |
| `operations` | 4 | Low |
| `program-management` | 3 | Low |
| `legal-compliance` | 2 | **High** — checklist only, not legal advice |

**Phase 3 total:** ~17 P0 skills

### Phase 4 — Executive & niche

- `strategy-executive`, `communications`, `design-ux`, `procurement-supply-chain`, `risk-management`, `sustainability`, `finance-capital-markets` (optional)

---

## 9. Governance & risk tiers

Skills must declare a **risk tier** in `manifest.yaml` for marketplace/certification workflows (per enterprise agent marketplace research).

| Tier | Autonomy | Examples | Required controls |
|------|----------|----------|-------------------|
| **T0 — Safe** | Full auto | `changelog-generator`, `meeting-agenda`, `sop-builder` | Standard QA |
| **T1 — Review recommended** | Auto + human spot-check | `prd-writer`, `campaign-plan`, `code-review` | Owner sign-off |
| **T2 — Sensitive data** | Restricted context | `compensation-benchmarking`, `financial-forecast` | No PII in prompts; audit log |
| **T3 — Regulated / advice-adjacent** | Human-in-the-loop mandatory | `contract-review-checklist`, `dcf-model`, `tax-planning-overview` | Disclaimers, legal/finance review, jurisdiction tags |
| **T4 — Prohibited autonomous** | Agent must refuse final action | Binding legal advice, tax filing, medical diagnosis | Block or escalate only |

Existing R&D skills `prior-art-search` and `ip-landscape` already follow T3 (non-legal disclaimer). Same pattern required for legal/finance expansions.

---

## 10. Agent ↔ skill pairing recommendations

New bundles should ship with **role agents** (pattern from existing 21 agents):

| Proposed agent | Bundle | Key skills |
|----------------|--------|------------|
| `product-manager` | product-management | prd, roadmap, prioritization |
| `devops-engineer` | devops-sre | ci-cd, incident, SLO |
| `data-analyst` | data-analytics | sql, dashboard, KPI |
| `ml-engineer` | ai-operations | RAG, prompt-eval, model selection |
| `marketing-manager` | marketing | campaign, SEO, content |
| `account-executive` | sales | discovery, outreach, battlecard |
| `customer-success-manager` | customer-success | QBR, churn, health |
| `fp-and-a-analyst` | finance | budget, forecast, variance |
| `hr-business-partner` | human-resources | JD, interview, onboarding |
| `legal-ops-analyst` | legal-compliance | contract checklist, NDA triage |
| `operations-manager` | operations | SOP, business case, status |

---

## 11. Overlap & deduplication rules

When authoring new skills, apply these rules to avoid catalog bloat:

1. **Global wins** — if a skill applies to all departments, put in `global/` (max ~10–15 total).
2. **Workflow vs reference** — workflows (`campaign-plan`) vs reference data (`aspice-bp-reference`); don't merge.
3. **Scouting vs domain research** — `technology-scouting` for tech/vendor; `market-research` for marketing personas — cross-link, don't duplicate matrices.
4. **Postmortem** — one skill (`incident-postmortem`), referenced by DevOps and Operations bundles.
5. **Data analysis** — generalize R&D `data-analysis` into `data-analytics` bundle; R&D skill becomes thin wrapper or alias.
6. **Competitive analysis** — executive `competitive-landscape`, marketing `competitor-marketing-analysis`, sales `competitive-battlecard` — same data, different output format (OK to keep separate).

---

## 12. Open questions

1. **Industry verticals** — Should automotive-specific content stay in SWE bundle while general content grows separately? (Recommended: yes.)
2. **Localization** — German/English skill variants for CARIAD/EU compliance?
3. **Certification** — Internal marketplace approval per bundle before `--full` includes finance/legal?
4. **TypeScript parity** — Mirror top 50 skills in `@agenthub/sdk` for npm consumers?
5. **Community contributions** — Accept external skills PRs with manifest schema validation?
6. **Skill size cap** — Max SKILL.md length before splitting into `references/`? (Current SWE skills set precedent.)

---

## 13. Conclusion

Agent Hub has a **world-class foundation** in ASPICE software engineering and R&D methodology. To become a **company-wide Agent Hub**, the catalog should grow from **49 → ~300 skills** across **15–20 department bundles**, phased by governance risk and user demand.

**Immediate research-complete next steps** (for product/engineering, not this doc):

1. Author Phase 1 bundles (`document-processing`, `product-management`, `devops-sre`, `ai-operations`)
2. Add `riskTier` field to `manifest.yaml` schema
3. Publish bundle preset table in product requirements doc
4. Create `skill-authoring` skill (upgrade `some-skill` template)

---

## References

1. Agent Hub MCP — `list_skills`, `list_bundles`, `list_agents` (2026-08-20 inventory)
2. Agent Hub skills — `r-and-d-workflow`, `technology-scouting`, `research-report`, `innovation-ideation`
3. [Agent Skills Ecosystem Report 2026](https://agentman.ai/blog/agent-skills-ecosystem-report-2026) — category volumes, MCP adoption
4. [awesome-claude-corporate-skills](https://github.com/ununununium/awesome-claude-corporate-skills) — 166 corporate skills, 14 categories
5. [skill-library](https://github.com/wangzaiwang-hub/skill-library) — 418 skills, 31 plugins, 54 roles
6. [Internal AI Agent Marketplace](https://wavect.io/blog/internal-ai-agent-marketplace/) — governance, certification, department rollout
7. [Agent Hub universal MCP research](./agenthub-universal-mcp-sdk.md)
8. [Agent Hub product requirements](./agenthub-product-requirements.md)

---

## Appendix A — Full P0 skill checklist (76 skills)

Quick reference for Phase 1–3 implementation backlog:

**document-processing (4):** docx-authoring, xlsx-analysis, pptx-generation, pdf-extraction

**product-management (7):** prd-writer, feature-spec, roadmap-builder, feature-prioritization, user-research-synthesis, product-discovery, sprint-planning

**devops-sre (7):** ci-cd-pipeline, deployment-strategy, incident-response-runbook, incident-postmortem, slo-sli-tracking, monitoring-setup, secrets-management

**software-engineering-general (8):** code-review, test-driven-development, testing-strategy, system-design, software-architecture, api-design, changelog-generator, technical-rfc

**ai-operations (5):** prompt-engineering, prompt-evaluation, rag-pipeline-design, llm-risk-review, agent-workflow-design

**data-analytics (5):** sql-query-review, data-exploration, statistical-analysis, dashboard-design, kpi-definition

**security (4):** threat-modeling, owasp-top10-review, secrets-scanning, vulnerability-triage

**marketing (6):** campaign-plan, content-marketing, seo-audit, seo-content-optimization, email-marketing, landing-page-copy

**sales (6):** discovery-call-prep, account-research, call-prep, draft-outreach, competitive-battlecard, lead-qualification

**customer-success (5):** ticket-triage, support-response-draft, kb-article-writer, qbr-prep, churn-analysis

**finance (4):** budget-plan, financial-forecast, variance-analysis, unit-economics

**human-resources (4):** job-description-writer, interview-kit-builder, interview-scorecard, onboarding-plan

**operations (4):** sop-builder, process-optimization, business-case, status-report

**program-management (3):** raid-log, stakeholder-analysis, program-status-report

**legal-compliance (2):** contract-review-checklist, nda-triage

**strategy-executive (3):** strategic-planning, swot-analysis, competitive-landscape

**communications (1):** internal-comms

**meta (1):** skill-authoring

**procurement (2):** rfp-draft, vendor-evaluation

---

## Appendix B — Skills.sh category benchmark (2026)

| Category | Approx. published skills |
|----------|--------------------------|
| Development & Engineering | 288,811 |
| Product Management | 86,948 |
| Marketing | 74,510 |
| Data & Analytics | 69,187 |
| Operations | 51,007 |
| Sales | 42,570 |
| Design | 25,743 |
| Legal | 17,624 |
| Finance & Accounting | 14,932 |
| Healthcare & Life Sciences | 6,354 |

*Source: Agent Skills Ecosystem Report 2026 (Skills.sh aggregates). Volumes indicate builder interest, not quality.*
