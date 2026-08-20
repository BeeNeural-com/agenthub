---
name: web-ecosystem-catalog
description: >-
  Living reference index of major web libraries by category: UI, state, forms, auth,
  testing, CSS, and build tools. Use when selecting libraries or onboarding to the stack.
tags: [web-development, ecosystem, reference]
---

# Web Ecosystem Catalog

## When to Use

- Selecting a library for a new feature (UI kit, form lib, auth, ORM)
- Onboarding developers to the project's stack choices
- Comparing alternatives before adding npm dependencies
- Auditing dependencies against current ecosystem standards

## Procedure

### Step 1: Identify category need

- Match the task to a category table below (Frameworks, State, Forms, etc.)
- Shortlist 2-3 candidates from the table

### Step 2: Verify current versions

- Run **npm-package-research** for each candidate's latest stable version
- Check compatibility with project's React/Vue/Angular/Node version
- Read official docs linked in the table; do not rely on this catalog alone for API details

### Step 3: Apply selection criteria

- TypeScript support, tree-shaking, bundle size (Bundlephobia)
- License compatibility (MIT, Apache-2.0, BSD)
- Maintenance: recent release, responsive maintainers
- Team familiarity and existing project conventions

### Step 4: Update project decisions

- Document chosen library in README or ADR
- Add to lockfile with intentional semver range

## Library Index

### Frameworks and Meta-Frameworks

| Library | npm package | Docs |
|---------|-------------|------|
| React | `react` | https://react.dev |
| Next.js | `next` | https://nextjs.org/docs |
| Vue | `vue` | https://vuejs.org |
| Nuxt | `nuxt` | https://nuxt.com/docs |
| Angular | `@angular/core` | https://angular.dev |
| Svelte | `svelte` | https://svelte.dev/docs |
| SvelteKit | `@sveltejs/kit` | https://kit.svelte.dev/docs |
| Remix | `@remix-run/react` | https://remix.run/docs |
| Astro | `astro` | https://docs.astro.build |
| SolidJS | `solid-js` | https://www.solidjs.com/docs/latest |

### State Management

| Library | npm package | Docs |
|---------|-------------|------|
| Zustand | `zustand` | https://zustand.docs.pmnd.rs |
| Redux Toolkit | `@reduxjs/toolkit` | https://redux-toolkit.js.org |
| Jotai | `jotai` | https://jotai.org |
| Pinia | `pinia` | https://pinia.vuejs.org |
| NgRx | `@ngrx/store` | https://ngrx.io |
| TanStack Query | `@tanstack/react-query` | https://tanstack.com/query |
| XState | `xstate` | https://stately.ai/docs |

### Forms

| Library | npm package | Docs |
|---------|-------------|------|
| React Hook Form | `react-hook-form` | https://react-hook-form.com |
| Formik | `formik` | https://formik.org |
| TanStack Form | `@tanstack/react-form` | https://tanstack.com/form |
| VeeValidate | `vee-validate` | https://vee-validate.logaretm.com |
| Angular Reactive Forms | `@angular/forms` | https://angular.dev/guide/forms |
| Zod (validation) | `zod` | https://zod.dev |

### Authentication

| Library | npm package | Docs |
|---------|-------------|------|
| Auth.js (NextAuth) | `next-auth` / `@auth/core` | https://authjs.dev |
| Clerk | `@clerk/nextjs` | https://clerk.com/docs |
| Auth0 SDK | `@auth0/nextjs-auth0` | https://auth0.com/docs |
| Supabase Auth | `@supabase/supabase-js` | https://supabase.com/docs/guides/auth |
| Passport.js | `passport` | https://www.passportjs.org |
| Lucia | `lucia` | https://lucia-auth.com |

### ORM and Database Clients

| Library | npm package | Docs |
|---------|-------------|------|
| Prisma | `@prisma/client` | https://www.prisma.io/docs |
| Drizzle ORM | `drizzle-orm` | https://orm.drizzle.team |
| TypeORM | `typeorm` | https://typeorm.io |
| Sequelize | `sequelize` | https://sequelize.org/docs |
| Mongoose | `mongoose` | https://mongoosejs.com/docs |
| Kysely | `kysely` | https://kysely.dev |
| pg (PostgreSQL) | `pg` | https://node-postgres.com |

### CSS and Styling

| Library | npm package | Docs |
|---------|-------------|------|
| Tailwind CSS | `tailwindcss` | https://tailwindcss.com/docs |
| shadcn/ui | (copy-paste components) | https://ui.shadcn.com |
| MUI | `@mui/material` | https://mui.com/material-ui |
| Radix UI | `@radix-ui/react-*` | https://www.radix-ui.com |
| Headless UI | `@headlessui/react` | https://headlessui.com |
| styled-components | `styled-components` | https://styled-components.com |
| Emotion | `@emotion/react` | https://emotion.sh/docs |
| CSS Modules | (built-in) | https://github.com/css-modules/css-modules |

### Testing

| Library | npm package | Docs |
|---------|-------------|------|
| Vitest | `vitest` | https://vitest.dev |
| Jest | `jest` | https://jestjs.io/docs |
| Testing Library | `@testing-library/react` | https://testing-library.com |
| Playwright | `@playwright/test` | https://playwright.dev |
| Cypress | `cypress` | https://docs.cypress.io |
| MSW (mocking) | `msw` | https://mswjs.io |

### Build Tools

| Library | npm package | Docs |
|---------|-------------|------|
| Vite | `vite` | https://vite.dev |
| Webpack | `webpack` | https://webpack.js.org |
| esbuild | `esbuild` | https://esbuild.github.io |
| Turbopack | (bundled in Next.js) | https://nextjs.org/docs/architecture/turbopack |
| Rollup | `rollup` | https://rollupjs.org |
| SWC | `@swc/core` | https://swc.rs/docs |

## Output

- Recommended library from catalog with npm install command and doc link
- Brief rationale against alternatives in the same category

## References

- npm registry: https://www.npmjs.com/
- Bundlephobia: https://bundlephobia.com/
- State of JS survey: https://stateofjs.com/
- npm trends: https://npmtrends.com/
