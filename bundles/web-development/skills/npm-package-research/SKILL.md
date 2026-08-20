---
name: npm-package-research
description: >-
  Search npm registry, compare versions, semver, bundle size, and pick latest stable packages.
  Use before adding or upgrading npm dependencies.
tags: [web-development, npm, tooling]
---

# npm Package Research

## When to Use

- Adding a new dependency to a web project
- Upgrading packages to latest stable or a specific major version
- Comparing alternative libraries (e.g., date libs, HTTP clients)
- Assessing bundle impact before importing a client-side package

## Procedure

### Step 1: Search the npm registry

- Query registry API: `https://registry.npmjs.org/<package-name>`
- Or run: `npm view <package> versions --json` and `npm view <package> version`
- Check weekly downloads and last publish date on https://www.npmjs.com/package/<name>
- Prefer maintained packages with recent releases and active issue responses

### Step 2: Evaluate version and semver

- **Latest stable**: `npm view <package> version` (not `@next` or `@beta` unless intentional)
- **Peer dependencies**: verify compatibility with React/Vue/Angular version in project
- Pin with caret (`^`) for minor updates; exact pin for critical infra packages
- Read CHANGELOG and migration guide before major version bumps

### Step 3: Compare alternatives

- List 2-3 candidates from **web-ecosystem-catalog**
- Compare: bundle size, TypeScript support, tree-shaking, license (MIT/Apache preferred)
- Check bundlephobia: https://bundlephobia.com/package/<name>
- Avoid packages that duplicate built-in platform APIs

### Step 4: Security and maintenance

- Run `npm audit` after install; review advisories for direct vs transitive deps
- Check GitHub stars, open issues, and bus factor
- Prefer packages with provenance and signed publishes when available

### Step 5: Document the decision

- Record chosen package, version, and rationale in PR or ADR
- Note breaking changes and required config (polyfills, peer installs)

## Output

- Recommended package name, exact version range, and install command
- Comparison table if evaluating alternatives
- Bundle size estimate for client-side imports

## References

- npm registry API: https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
- npm semver: https://docs.npmjs.com/about-semantic-versioning
- npm view command: https://docs.npmjs.com/cli/v10/commands/npm-view
- Bundlephobia: https://bundlephobia.com/
- npm downloads: https://www.npmjs.com/
