---
name: requirements-specification
description: 'Conventions for specifying component software requirements in Markdown format.'
applyTo: '**/doc/*/component_requirements/**/*.md'
---

## Purpose

Define formats, rules, and conventions for specifying component software requirements in Markdown format.

## Rules

- **Normative input.** The only permitted inputs for specifying requirements are: product specification (`doc/<component>/product_specification/*`), use cases (`doc/<component>/use_cases/*`), glossary (`doc/<component>/glossary.md`).
- **Scope.** Only specify requirements for the component and features described by the user.
- **Black-box perspective.** Only specify requirements describing externally observable properties and behavior of the component or its externally visible parts, not their internal workings.
- **Use of specific domain or technology knowledge.** The specific domain or technology knowledge (`.github/skills/<topic>/SKILL.md`) can be used only if the user explicitly references it. In such cases, only the black-box terminology and concepts can be used.
- **Never invent information.** If a detail is missing, use `(TODO: <what is missing>)` as placeholder and ask the user.
- **Never assume upstream references.** Only use upstream artifact IDs the user explicitly provides. Use `(TODO: <missing upstream reference>)` otherwise.

## File Organization

The component requirement specification consists of one or more requirement files in `doc/<component>/component_requirements/`. One requirement file contains blocks, which are requirements or optional non-normative information about a specific topic or feature.

The file `doc/<component>/component_requirements/requirements.md` is an index that lists all requirement files for a given component. It does not include any requirements or information blocks. The format is as follows:

**Index file**

```markdown
# Component Requirements for the <Component Display Name>

<Overview or introduction text.>

* [Topic name](<topic-file-name>.md) +
```

**Topic files**

A topic file contains requirements and information blocks related to a single topic or feature. File names must be lowercase and may include only `a–z`, `0–9`, and `_`. The file structure is defined as follows:

```markdown
# <Topic Name>

<information-block with introduction to the topic>

<information-or-requirement-block> +
```

## Requirement and Information Blocks Syntax

Each requirement or information block is a Markdown section with a human-readable heading, a YAML metadata block, a block sentence, and other information.

The block's heading level is one below its nearest enclosing heading level. In a flat file (`#` Title, no sub-section) block headings are `##`. Inside a sub-section with level `##`, block headings are `###`, etc.

### Requirement Block

Requirement blocks contain normative information. The requirement block sentence is a normative "shall" sentence, followed by additional blockquote annotations.

````markdown
## REQ: <Concise requirement name>

```yaml
id: req:<component>-<feature>-<short-name>
classification: <functional|constraint|quality>
status: <draft|accepted|obsolete>
covers: <comma-separated IDs of upstream references>
verification_method: <dynamic_test|static_test|no_test>
```

<Requirement statement in active voice with exactly one "shall">

> **Rationale:** <Explanation of why this requirement exists>

> **Verification criteria:** <Verification guidance>

---
````

### Information Block

Information blocks describe context, definitions, recommendations, or background information that is not a requirement. They have an ID so that they can be referenced.

````markdown
## INFO: <Concise information name>

```yaml
id: info:<component>-<topic>-<short-name>
status: <draft|accepted|obsolete>
```

<Informative non-normative text. Not a requirement, i.e., no "shall".>

---
````

Examples:
- If a component is single-threaded by design and provides no internal locking, document this as an information block in a topic file such as `thread_safety.md`. It is a usage contract for the API caller, rather than a behavioral obligation of the component.
- Expected implementation methods (for example, POSIX APIs selected by the design) can be listed as an information for the designer. These constitute a possible design choice (possibly evaluated in a prior proof-of-concept).

## Metadata Fields

The metadata fields of each respective block are mandatory.

### Requirement identifier

- The field **`id`** is a unique requirement or information identifier.
- Requirement ID format is `req:<component>-<descriptive-kebab-case-id>`: all lowercase, with characters `a-z`, `0-9`, and `-` only.
- Information IDs use the `info:` prefix instead of `req:`.
- The part `<component>` is the component name from the glossary, in lowercase, with spaces replaced by `-`, e.g., `libipc -> libipc`, `Smart thermostat -> smart-thermostat`.
- **Keep IDs consistent with the block terminology.** When a term used in a block statement is renamed (e.g., "command" to "message"), and the term is used in the block's ID, then update the ID to match the block terminology.

### Classification

- The field **`classification`** indicates the type of requirement.
- Use **`functional`** for requirements describing an observable behavior as a response to an input, i.e., what the component *does* when an operation is requested, succeeds, fails, or a condition holds.
- Use **`constraint`** for requirements restricting the design/solution space, e.g., use of POSIX API, language subset (C++ 17), runtime support (no RTTI, no heap allocation), compile-time configurability, etc. Constraints do not describe responses to events.
- Use **`quality`** for requirements specifying the quality attributes of a component (performance, reliability, availability, portability) without prescribing a specific action.

### Traceability

- The field **`covers`** includes a list of upstream artefact identifiers (upstream references) for traceability.
- Use the referenced artifact identifier as is, e.g., `feat:FEAT-123`, `req:upstream-id`, `uc:use-case-id`, `cb:STKH-123`, `qual:QCPL-123`.
- Use `(TODO: missing upstream reference)` as placeholder if reference is not yet available.

### Status

- The field **`status`** indicates the current state of the requirement.
- Use `draft` for all **new or modified** requirements.
- Never modify for untouched requirements.

### Verification method

- The field **`verification_method`** indicates how the requirement will be verified.
- Use `dynamic_test` for automated testing. Prefer whenever possible.
- Only use `static_test` when the requirement cannot be verified by an automated test and requires verification by a review or analysis (e.g., proving absence of a feature or property across all code paths, for verification of constraints, etc.).
- Never use `no_test`; warn the user if existing requirements make use of `no_test`.

## Verification criteria

- The section **`Verification criteria`** contains mandatory information providing additional guidance on how to verify the requirement.
- For verification method `dynamic_test`, the criteria describe the automated test scenario, i.e., stimulation and the expected outcome(s). The stimulation must specify how the test environment or the system under test is set up and/or triggered to provoke the behavior(s) leading to the observable outcome.
- For verification method `static_test`, the criteria describe the scope of a review or analysis (e.g., which code areas to inspect and what to look for) and explain why a dynamic test is not feasible.
- **Observable component state or response belongs in the requirement sentence, not only in the verification criteria.** If verification criteria are the only place that specifies observable state or response (e.g., return value, callback argument, etc.), move that detail into the requirement sentence.
- **Always update if the requirement statement changes.** Whenever the requirement sentence changes, update the verification criteria to match the requirement.

## Rationale

- The section **`Rationale`** is mandatory if the upstream references (`covers`) are absent or include `TODO`. Optional otherwise.
- **Recommended** even when upstream references are present to help reviewers understand the intent.
- Explain the need for the requirement in a clear and concise manner.

## Optional annotations

Optional annotations, listed below, are added to a requirement block only when necessary, after the verification criteria.

### Analysis note

Add section **Analysis note** if you discover non-obvious information that is not captured in the requirement or its rationale, e.g., a feasibility constraint or a testability concern.

### Environment impact

Add section **Environment impact** when the requirement imposes a constraint on the operating environment or reveals a runtime resource or deployment dependency, e.g., tmpfs mount required at runtime; one file descriptor consumed per active connection.

### TODO placeholders

Use `(TODO: <explain what is missing>)` in the block's metadata fields, statement, rationale or verification criteria to mark incomplete items when information is missing or not available.


## Requirement Statement

Follow this constrained syntax:

```markdown
[If <condition>,] [when <trigger>,] the <component> shall <action> <object>.
```

**Component and role names**

- **Do not append "library" or similar to the component name.** The preferred form is `the <component> shall ...`.
- **Always include the definite article "the" before the component name**: both at the start of a sentence (`The <component> shall ...`) and in the consequent clause of a conditional sentence (`If ..., the <component> shall ...`). Never write a bare component name without "the" in a requirement sentence.
- **Capitalise component and role names consistently.** The capitalisation of component and role names is defined in the glossary or the product specification; treat them as proper nouns. Use the same capitalisation in the verification criteria and rationale as well.

**Clause semantics ("If" vs "When")**

- **"When"**: use for **expected triggers** on the happy path. These are normal operations the user initiates (e.g., "When the server application creates a Server instance ...", "When the Server processes a pending client connection ...").
- **"If"**: use for **causal conditions, error paths, and input validation failures**. These describe situations where something goes wrong or a precondition is checked (e.g., "If creating the acceptor socket fails ...", "If the provided socket path is empty ...").
- **"If ... and ..."**: when the condition and the action are part of the same causal chain, combine them with `and` in a single `if` clause. Do **not** nest `when` inside an `if` clause (e.g., write "If the application provides an empty path and requests ..." instead of "If the application provides an empty path when requesting ...").

**Rules**

- **One "shall"** per requirement: exactly one process verb (atomic). **Exception**: verbs "log", "reject", and "return" are always permitted as companion verbs alongside the primary action. For example, "shall release Y and return a failure status" is atomic.
- **Active voice** — component is always the subject.
- **"shall"** only — never "should", "may", "must", "can".
- **Positive voice ALWAYS** — "shall not" may not appear in any requirement. Rewrite: "shall not crash" → "shall recover from errors"; "not at retrieval time" → "during ingestion"; "are not obfuscated" → "remain unobfuscated". State what the component *shall do*, never what it *shall not do*.
- **No weak words**: never use "support", "appropriate", "efficient", "robust", "user-friendly", "as possible", "multiple", "timely", "adequate", "sufficient", "easy", "reliable", "normal", "quickly", "state-of-the-art".
- **No vague trigger verbs**: never use "processes", "handles", "manages", "deals with", "takes care of" as the trigger verb in a `when` clause. Replace with the precise verb for the completed action from the use case step: "accepts", "detects", "receives", "requests", "sends", "triggers".
- **Using "or" in condition clause**: use "or" only if the condition options are mutually exclusive, do not require separate handling, and cannot be triggered independently. Otherwise, split into separate requirements.
- **Black-box perspective**: external behavior only, no implementation details.
- **Continue-on-error: singular condition clause.** In requirements that mandate continuing after a partial failure, use singular in the condition clause: "If a system error occurs while releasing *a* [singular resource] during [operation], the [component] shall continue releasing the other [plural resources]."
