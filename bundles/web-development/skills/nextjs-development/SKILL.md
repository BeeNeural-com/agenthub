---
name: nextjs-development
description: >-
  App Router, SSR/SSG, server actions, routing, and data fetching in Next.js.
  Use when building or reviewing Next.js applications.
tags: [web-development, nextjs, react]
---

# Next.js Development

## When to Use

- Creating or extending a Next.js app with App Router
- Choosing between SSR, SSG, ISR, or client-side rendering
- Implementing server actions, route handlers, or middleware
- Optimizing data fetching and caching in Next.js

## Procedure

### Step 1: Confirm Next.js version and router

- Check `next` version in `package.json` via **npm-package-research**
- Default to App Router (`app/` directory) for new projects unless legacy Pages Router required
- Read version-specific docs at nextjs.org/docs for that major version

### Step 2: Plan rendering strategy

- **Server Components** (default): data fetching without client JS overhead
- **Client Components** (`"use client"`): interactivity, hooks, browser APIs
- **Static**: `generateStaticParams` for build-time paths
- **Dynamic**: `fetch` with `{ cache: 'no-store' }` or `revalidate` for ISR

### Step 3: Routing and layouts

- Use nested `layout.tsx` for shared UI; `page.tsx` for route content
- Route groups `(folder)` for organization without URL impact
- `loading.tsx`, `error.tsx`, and `not-found.tsx` for UX boundaries
- API endpoints via `route.ts` (Route Handlers) or Server Actions

### Step 4: Data fetching and mutations

- Fetch in Server Components directly; pass data as props to Client Components
- Server Actions for form mutations with `"use server"` directive
- Configure `next.config.js` for redirects, rewrites, and image domains

### Step 5: Performance and deployment

- Use `next/image` and `next/font` for optimized assets
- Analyze bundle with `@next/bundle-analyzer` when needed
- Verify build with `next build`; test SSR output in production mode

## Output

- Next.js route, component, or server action implementation
- Rendering strategy notes (SSR/SSG/CSR) and caching decisions documented

## References

- Next.js docs: https://nextjs.org/docs
- App Router: https://nextjs.org/docs/app
- Server Components: https://nextjs.org/docs/app/building-your-application/rendering/server-components
- Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions
- Route Handlers: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
