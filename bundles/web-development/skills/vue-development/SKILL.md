---
name: vue-development
description: >-
  Vue 3 Composition API, Pinia, Vue Router, and SFC patterns.
  Use when building or reviewing Vue applications.
tags: [web-development, vue, frontend]
---

# Vue Development

## When to Use

- Building Vue 3 applications with Composition API
- Setting up Pinia stores and Vue Router navigation
- Migrating Options API code to Composition API
- Structuring Single File Components (SFCs) for maintainability

## Procedure

### Step 1: Confirm Vue ecosystem versions

- Check `vue`, `vue-router`, and `pinia` versions via **npm-package-research**
- Use **web-docs-research** for version-specific Vue docs (vuejs.org/guide)
- Prefer `<script setup>` syntax for new components

### Step 2: Component architecture

- One SFC per component: `<template>`, `<script setup>`, scoped `<style>`
- Props down, events up; use `defineProps` and `defineEmits` with TypeScript
- Extract reusable logic into composables (`useAuth`, `useFetch`) in `composables/`
- Use `defineModel` (Vue 3.4+) for two-way binding when appropriate

### Step 3: State and routing

- Pinia stores for shared application state; keep stores focused by domain
- Vue Router with lazy-loaded route components for code splitting
- Route guards for auth; meta fields for layout and permissions
- Prefer `storeToRefs` when destructuring reactive store state

### Step 4: Reactivity patterns

- `ref` for primitives; `reactive` for objects (avoid destructuring without `toRefs`)
- `computed` for derived state; `watch`/`watchEffect` for side effects
- `provide`/`inject` for dependency injection across deep trees

### Step 5: Testing and build

- Unit test composables and components with Vitest + `@vue/test-utils`
- Run `vue-tsc` for type checking in TypeScript projects
- Verify production build with `vite build` or framework-specific command

## Output

- Vue SFC(s), composable(s), or Pinia store with typed interfaces
- Router configuration notes if navigation changed

## References

- Vue 3 guide: https://vuejs.org/guide/introduction.html
- Composition API: https://vuejs.org/guide/extras/composition-api-faq.html
- Pinia: https://pinia.vuejs.org/
- Vue Router: https://router.vuejs.org/
- `<script setup>`: https://vuejs.org/api/sfc-script-setup.html
