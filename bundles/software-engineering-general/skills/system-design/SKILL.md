---
name: system-design
description: >-
  Design distributed systems with capacity, consistency, and failure modes. Use for new services or major scalability changes.
tags: [software-engineering-general, system]
---

# System Design

## When to Use

- Design interview or architecture review prep
- Scaling service beyond current limits
- Splitting monolith or adding async processing

## Procedure

### Step 1: Requirements

- Functional requirements and SLAs (QPS, latency, durability)
- Consistency model needs (strong vs eventual)
- Regulatory or residency constraints

### Step 2: High-level design

- Draw components: clients, APIs, workers, stores, queues
- Define data flow for read and write paths
- Identify single points of failure

### Step 3: Deep dive critical paths

- Estimate capacity with back-of-envelope math
- Choose storage and indexing strategy
- Plan caching and CDN if applicable

### Step 4: Reliability

- Failure scenarios: node loss, partition, dependency down
- Mitigations: retry, circuit breaker, bulkhead
- Observability per **monitoring-setup**

## Output

Save as `doc/engineering/system-design-<topic>.md` with diagrams.
