---
name: changelog-generator
description: >-
  Produce user-facing release notes from commits, PRs, or tickets. Use before product or engineering releases.
tags: [software-engineering-general, changelog]
---

# Changelog Generator

## When to Use

- Preparing release notes for customers or internal users
- Summarizing sprint deliverables for stakeholders
- Documenting breaking changes for upgrade guides

## Procedure

### Step 1: Collect changes

- Gather merged PRs since last release tag
- Group by type: feature, fix, breaking, internal
- Exclude noise: chores, dependency-only bumps unless security

### Step 2: Write for audience

- User-facing: outcome language, not commit hashes
- Developers: migration steps for breaking changes
- Link to docs and KB articles

### Step 3: Highlight impact

- Call out security fixes without exploit detail
- Note performance improvements with benchmarks if available
- Thank contributors if open source

### Step 4: Publish

- Follow Keep a Changelog or team format
- Sync version in package manifests
- Coordinate with support and marketing on major releases

## Output

Update `CHANGELOG.md` and optional `doc/releases/v<version>.md`.
