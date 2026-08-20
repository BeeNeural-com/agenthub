---
name: nodejs-development
description: >-
  Node.js APIs, ESM/CJS modules, npm scripts, async patterns, and security basics.
  Use when building or reviewing server-side JavaScript/TypeScript.
tags: [web-development, nodejs, backend]
---

# Node.js Development

## When to Use

- Building HTTP servers, CLI tools, or backend services in Node.js
- Migrating between CommonJS and ESM module systems
- Reviewing async code, error handling, or npm script workflows
- Hardening Node.js services against common security issues

## Procedure

### Step 1: Confirm runtime and module system

- Check `package.json` for `"type": "module"` (ESM) or default CJS
- Verify Node.js version against `engines` field and project requirements
- Use `import`/`export` for ESM; `require`/`module.exports` for CJS only when legacy

### Step 2: Structure the application

- Separate entry point, routes/handlers, and business logic
- Use built-in `node:` prefix imports (`node:fs`, `node:path`, `node:http`)
- Configure npm scripts for dev, build, test, and lint in `package.json`

### Step 3: Async and error handling

- Prefer `async/await` over raw Promise chains for readability
- Wrap top-level async in try/catch or use `process.on('unhandledRejection')` in servers
- Use streams for large file I/O; avoid loading entire files into memory

### Step 4: Security and dependencies

- Never expose secrets in client bundles or logs
- Validate and sanitize all external input (query, body, headers, env)
- Run `npm audit` and pin dependencies with semver ranges intentionally
- Use **npm-package-research** to verify latest stable package versions

### Step 5: Verify against official docs

- Before implementing APIs, fetch current Node.js docs for the target version
- Use **web-docs-research** when unsure about API behavior or deprecations

## Output

- Working Node.js module or service with documented npm scripts
- Brief notes on module system, Node version, and key dependencies used

## References

- Node.js docs: https://nodejs.org/docs/latest/api/
- Node.js ESM: https://nodejs.org/api/esm.html
- npm scripts: https://docs.npmjs.com/cli/v10/using-npm/scripts
- Node.js security best practices: https://nodejs.org/en/docs/guides/security/
