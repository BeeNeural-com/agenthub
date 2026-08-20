---
name: secrets-management
description: >-
  Manage secrets lifecycle: storage, rotation, scanning, and access control. Use when handling credentials, API keys, or certificates.
tags: [devops-sre, secrets]
---

# Secrets Management

## When to Use

- New service needs secrets injection pattern
- Credential rotation after incident or policy
- Remediating leaked secrets in repo or logs

## Procedure

### Step 1: Inventory secrets

- List secret types: API keys, DB passwords, certs, tokens
- Map consumers (services, humans, CI jobs)
- Classify sensitivity and rotation frequency

### Step 2: Storage pattern

- Use vault/KMS — never commit secrets to git
- Inject at runtime via env or sidecar
- Separate secrets per environment

### Step 3: Rotation and access

- Automate rotation where platform supports
- Apply least privilege and audit access logs
- Revoke compromised secrets immediately

### Step 4: Prevent leakage

- Enable pre-commit and CI secret scanning
- Scrub logs and error messages for secret patterns
- Run **secrets-scanning** after any exposure event

## Output

Save policy as `doc/platform/secrets-<scope>.md`; implement in vault/IaC.
