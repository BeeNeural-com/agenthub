---
name: typescript-frontend
description: >-
  TypeScript patterns for React, Vue, and Angular: generics, strict mode, typed props,
  and shared types. Use when adding types to frontend code.
tags: [web-development, typescript, frontend]
---

# TypeScript for Frontend

## When to Use

- Adding TypeScript to a JavaScript frontend project
- Typing React props, Vue composables, or Angular services
- Sharing types between client and API (monorepo or openapi-typescript)
- Enabling or tightening `strict` compiler options

## Procedure

### Step 1: Configure TypeScript

- Enable `strict: true` in `tsconfig.json` for new projects
- Set `moduleResolution: "bundler"` for Vite/Next.js projects
- Configure path aliases (`@/*`) matching bundler resolution
- Use **web-docs-research** for framework-specific tsconfig templates

### Step 2: Framework typing patterns

**React**
- `interface Props { ... }` or `type Props = { ... }` for components
- `React.FC` discouraged; type props directly on function signature
- `useRef<HTMLInputElement>(null)` for DOM refs

**Vue**
- `<script setup lang="ts">` with `defineProps<{...}>()` 
- Typed composables: return type inferred or explicit interface

**Angular**
- Strict templates (`strictTemplates: true` in angular.json)
- Typed `FormControl<string>`, inject with `inject()` function

### Step 3: Shared and API types

- Generate types from OpenAPI with `openapi-typescript`
- tRPC or shared package for end-to-end type safety
- Zod schemas infer types: `type User = z.infer<typeof UserSchema>`
- Avoid `any`; use `unknown` + type guards for external data

### Step 4: Utility types and generics

- `Partial<T>`, `Pick<T, K>`, `Omit<T, K>` for flexible APIs
- Generic components: `<T extends { id: string }>(items: T[]) => ...`
- Discriminated unions for state machines and action types

## Output

- Typed components/services with no implicit `any`
- tsconfig changes documented if compiler options updated

## References

- TypeScript handbook: https://www.typescriptlang.org/docs/handbook/
- React TypeScript cheatsheet: https://react-typescript-cheatsheet.netlify.app/
- Vue TypeScript: https://vuejs.org/guide/typescript/overview.html
- Angular TypeScript: https://angular.dev/tools/cli/build#typescript-configuration
