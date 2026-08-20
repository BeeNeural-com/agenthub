---
name: secrets-scanning
description: >-
  Scan repositories, CI logs, and artifacts for exposed secrets. Use in CI and after suspected leakage.
tags: [security, secrets]
---

# Secrets Scanning

## When to Use

- Setting up pre-commit or CI secret detection
- Investigating leaked credential alert
- Onboarding new repo to security baseline

## Procedure

### Step 1: Configure scanners

- Enable git history scan on repo add
- Custom patterns for org-specific tokens
- Integrate with CI blocking on findings

### Step 2: Triage findings

- Verify true positive vs test fixtures
- Assess exposure: committed, public, forked
- Rotate credentials if ever in git history

### Step 3: Remediate

- Remove secret from history if policy requires (BFG/filter-repo)
- Move to vault; inject via CI secrets
- Add allowlist only with justification

### Step 4: Prevent recurrence

- Developer training on env vars
- Pre-commit hooks locally
- Audit quarterly

## Output

Scan report at `doc/security/secrets-scan-<repo>-<date>.md`.
