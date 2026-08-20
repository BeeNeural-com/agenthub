---
name: api-design
description: >-
  Design REST, GraphQL, or gRPC APIs with consistent conventions and versioning. Use when exposing new or revised service interfaces.
tags: [software-engineering-general, api]
---

# API Design

## When to Use

- Public or partner API design
- Internal service contract definition
- API redesign for breaking change management

## Procedure

### Step 1: Model resources

- Noun-based resources and consistent pluralization
- Represent relationships via URLs or embedded refs
- Define idempotency for mutating operations

### Step 2: Request and response

- Standard error envelope with codes and details
- Pagination, filtering, sorting conventions
- Use appropriate HTTP status codes

### Step 3: Versioning and compatibility

- URL or header versioning strategy
- Deprecation timeline and sunset headers
- Backward-compatible field additions only

### Step 4: Documentation and testing

- OpenAPI/Proto spec as source of truth
- Contract tests for consumers
- Rate limits and auth documented

## Output

OpenAPI/Proto spec in repo; summary in `doc/engineering/api-<name>.md`.
