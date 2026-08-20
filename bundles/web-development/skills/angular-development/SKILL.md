---
name: angular-development
description: >-
  Standalone components, signals, RxJS, and Angular CLI workflows.
  Use when building or reviewing Angular applications.
tags: [web-development, angular, frontend]
---

# Angular Development

## When to Use

- Building Angular apps with standalone components (no NgModule required)
- Using signals for reactive state (Angular 16+)
- Integrating RxJS streams for async data and events
- Scaffolding or extending projects with Angular CLI

## Procedure

### Step 1: Confirm Angular version and CLI

- Check `@angular/core` version via **npm-package-research**
- Use **web-docs-research** for version-matched docs at angular.dev
- Run `ng version` to verify CLI and workspace alignment

### Step 2: Standalone component architecture

- Generate with `ng generate component --standalone`
- Import dependencies directly in component `imports` array
- Bootstrap with `bootstrapApplication(AppComponent, appConfig)` in `main.ts`
- Provide services via `providers` in route or application config

### Step 3: Signals and reactivity

- `signal()` for writable state; `computed()` for derived values
- `effect()` for side effects reacting to signal changes
- Prefer signals for local UI state; RxJS for HTTP streams and complex async
- Use `input()` and `output()` signal-based APIs (Angular 17.1+) where available

### Step 4: RxJS and data fetching

- `HttpClient` with typed responses and interceptors for auth/errors
- Unsubscribe via `async` pipe, `takeUntilDestroyed`, or `toSignal()`
- Avoid nested subscriptions; use `switchMap`, `mergeMap` appropriately
- NgRx or signals-based stores for complex global state

### Step 5: Routing and forms

- Lazy-loaded routes with `loadComponent` for standalone components
- Reactive forms (`FormBuilder`) for complex validation; template-driven for simple cases
- Run `ng build --configuration production` before release

## Output

- Standalone Angular component, service, or route configuration
- Notes on signals vs RxJS usage for the feature

## References

- Angular docs: https://angular.dev/
- Standalone components: https://angular.dev/guide/components/importing
- Signals: https://angular.dev/guide/signals
- RxJS guide: https://angular.dev/guide/rx-library
- Angular CLI: https://angular.dev/tools/cli
