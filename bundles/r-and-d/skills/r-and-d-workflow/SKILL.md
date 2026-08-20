---
name: r-and-d-workflow
description: >-
  Orchestrate end-to-end R&D pipelines: research scouting, feasibility, prototyping,
  experiment design, and handoff to requirements. Use when planning a full R&D initiative
  or routing work across research, innovation, and engineering stages.
tags: [r-and-d, workflow, orchestration]
---

# R&D Workflow Orchestration

Route R&D work through the correct Agent Hub skills and agents.

## Pipeline A: Research to Product

1. **technology-scouting** — landscape and vendor evaluation
2. **literature-review** — prior art and academic/industry evidence
3. **feasibility-study** — technical and economic viability
4. **trade-study** — compare options with weighted criteria
5. **research-to-requirements** — translate findings into component requirements
6. **function-owner** agent → **write-epics** → **write-user-stories**

## Pipeline B: Innovation to Prototype

1. **innovation-ideation** — structured ideation and TRL assessment
2. **prototype-spike** — time-boxed proof of concept
3. **experiment-design** — hypothesis, variables, controls
4. **data-analysis** — interpret results
5. **feasibility-study** — go/no-go decision

## Pipeline C: IP-Aware Development

1. **prior-art-search** — patents and publications
2. **ip-landscape** — freedom-to-operate overview (non-legal)
3. **architecture-design** skill → existing SWE bundle

## Agent Routing

| Task type | Agent |
|-----------|-------|
| Research, scouting, feasibility | research-analyst |
| Ideation, TRL, roadmap input | innovation-lead |
| PoC, spike execution | prototype-engineer |
| Prior art, IP mapping | ip-analyst |
| Requirements handoff | function-owner |
| Architecture & design | software-architect |
| Implementation | software-engineer |

## When to Use

- Starting a new R&D initiative without knowing which skill applies
- Routing multi-stage research → engineering work
- Ensuring IP and feasibility gates are not skipped
