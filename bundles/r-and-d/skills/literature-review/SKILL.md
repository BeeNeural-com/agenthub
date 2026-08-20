---
name: literature-review
description: >-
  Conduct a structured literature and prior-work review. Use when gathering academic,
  industry, and internal evidence before feasibility studies, architecture decisions,
  or research reports.
tags: [r-and-d, research, literature]
---

# Literature Review

Systematically collect and synthesize existing knowledge before new R&D work.

## When to Use

- Starting research on an unfamiliar domain
- Validating assumptions before a feasibility study
- Supporting prior-art or patent searches
- Building evidence for a research report

## Procedure

### Step 1: Define scope

- Research question (one sentence)
- Inclusion criteria (date range, domains, languages)
- Exclusion criteria
- Key search terms and synonyms

### Step 2: Search sources

Search in order:
1. Internal docs, wikis, prior POC reports
2. Industry standards and white papers
3. Academic databases (Google Scholar, IEEE, ACM)
4. Open source repos and issue trackers
5. Patent databases (for IP overlap awareness)

### Step 3: Screen and extract

For each source record:
- Title, author, date, link
- Relevance (high / medium / low)
- Key findings (3 bullet max)
- Limitations or conflicts with other sources

### Step 4: Synthesize

Group findings by theme. Identify:
- Consensus views
- Contradictions
- Gaps in existing work
- Implications for your project

### Step 5: Document

Use `references/review-template.md`. Include bibliography with links.

## Quality checks

- At least 2 independent sources for major claims
- Note publication date and recency
- Flag single-source claims as low confidence
