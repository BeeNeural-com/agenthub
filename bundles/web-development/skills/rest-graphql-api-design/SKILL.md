---
name: rest-graphql-api-design
description: >-
  REST vs GraphQL, OpenAPI, tRPC, and fetch/axios patterns for web APIs.
  Use when designing or consuming HTTP APIs in web applications.
tags: [web-development, api, rest, graphql]
---

# REST and GraphQL API Design

## When to Use

- Designing a new API for a web or mobile client
- Choosing between REST, GraphQL, or tRPC for a TypeScript monorepo
- Writing OpenAPI specs or GraphQL schemas
- Implementing client-side data fetching with fetch or axios

## Procedure

### Step 1: Choose API style

| Style | Best for |
|-------|----------|
| REST + OpenAPI | Public APIs, broad client support, cacheable resources |
| GraphQL | Flexible client queries, nested data, mobile apps |
| tRPC | End-to-end TypeScript monorepos with shared types |
| Server Actions (Next.js) | Same-repo full-stack mutations without separate API layer |

Document trade-offs before committing; avoid mixing styles without clear boundaries.

### Step 2: Design the contract

- REST: noun resources, plural paths, standard HTTP verbs and status codes
- GraphQL: schema-first types, queries for reads, mutations for writes
- OpenAPI 3.1 spec as source of truth for REST; generate types with openapi-typescript
- Version via URL prefix (`/v1/`) or Accept header; document deprecation policy

### Step 3: Client fetching patterns

- Native `fetch` with typed wrappers; handle errors consistently
- axios: interceptors for auth tokens and global error handling
- React Query / TanStack Query for caching, retries, and stale-while-revalidate
- tRPC client for type-safe calls in shared TS projects

### Step 4: Cross-cutting concerns

- Authentication: Bearer JWT, session cookies (httpOnly, Secure, SameSite)
- Pagination: cursor-based for large datasets; offset for admin UIs
- Rate limiting and CORS configured at gateway or framework level
- Standard error envelope: `{ error: { code, message, details } }`

### Step 5: Validate with official references

- Use **web-docs-research** for framework-specific API route patterns
- Verify HTTP semantics against MDN before implementing edge cases

## Output

- API contract (OpenAPI YAML, GraphQL schema, or tRPC router)
- Client fetch utility or hook with error handling documented

## References

- OpenAPI spec: https://spec.openapis.org/oas/latest.html
- GraphQL: https://graphql.org/learn/
- tRPC: https://trpc.io/docs
- MDN fetch: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- axios: https://axios-http.com/docs/intro
