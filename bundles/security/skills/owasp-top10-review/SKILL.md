---
name: owasp-top10-review
description: >-
  Review application against OWASP Top 10 web risks with remediation guidance. Use for web app security assessments.
tags: [security, owasp]
---

# OWASP Top 10 Review

## When to Use

- Pre-release security checklist for web app
- Pen test prep or finding triage
- Annual app security hygiene review

## Procedure

### Step 1: Scope application

- List endpoints, auth model, data classification
- Identify frameworks and dependency versions
- Note API vs server-rendered vs SPA

### Step 2: Assess each category

- Broken access control, cryptographic failures, injection, etc.
- Evidence: code path, config, or test result
- Rate: pass, partial, fail

### Step 3: Remediate

- Critical/high findings block release
- Provide fix pattern, not only CWE ID
- Retest after fix

### Step 4: Report

- Summary for engineering manager
- Detailed findings for developers
- Track in vulnerability backlog

## Output

Report at `doc/security/owasp-review-<app>-<date>.md`.
