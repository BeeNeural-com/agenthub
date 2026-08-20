---
name: requirements-writing
description: "Component software requirements authoring reference for E3 Software Platform. Contains common patterns, anti-patterns, guidance on abstraction level, and other best practices. Use when writing or reviewing software requirements."
---

# Requirements writing

This skill provides authoring patterns, guidance on abstraction level, and anti-patterns and best practices for software requirements. Use it when writing or reviewing requirements in `doc/<component>/component_requirements/*.md`.

## Abstraction level

Requirements describe observable black-box behavior. Design choices or implementation details, like concrete artifact names, exact log strings, or file formats, must not appear in requirement text.

- **Use externally observable entities or concepts** defined in the glossary or the referenced domain or technology knowledge, or which are commonly known behaviors, states, or interface interactions of such entities (e.g., create, close, remove, open, release, reject, status, message, trigger, notification, callback, log, etc.).
- **Never embed exact file or directory names or paths, or deployment layouts** in requirement text. Use descriptive noun phrases (e.g., "the flash wear configuration", "configuration directory", "static data path", "alterable data path").
- **Never use bullet lists to format logging requirements.** Do not use bullet lists with `log level:` and `log message:`. Write a single sentence instead.
- **Never embed exact log message strings.** State the log severity and semantic meaning in a single sentence (e.g., "shall log a warning indicating that the status file is unavailable").
- **Use the following phrases for logging:**
  | Severity | Short form (no context) | Short form (with context) |
  |----------|-------------------------|---------------------------|
  | fatal    | "log a fatal error"     | "log a fatal error message with the system error" |
  | error    | "log an error"          | "log an error message with the socket path and system error" |
  | warning  | "log a warning"         | "log a warning message indicating that the value is out of range" |
  | info     | "log an info message"   | "log an info message indicating successful startup" |

- **Exception:** Concrete symbols, like configuration field names, or parameters (e.g., `cycleSizeLimit`, `bufferMemoryVolumeLimit`), are acceptable in requirements if they define the observable interface contract.

Examples:

| DO NOT write                                    | CORRECT                                                         | 
| ----------------------------------------------- | ----------------------------------------------------------------|
| Exact file names: `FlashWearConfiguration.json` | Descriptive terms: "the flash wear configuration"               |
| Exact log strings: `"XYZ not found. Aborting."` | Semantic meaning: "shall log a fatal error indicating that ..." |
| Subfolder paths: `subfolder "config"`           | Abstracted: "from the static data path"                         |


## Produce complementary pairs

If a concept has an observable complementary pair (e.g., success/failure, presence/absence, mandatory/optional), write separate requirements for each observable outcome. This ensures that both the expected and the complementary behavior are explicitly defined and verifiable.

Examples:

- **Mandatory vs optional**: When a component supports both mandatory and optional features (e.g., configuration), write separate requirement pairs. When mandatory configuration is absent, the component shall prevent startup and log a fatal error. When optional configuration is absent, the component shall use the default value and log a warning. Do not conflate the two behaviors in a single requirement.
- **Success vs failure**: Every operation that can succeed or fail needs BOTH a success and a failure requirement.
- **Resource lifecycle**: Include requirements for creation and usage of resources, as well as requirements for their cleanup/destruction.


## Trigger chain

If the `when` trigger of a requirement is the completed outcome of a prior requirement in the same flow, use the completed-action form of the prior step as the trigger. This is the primary mechanism for expressing dependency between steps; no linking is needed.

Example:

```
Requirement A: "...the <component> shall reject the incoming connection."
Requirement B: "When the Server rejects a Client's incoming connection, the <component> shall reject the Client's connect request ..."
```

**Trigger verb**: The trigger verb must match the completed-action verb in the corresponding use case step exactly. If a use case step says "The Server accepts the incoming connection", the trigger is "When the Server accepts a pending client connection". Never use vague processing verbs ("processes", "handles") as triggers.

**Trigger forms**: Both `"When <completed step>"` and `"After <completed step>"` are valid patterns. Use `when` for events triggered by an actor; use `after` if the trigger is a prior step's completed outcome (e.g., "After the Server closes the acceptor socket during shutdown").

**Never use `before` or `after` to order two actions within a single requirement.** This couples two steps into one requirement and violates atomicity. Split the requirement into two steps, and use the trigger chain pattern to express the ordering between them.

Examples:

| DO NOT use ordering in one sentence using `before` or `after`| CORRECT: use trigger chain |
|---|---|
| "shall close the acceptor socket before releasing clients" | A: "...shall close the acceptor socket." <br> B: "After the Server closes the acceptor socket, ...shall release all server-side resources." |
| "shall release clients after closing the acceptor socket"  | Split as above. |
| "shall stop accepting connections before closing clients"      | A: "shall stop accepting connections." <br> B: "When the Server stops accepting connections during shutdown, shall release all server-side resources for each connected Client." |
| "shall close the acceptor socket after all clients are closed" | "When the Server releases all server-side resources for connected Clients during shutdown, the Server shall close the acceptor socket." |

**Return value and intermediate steps**: Only use "return <result/status>" as a companion verb when there are no independently observable intermediate steps in the use-case flow between the trigger and the result. If the use-case flow has 2 or more steps with observable side effects (filesystem changes, cross-side exchanges, visible state changes) between the trigger and the result, then:
- all requirements for the given normal flow except the last one include the respective observable side effect; they do not include a return statement
- only the final requirement of the trigger chain includes the return statement.

Example: 

```
"When <the last step>, the <component> shall return success to the caller."
```

**Shutdown ordering**: When writing requirements for shutdown or cleanup sequences, trigger chains may be used to enforce the correct order. Consider the following:
- Close the acceptor or listener socket **before** releasing the resources associated with the connected peers. Closing it is the only reliable barrier against new connections being queued during the shutdown.
- Releasing resources during shutdown or cleanup is a best-effort operation. The component should attempt to release all resources, but if some resources cannot be released (e.g., due to a system failure), the component should still proceed with shutdown and log the failure, rather than leaving the system in an indeterminate state.


## Edge case handling

When analyzing or updating requirements for edge cases:

- **Combine equivalent outcomes:** when multiple error conditions produce the same observable behavior, use a single requirement with "or".
- **Adapt existing requirements:** over adding new ones, i.e., widen the scope (e.g., "not found" → "not found or cannot be parsed") to cover related error variants.
- **Sharpen wording:** add precise qualifiers (e.g., "completed log files" instead of "log files") rather than separate edge-case requirements.
- **Keep verification criteria up-to-date:** if multiple edge cases are covered in a requirement, ensure the verification criteria cover them as well.
- **Add new requirements only if necessary:** add a new requirement only if the edge-case produces a **different observable behavior** not covered by any existing requirement.


## Requirement ordering within a topic file

Requirements in a topic file must follow the use case flow **step by step**. For each step, write the **happy-path requirement first**, then all edge-case and failure requirements for that step, before moving on to the next step. This mirrors how a reviewer reads the use case and makes gaps immediately visible, compared to clustering all happy paths together followed by all failure paths.

**Pattern:**

```
Step 1 — happy path
Step 1 — failure / edge case A
Step 1 — failure / edge case B
Step 1 — constraint (if any)
Step 2 — happy path
Step 2 — failure / edge case
...
```

**Rules:**
1. **Happy path first.** The success requirement for a step always comes before any failure or edge-case requirement for that same step.
2. **Group by step, not by classification.** Do not cluster all success requirements together followed by all failure requirements. Keep each step's requirements adjacent.
3. **Constraints inline.** If a constraint applies to a specific step (e.g., required set of resource configuration parameters for its creation), place it immediately after the happy path for that step, before the failure requirements.
4. **Cross-cutting topic concerns last.** Requirements that span the entire topic (e.g., logging policy, thread-safety notes) go at the end of the respective topic file, after all step-specific requirements.


## Component API specification

Components, or their parts, that expose an API to external actors or to other components or their parts shall be specified as described below. The order of the stated requirements does not imply the order of their evaluation. Every requirement is independent.

The term `<requester>` is a placeholder for the caller of the API. The caller may be external to the component or an internal actor within the component. Concrete roles shall be defined in the component glossary. If no specific external actors are defined in the glossary, "caller" or "user" may be used instead.

The term `<provider>` refers to the software component itself, or to an actor within the component (e.g., a library, a server, a client).

**Declare the API need**
"The <provider> shall provide an API that allows a <requester> to <perform something> by providing <parameter(s)>."

**Pre-condition check for invalid parameters**
"If the <requester> provides <invalid-parameter-condition> and requests the <provider> to <perform something>, the <provider> shall <error reaction>."

**Pre-condition check for invalid states, ordering, or environment assumptions**
"If <invalid-pre-condition> and the <requester> requests the <provider> to <perform something>, the <provider> shall <error reaction>."

**Normal observable behavior (if there are no pre-conditions)**
"When a <requester> requests the <provider> to <perform something> with <valid parameter(s)>, the <provider> shall <do observable action>."

**Normal observable behavior (if pre-condition(s) exist)**
"When a <requester> requests the <provider> to <perform something> with <valid parameter(s)> and <valid-pre-condition(s)>, the <provider> shall <do observable action>."

**Internal or action-related error reaction**
"If an <error condition> while performing <action>, the <provider> shall <error reaction>."


## Cross-cutting concepts

Requirements that span the entire component, like general logging policy or threading/event-loop model, are placed in a dedicated topic file (e.g., logging.md, threading.md). Such requirements typically have the verification method set to `static_test` (since automated tests cannot exhaustively verify all error paths or proper use of threading). The individual functional requirements (in the respective topic files) then focus only on the observable outcome of the operation (e.g., status returned, notification delivered) without embedding logging or threading details.

Example:

````markdown
## REQ: Error logging policy

```yaml
id: req:<component>-error-logging
classification: constraint
status: draft
covers: uc-error-logging
verification_method: static_test
```

When an error condition occurs, the <component> shall log an error message stating the error and its context.

> **Rationale:** Consistent error logging is required for failure diagnostics.

> **Verification criteria:** During code review, inspect every code path that returns a failure status and verify that a log call at the appropriate severity level is present.

---
````

## Multi-step operations and atomicity

When a use case step describes a multi-step operation, where the steps do not represent a black-box view (e.g., "bind and start listening"), describe the **overall observable outcome** with a single composite verb rather than listing each white-box step as a separate verb.

Logging, rejecting, and returning a status/result (e.g., "log", "reject", "return") are permitted as companion verbs alongside the primary action and do not violate atomicity.

Example:

| DO NOT write (not atomic, white-box)                      | CORRECT: one composite black-box verb |
| --------------------------------------------------------- | -------------------------------------------------------------------------- |
| "shall bind ..., start listening ..., and return success" | "shall set up the acceptor socket on the provided path and return success" |

## ASPICE rating guidelines

For the Automotive SPICE rating rules that govern SWE.1 process assessment, see [aspice-rating-guidelines.adoc](./aspice-rating-guidelines.adoc).

---

## Example: Use of optional annotations

````markdown
## REQ: Temperature reporting range

```yaml
id: req:libsmart-thermostat-temperature-range
classification: functional
status: draft
covers: (TODO: Provide upstream artefact ID for temperature reporting)
verification_method: dynamic_test
```

The Smart Thermostat shall report temperatures in the range from (TODO: confirm minimum value) to (TODO: confirm maximum value) degrees Celsius.

> **Rationale:** (TODO: Confirm the required operating temperature range with the hardware team.)

> **Verification criteria:** Set up the test environment for the sensor to report values at the lower and upper boundaries, as well as typical representative values in the specified range; verify that the Smart Thermostat reports each value correctly.

> **Analysis note:** The temperature sensor has a hardware resolution of 0.5°C. Test input values that are not multiples of 0.5°C will be rounded by the sensor, causing a discrepancy between the configured input and the reported value.

> **Environment impact:** Requires a calibrated temperature sensor stub capable of simulating values across the full specified range.

---
````

## Example: Trigger chain and step-by-step ordering

The example below shows use of trigger chaining and step-by-step ordering patterns. The individual requirements are not shown, just their titles.

```markdown
<!-- Step 1: Server instance construction (no parameters, no resource acquisition, cannot fail) -->
## REQ: Server setup success
<!-- Step 2: Server activation at the provided path triggered, path validation -->
## REQ: Server activation with empty path rejected
<!-- Step 3: Server activation at a valid path, remove any stale socket first -->
## REQ: Stale socket removal
<!-- Step 3: failure path, stale socket removal fails, new socket cannot be created -->
## REQ: Stale socket removal failure
<!-- Step 4: Server activation at a valid path, socket creation with close-on-exec flag constraint -->
## REQ: Acceptor socket close-on-exec flag
<!-- Step 4: Server activation at a valid path, socket creation, bind or listen fails -->
## REQ: Acceptor socket setup failure
<!-- Step 5: Server activation at a valid path, every partial step completed, success -->
## REQ: Acceptor socket setup success
```
