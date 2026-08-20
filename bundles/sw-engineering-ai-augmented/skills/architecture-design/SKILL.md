---
name: architecture-design
description: 'Authoring judgement for architectural design of E3 Software Platform components: abstraction level, what qualifies as an element, when element data fields and diagrams are needed, scenario coverage in sequence diagrams, and design alternatives. Use when authoring or reviewing a component architecture.'
---

# Architectural design authoring

This document provides guidance for what to specify and how to decide when authoring or reviewing architecture in `doc/<component>/component_architecture/`. The form and format of every artifact is governed by the `architecture-specification` instructions and is not repeated here.

## Abstraction level

Specify responsibilities and contracts at element boundaries from a black-box perspective. Exclude internal implementation details.

| DO NOT use in architecture                                   | CORRECT                                                                 |
| ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| "uses `ioctl()` to read the sensor register at address 0x4A" | "queries the physical temperature sensor and returns its current value" |
| "stores state in `std::atomic<bool> mHeatingActive`"         | "maintains the current activation state of the heating actuator"        |
| "calls `ara::log::CreateLogger(\"THERM\")`"                  | "issues log messages via the platform logging mechanism"                |

An element's behavior is black-box by default unless a design decision of the component states otherwise.

## When a concept becomes an element

Promote a concept to an element only when all the following hold:

- **Persistent state between calls**: The concept maintains state across invocations that affects later behavior. Pure functions of their inputs are not elements.
- **Lifecycle**: The concept has creation, active-use, and destruction phases with observable state transitions. A concept that is instantiated once and never changes, or that needs no instantiation, belongs in detailed design.
- **First-class participant**: The concept acts as an autonomous peer in at least one interaction, receiving stimuli and producing responses that change observable state. A synchronous call-and-return helper with no side effects beyond its return value is an internal utility. Elements forming the component's external API are first-class by definition.
- **Cross-boundary side effects**: The concept's operations produce effects observable outside the call chain (e.g., shared state, resources, IPC). If the only meaningful check is "did the caller get the right return value?", no architectural boundary is needed.

**If a concept fails these but carries an architecturally significant contract** (e.g., a specific encoding, a polling semantic), capture the contract as either a design decision, or a behavioral constraint in the calling operation's specification (e.g., "encodes a fixed-size header containing payload size and metadata before transmission"). This leaves detailed design free to choose the realization (e.g., free function, template, inline, class).

## When a behavioral element gets data fields

Data-model elements use data fields to specify the information they represent. These data fields are always public.

Behavioral elements (those with operations) normally have no data fields; their white-box state is defined in detailed design. Specify a data field on a behavioral element only when a requirement or a design decision mandates it. Such a data field has the following visibility:
- mandated as part of the element's interface -> public visibility
- mandated as internal state -> private visibility.

## Choosing diagrams

The following guidance helps determine when a diagram must be included in an architectural specification.

**Stateful elements need a state machine diagram**
A stateful element has any of the following:
- distinct lifecycle phases (creation, init, active, shutdown, destruction)
- distinct operating modes or states (idle, busy, connected, disconnected, degraded), or
- operations whose effect depends on current state.

**Complex operations need an activity diagram**
- A complex operation has at least two non-trivial branching steps.
- An activity diagram complements, but never replaces, the natural language description of the operation.
- Omit the activity diagram if the operation's logic is up to about five sequential steps with trivial fail-fast exits, or if the logic is better shown in a sequence diagram.

**Sequence diagram(s) are needed to show every operation outcome**
- Aim for the smallest set that still shows every operation outcome at least once.
- Split large diagrams into cohesive parts, or reuse repeated sequences via reference fragments.

## Scenario coverage in sequence diagrams

Sequence diagrams must cover the following scenarios when matching requirements exist:

- **Initialization**: how the component starts and becomes ready.
- **Normal operation**: happy-path sequences for the primary operations.
- **Error flows**: at least one scenario per distinct error condition that is observable in or on the operations.
- **Shutdown**: how shutdown is handled and how resources are released.
- **Concurrency model**: which threads exist, which elements run in which threads, how synchronization is ensured.

Additionally, include the following when matching requirements exist:
- resource cleanup during normal operation
- thread safety and concurrency
- retry and recovery of failed operations
- credential verification or authentication.

## Design alternatives

When multiple reasonable alternatives exist, document them with pros and cons, and with the rationale for the selected option. Place the selected alternative in the main `component_architecture/*.md` files. Place each rejected alternative in its own `design_alternative_<alt-name>/` subdirectory (layout defined in the instructions file).

Summarize and compare the alternatives in `design_decisions.md`:

```markdown
## Design alternatives

| Alternative | Summary | Decision |
| ----------- | ------- | -------- |
| <Alternative A> | <Short description> | selected/rejected: <one to five major pros/cons> |
| <Alternative B> | <Short description> | ... |

Comparison:

| Aspect/property | <Alternative A> | <Alternative B> | ... |
|---|---|---|---|
| <design aspect or property> | <assessment of how A addresses it> | ... | ... |
```

Assessments may be qualitative (e.g., "best", "good", "medium", "poor") or quantitative (e.g., "2ms latency", "5% CPU"). If an assessment is too complex for the table, include a brief summary in the cell and provide the detailed explanation in text below, with references to specific fragments in the subdirectory of the alternative.

If alternatives address several distinct design aspects, each with their own properties, split the `Comparison` section into one table per aspect (e.g., "Comparison: concurrency model", "Comparison: error handling").

## ASPICE rating guidelines

For the Automotive SPICE rating rules governing SWE.2 assessment, see [aspice-rating-guidelines.adoc](./aspice-rating-guidelines.adoc).

## Relation to detailed design

Downstream artifacts, such as detailed design, reference architecture fragments by their identifiers. Element realization (e.g., module, class) and implementation naming are decided in later stages.
