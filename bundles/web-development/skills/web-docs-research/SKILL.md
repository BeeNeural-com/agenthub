---
name: web-docs-research
description: >-
  Find official documentation (MDN, React/Vue/Angular/Node/Next sites), version-specific
  docs, and avoid stale blog posts. Use when verifying APIs or learning current best practices.
tags: [web-development, documentation, research]
---

# Web Docs Research

## When to Use

- Verifying API behavior before writing code (do not rely on training data alone)
- Finding version-specific docs for the exact framework version in the project
- Resolving deprecation warnings or migration paths
- Confirming browser support or platform feature availability

## Procedure

### Step 1: Identify the authoritative source

| Topic | Official source |
|-------|-----------------|
| Web platform (HTML, CSS, JS APIs) | MDN Web Docs |
| React | https://react.dev |
| Next.js | https://nextjs.org/docs |
| Vue | https://vuejs.org |
| Angular | https://angular.dev |
| Node.js | https://nodejs.org/docs |
| TypeScript | https://www.typescriptlang.org/docs |
| npm / Node packages | Package README + linked docs site |

Always prefer `.org` or official project domains over third-party tutorials.

### Step 2: Match documentation version

- Read `package.json` for exact major version installed
- Use versioned doc URLs when available (e.g., Next.js `/docs` matches latest; Angular `/guide` for current)
- For MDN, check "Browser compatibility" table for target browsers
- Archive.org only as fallback for removed APIs; prefer current docs

### Step 3: Search effectively

- Site-restricted search: `site:developer.mozilla.org <topic>`
- Use official search within doc sites (React, Next.js, Vue all have search)
- Cross-reference spec (WHATWG, W3C) for edge-case behavior
- Avoid Medium/Dev.to posts for API signatures; use them only for conceptual overview

### Step 4: Validate freshness

- Check "Last updated" or git history on doc pages when visible
- Compare with release notes / CHANGELOG for the installed version
- If docs conflict with behavior, check GitHub issues on the official repo

### Step 5: Cite sources in deliverables

- Link official doc URLs in code comments, PRs, and skill outputs
- Note doc version/date when behavior is version-sensitive

## Output

- Curated list of official doc links relevant to the task
- Version-matched guidance summary with source citations
- Migration notes if upgrading between major versions

## References

- MDN Web Docs: https://developer.mozilla.org/
- MDN sitemap: https://developer.mozilla.org/sitemap.xml
- Can I use (browser support): https://caniuse.com/
- web.dev (Google): https://web.dev/
- W3C TR index: https://www.w3.org/TR/
