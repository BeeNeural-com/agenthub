# Document Skeletons

Phase 1 of the structured-code-review workflow creates the deliverable folder from the shells
below. Copy each shell into the named file and replace every «placeholder». Create the
`diagrams/` and `appendix/` sub-folders. Keep the document numbering contiguous.

The category documents (`01`–`04`) all use the same shell — produce one per focus area covered.

---

## Skeleton — `00-architecture-overview.md`

```
# «System name» — Architecture Overview & Code Review

**Date:** «review cut-off date»
**Reviewer:** «reviewer or team»
**Scope:** «repositories / paths reviewed»
**Focus areas:** «e.g. performance, architecture, code quality, test coverage»

## 1. System overview

«Plain-language description of what the system does and for whom — written for a product owner,
no jargon.»

### How it works

1. «Step-by-step, plain-language walkthrough of the main flow.»

## 2. Architecture diagrams

«One line per diagram in diagrams/, each saying what it shows.»

_These diagrams are lightweight review aids — not a replacement for «the organisation's official
architecture-diagramming standard»; defer to that standard._

## 3. What the team is doing well

«Bullet list of sound practices observed in the codebase. About practices and the code, never
about individuals. Mandatory — never empty.»

## 4. Technology stack

| Layer | Technology | Version | Notes |
|---|---|---|---|
| «layer» | «tech» | «version» | «notes» |

## 5. Repository activity

«Per repository: commit volume over the review period, and the highest-churn files (from
appendix/code-hotspots.md). File-level only — no per-person data.»

| Repository | Commits (period) | Top hotspot files |
|---|---|---|
| «repo» | «n» | «file (n changes), …» |

## 6. Findings map (preview)

| Document | Category | Findings | Severity range |
|---|---|---|---|
| 01 | «category» | F-01 – F-«nn» | «range» |
```

---

## Skeleton — category document `0N-«category».md` (one per focus area)

```
# «Category name» (F-«from» – F-«to»)

**Date:** «date» | **Reviewer:** «reviewer»
**Severity range:** «e.g. Critical – High»

## Summary

| ID | Title | Severity | Area | Effort |
|---|---|---|---|---|
| F-«nn» | «title» | «severity» | «component/repo» | «S/M/L/XL» |

## [F-«nn»] «Finding title»

**Severity:** «Critical / High / Medium / Low»

**Business Impact:** «Plain-language consequence for users, cost, or delivery — first, before
technical detail.»

**Technical Summary:** «What the issue is and why, technically.»

**Evidence:**

| File | Location | Detail |
|---|---|---|
| «path» | «line(s) — only if actually read» | «what is there» |

«Quote real code where it makes the point clearer. Mark anything not directly verified.»

**Best Practice Reference:** «Standard, documentation, or principle.»

**Suggested Owner:** «Team, role, or component area — never an individual.»

**Effort Estimate:** «S / M / L / XL»

**Recommendation:** «Concrete, ordered steps. Offer a quick fix and a better fix where both
exist.»

«Repeat the [F-nn] block for each finding in this category.»
```

---

## Skeleton — `05-recommendations.md`

```
# Prioritized Recommendations & Action Plan

**Date:** «date» | **Reviewer:** «reviewer»

## Executive summary

«One to three short paragraphs: the overall state of the codebase, the balance of strengths and
risks.»

### Key numbers

- «n» Critical · «n» High · «n» Medium · «n» Low findings
- «n» strengths noted

### Top risks for the product owner

1. «Plain-language risk.»

## Effort/Impact matrix

«Place every finding in one quadrant. Impact = severity-driven; Effort = S/M/L/XL (S = low).»

- **QUICK WINS** (low effort, high impact): «F-nn, …»
- **BIG BETS** (high effort, high impact): «F-nn, …»
- **CONSIDER** (low effort, low impact): «F-nn, …»
- **STRATEGIC** (high effort, low impact): «F-nn, …»

## Action waves

### Wave 1 — «name»

| # | Finding | Action | Suggested owner (team/component) | Effort |
|---|---|---|---|---|
| 1 | F-«nn» | «action» | «team/component» | «S/M/L/XL» |

«Add waves as needed. Note dependencies between findings.»

## Findings by area

«Short table or list grouping findings under each category or repository.»

## Finding index

| ID | Title | Document | Severity | Effort | Wave |
|---|---|---|---|---|---|
| F-«nn» | «title» | «0N» | «severity» | «effort» | «wave» |

## What the team should keep doing

«The strengths from section 3 of document 00, restated as things to protect during the fixes.»
```

---

## Skeleton — `CHANGELOG.md`

```
# Changelog — «System name» Code Review

**Cut-off:** «date the reviewed code state corresponds to»
**Revision:** v1.0

«First cut: keep only the single line below.»

Initial cut — no revisions.

«Later revisions: replace the line above with the two sections below.»

## Summary of changes

| # | File | Type | Rationale |
|---|---|---|---|
| 1 | «file» | «Correction / Clarification» | «why» |

## Detailed changes

### 1. «file» — «short description»

**Was:** «previous text»
**Now:** «new text»
**Why:** «reason»
```
