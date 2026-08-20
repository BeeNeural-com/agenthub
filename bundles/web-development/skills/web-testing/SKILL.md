---
name: web-testing
description: >-
  Vitest, Playwright, Cypress, and Testing Library for unit, integration, and E2E tests.
  Use when setting up or writing tests for web applications.
tags: [web-development, testing, quality]
---

# Web Testing

## When to Use

- Setting up a test suite for a new web project
- Writing unit tests for components, hooks, or utilities
- Adding integration tests for API routes or pages
- Creating E2E tests for critical user flows

## Procedure

### Step 1: Choose test layers

| Layer | Tool | Scope |
|-------|------|-------|
| Unit | Vitest / Jest | Functions, hooks, composables |
| Component | Testing Library + Vitest | Render, user interaction, a11y |
| Integration | Vitest + MSW | API mocking, multi-component flows |
| E2E | Playwright / Cypress | Full browser, real backend or staging |

Follow testing pyramid: many unit, fewer integration, minimal E2E for happy paths.

### Step 2: Configure test runner

- Vitest for Vite projects; Jest for CRA/legacy
- Setup file: `@testing-library/jest-dom` matchers
- MSW for HTTP mocking in integration tests
- Verify versions via **npm-package-research**

### Step 3: Write effective tests

- Test behavior, not implementation (query by role/label, not class names)
- Use `userEvent` over `fireEvent` for realistic interactions
- Arrange-Act-Assert structure; one assertion focus per test
- Mock external services; do not mock the unit under test

### Step 4: E2E best practices

- Playwright: parallel workers, auto-wait, trace on failure
- Test critical paths: login, checkout, core CRUD
- Run against staging with test accounts; never production
- Integrate in CI with artifact upload on failure (screenshots, traces)

## Output

- Test files with clear describe/it blocks and meaningful names
- CI configuration snippet for running tests on PR

## References

- Vitest: https://vitest.dev/guide/
- Testing Library: https://testing-library.com/docs/
- Playwright: https://playwright.dev/docs/intro
- Cypress: https://docs.cypress.io/guides/overview/why-cypress
- MSW: https://mswjs.io/docs/
