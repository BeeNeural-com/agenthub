---
name: structured-code-review
version: 1.0
description: Produce a structured, multi-document architecture and code-review deliverable for a codebase — system overview, diagrams, prioritized findings, and an action plan. Use for a thorough audit of a whole repository or system, not a quick pull-request diff review.
---

# Structured Code Review

A repeatable methodology for auditing a codebase and producing a professional,
product-owner-ready review deliverable: an architecture overview, architecture diagrams,
findings grouped by category with severity and effort ratings, and a prioritized action plan.

This skill encodes **process and structure**. It does not replace reviewer judgement, and it
does not bundle language-specific linters — run those separately and feed notable results in as
evidence.

## When to use

- A stakeholder asks for a code review, architecture review, technical due diligence, or audit
  of a whole repository or system.
- The goal is a structured written deliverable, not inline comments on a single pull request.

For a quick single-PR diff review, this skill is heavier than needed.

## Core principles (non-negotiable)

1. **No personal data, no individual metrics.** Analyse *code and systems, never people*. Do not
   extract, count, classify, or attribute work by author or committer. Do not run `git blame`,
   `git shortlog`, or `git log` with an author field (`--author`, `--format=%aN/%aE`). The
   deliverable contains no personal names, emails, or per-person statistics — neither blame nor
   praise. A finding's "Suggested Owner" is always a team, role, or component area.
   *Rationale: GDPR data-minimization and purpose-limitation; and a reusable tool that
   systematically attributes work to individuals is a behavioural-monitoring system that, in a
   co-determined workplace, requires works-council agreement before use.*
2. **Evidence integrity.** Cite only files you have actually opened. Give a line number only
   when you have read that line; otherwise cite the file or function without a fabricated
   location. Prefer quoting the real code over paraphrasing it. Mark any inference explicitly
   ("unverified", "appears to"). Never invent file paths, line numbers, identifiers, or tickets.
3. **Business impact first.** Every finding leads with plain-language impact a non-technical
   product owner can understand, before any technical detail.
4. **Work in passes; persist as you go.** Review one focus area, or one repository, at a time.
   Write each document to disk as soon as its phase is complete — never hold the whole review in
   working memory. This keeps large codebases within reach.
5. **Acknowledge strengths.** The deliverable always includes what the team is doing well —
   about practices and the codebase, never about individuals.

## Workflow — 7 phases

Run in order. Each phase writes its output to disk before the next begins.

### Phase 1 — Scope & skeleton
Confirm with the requester: which repository/paths are in scope, the focus areas to cover, the
period for hotspot analysis, and where the deliverable folder should be created. Then create the
deliverable skeleton from `document-skeletons.md`.

### Phase 2 — Architecture mapping
Read the codebase to understand it: technology stack, tiers/components, entry points, external
systems and dependencies, data stores, and how it is deployed. Write
`00-architecture-overview.md` — system overview in plain language, technology-stack table, the
"What the team is doing well" section, and a repository-activity section. The findings-map
preview is filled in at the end.

### Phase 3 — Diagram generation
Produce the architecture diagrams into `diagrams/`, using `diagram-templates.md` (fixed Mermaid
theme block + adaptive diagram set). Generate only the diagrams that fit the system.

### Phase 4 — Code-hotspot analysis
Run the file-change-frequency analysis from `code-hotspots.md` and write
`appendix/code-hotspots.md`. This is **file-level only** — see the compliance note in that file.
High-churn files are review-priority signals; reference them when choosing what to inspect. Then
complete section 5 (Repository activity) of `00-architecture-overview.md` with the results.

### Phase 5 — Finding identification
For each focus area, scan the code using that area's checklist (below) and the hotspot signal.
Document each finding with the finding template, assign the next `F-NN` id, and append it to the
matching category document (`01`–`04`). Re-run this phase once per focus area.

### Phase 6 — Rating & prioritization
With all findings recorded, write `05-recommendations.md`: executive summary, severity tally,
effort/impact matrix, action waves, findings-by-area, the finding index, and "What the team
should keep doing". Severity and effort for each finding are assigned as the finding is written
in Phase 5; this phase consolidates them.

### Phase 7 — Consistency QC pass
Run the consistency checklist (below). Fix every contradiction. Record what changed in
`CHANGELOG.md` using the "Was / Now / Why" format. On the first cut, `CHANGELOG.md` simply
records "Initial cut — no revisions".

## Deliverable structure

A folder containing:

| File / folder | Contents |
|---|---|
| `00-architecture-overview.md` | System overview, tech stack, positives, repo activity, findings-map preview |
| `01-...` to `04-...` | Findings grouped by category (see Focus areas) |
| `05-recommendations.md` | Executive summary, effort/impact matrix, action waves, finding index |
| `diagrams/` | Mermaid architecture diagrams |
| `appendix/code-hotspots.md` | File-change-frequency analysis |
| `CHANGELOG.md` | Revision record |

Documents are numbered so they read in order. Use Word-export-friendly Markdown (tables, fenced
code, no exotic syntax).

## Severity scale

| Severity | Meaning |
|---|---|
| Critical | Production-breaking or security-critical; will cause user-visible failure, data loss, or a security incident under foreseeable conditions. |
| High | Serious resilience, architecture, or correctness risk; likely to become an incident or a major maintainability drag. |
| Medium | Maintainability or quality issue, or moderate risk; should be fixed but is not urgent. |
| Low | Minor: cosmetic, polish, or low-impact gap. |

## Effort scale

| Effort | Size |
|---|---|
| S | < 1 day |
| M | 1–3 days |
| L | 3–5 days |
| XL | 1–2 weeks |

## Finding template

Each finding, in a category document, has exactly these fields in this order:

- `## [F-NN] Title` — `F-NN` is sequential and unique across the whole review.
- **Severity** — Critical / High / Medium / Low.
- **Business Impact** — plain language, for a product owner; what it means for users, cost, or
  delivery. This comes first, before technical detail.
- **Technical Summary** — what the issue is and why, technically.
- **Evidence** — a `file : line` table or quoted code. Verified references only (see Evidence
  integrity).
- **Best Practice Reference** — the standard, documentation, or principle the recommendation
  rests on.
- **Suggested Owner** — a team, role, or component area. **Never an individual.**
- **Effort Estimate** — S / M / L / XL.
- **Recommendation** — concrete, ordered steps; offer a quick fix and a better fix where both
  exist.

## Focus areas

Each focus area is one category document. Cover the areas the requester asked for; the default
set and their checklists:

### 01 — Critical & Performance
Blocking or synchronous I/O on an async/event-loop path; N+1 queries; per-row commits instead
of bulk operations; missing pagination or unbounded result sets; hardcoded security/auth
configuration; database index or scaling weaknesses; race conditions and unsynchronised shared
state; resource leaks; missing timeouts.

### 02 — Architecture & Design
Missing failure isolation (one step failing kills an unrelated pipeline); duplicated or legacy
data structures with no migration path; modules the developers themselves flag as messy;
missing cost or rate controls on external/paid services; layers or services that add no value
(YAGNI); inappropriate coupling.

### 03 — Code Quality & Maintainability
Module-organisation debt; magic numbers / hardcoded config that should be settings;
accumulation of TODO/FIXME comments (flag any that are security- or correctness-relevant);
unhelpful error propagation reaching end users; naming and duplication.

### 04 — Test Coverage
Untested modules, routers, or endpoints; missing boundary and edge-case tests; coverage
exclusions that hide gaps; test infrastructure that is configured but unused; shallow tests
that assert calls rather than behaviour.

Adapt the set to the system: a library has no "endpoints"; a data pipeline weights resilience
heavily. Keep the numbering contiguous for the categories you do produce.

## Diagram conventions

See `diagram-templates.md`. All diagrams are Mermaid sharing one fixed theme block so they
render consistently and export cleanly to Word. The default set is five C4-style diagrams;
produce only the 2–5 that fit the target system — never force an irrelevant diagram.

The diagrams are lightweight review aids, not a replacement for the organisation's established
architecture-diagramming standards and tooling, and are not aligned to them. State this caveat
in the diagram section of `00-architecture-overview.md`.
<!-- TODO(PR review): name the organisation's official architecture-diagramming standard/tool. -->

## Prioritization

### Effort/Impact matrix
Place every finding in one quadrant. *Impact* is severity-driven (Critical/High → high impact).
*Effort* uses the S/M/L/XL estimate (S → low effort).

- **QUICK WINS** — low effort, high impact. Do first.
- **BIG BETS** — high effort, high impact. Plan deliberately.
- **CONSIDER** — low effort, low impact. Optional.
- **STRATEGIC** — high effort, low impact. Schedule or defer.

### Action waves
Group findings into sequential waves for sprint planning — e.g. Wave 1 quick wins, Wave 2
critical performance, and so on. State dependencies between findings ("do F-x before F-y").
Assign each item a Suggested Owner (team/component) and an effort estimate.

## Consistency checklist (Phase 7)

Check and fix every one of these:

- Severity tally in the executive summary equals the sum across the category finding tables and
  the finding index.
- Each finding's effort label is identical in its detail block, the finding index, and the
  effort/impact matrix.
- `F-NN` ids are sequential, unique, and gap-free; every finding appears once in the index.
- Every finding lives in exactly one category document.
- Any value annotated on a diagram (a threshold, a count, a port) matches the finding or fact it
  illustrates.
- Hotspot file lists are in descending change-count order and agree between `00` and the
  appendix.
- Each finding's matrix quadrant matches its severity and effort.
- The findings-map preview in `00` matches the final set of findings.
- All cross-document links resolve.

## Output acceptance criteria

A finished review must satisfy all of:

- Every finding has all nine template fields, none empty.
- Every Evidence entry cites a real file; line numbers appear only where actually read;
  uncertainty is marked.
- Severity counts reconcile across `00`, the category documents, and `05`.
- The "What the team is doing well" section is present and non-empty.
- Diagrams render as valid Mermaid; only diagrams relevant to the system are included.
- `CHANGELOG.md` exists (even if "Initial cut — no revisions").
- No `F-NN` gaps or duplicates; every finding is in the index.
- The deliverable contains no personal data — no contributor names, emails, or per-person
  statistics; every "Suggested Owner" is a team or component.

## Bundled assets

- `document-skeletons.md` — empty document shells to create in Phase 1.
- `diagram-templates.md` — the fixed Mermaid theme block and diagram stubs.
- `code-hotspots.md` — the file-change-frequency command and appendix format.
