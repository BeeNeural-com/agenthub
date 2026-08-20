---
name: use-case-writing
description: Rules for writing use case documents for software components
applyTo: "**/doc/*/use_cases/**/*.md"
---

# Use-case writing instructions

## File and use-case identifier conventions

- One use case per file.
- Use case identifier format is `uc:<descriptive-kebab-case-id>`, all lowercase, may include only `a–z`, `0–9`, and `-`.
- File name format is: `<use_case_identifier>.md`, with `:` and `-` replaced by `_` (e.g., `uc_speaking_use_case_id.md` for `uc:speaking-use-case-id`).

## Use-case index file

The file `doc/<component>/use_cases/index.md` is an index file that lists all use cases for a given component. The format is as follows:

```markdown
# Use Cases for the <Component Display Name>

* [Use case name 1](<use-case-file-name-1>.md) : <one line brief description>
* [Use case name 2](<use-case-file-name-2>.md) : <one line brief description>
...
```

Update the use-case index file when adding, updating or removing use cases.

## Use-case file format

````markdown
# <use-case-identifier>

<One-sentence description of the use case.>

**Precondition:** <Links to files of the use cases that must happen before this use case. Use "None. Short explanation sentence.", otherwise.>

**Normal flow:**

<Numbered happy-path steps.>

**Result:** <Observable state after success.>

**Failure paths:**

<Bullet list (error condition -> outcome) stating all possible failure paths. Use "None. Short explanation sentence.", if no such paths exist.>

**Precondition for:** <Links to files of the use cases that this use case is a precondition for. Use "None. Short explanation sentence.", otherwise.>

**Reference:** <Links to source document sections.>

[back to index](./index.md)
````

Do **not** add standalone `**Actor:**` or `**Trigger:**` fields. Who initiates the scenario and what triggers it must be named in the flow steps themselves.

## Ordering

- Order top-down: start from what is externally observable, then derive the enabling infrastructure.
- Do not order by implementation dependency alone.

## Vocabulary

Use only the following:

* terms that are commonly used for the given topic
* terms defined in the glossary (`doc/<component>/glossary.md`)
* vocabulary of the product specification (`doc/<component>/product_specification/*.md`)
* black-box terms defined for technologies referenced in the specification index (`doc/<component>/index.md`)

Do not use an alternative term for the same role or concept.

## Cross references

Never use bare text identifiers for cross referencing; instead use Markdown links, e.g., `[<use-case-identifier>](<use-case-file-name>.md)`.

For references to parts of a product specification document, use `[section title](../product_specification/<document>.md#section-title-anchor)`.

Use case prose does not need to reference glossary entries explicitly.

## Actor Naming

Actor names are defined in the glossary or the product specification. Use each name exactly as defined there.

**Patterns to avoid:**

| Avoid | Use instead |
|---         |---    |
| "user", "caller"              | the external role name from the glossary; "user" or "caller" is allowed only if there is only one kind of external role and glossary does not define any name for it (pick one and use consistently)  |
| "<component> process", "<role> process", "process" | the component role name from the glossary |
| concrete library or class names in prose | the role name from the glossary           |
| adjective-qualified variants ("server-side application", "host application") | the exact role name from the glossary |

**When multiple roles apply as an actor in a use case**, use the longest common term rather than the individual separate role names (e.g., if "Server Application" and "Client Application" are both the actors, use "Application" as the actor name in the use case prose). Capitalize the derived actor name according to the defined rules (e.g., "Server application", "Client application" -> "Application").

When the product specification defines that an operation is performed via an intermediate actor (which is part of an actor or component), the use case step must name that intermediate actor as the direct target of the request, not the enclosing entity.

## Rules

- **One file per use case**: one use case, one file.
- **No API names or symbols**: Describe observable black-box behavior; never name standard library functions, system calls, flags, options, or error codes.
- **No class or method names**: Write, for example, "Application requests the Calculator to add"; never use implementation-style notation like `calculator.add()`.
- **No concrete error, status, option or flag values**: Write, for example, `"arithmetic overflow"`; never use implementation-style notation like `ARITHMETIC_OVERFLOW`.
- **Abbreviations**: Use abbreviations defined in the glossary, or write terms in full everywhere else, e.g., "file descriptor" instead of "fd".
- **Log before reject**: "logs an error and rejects the request with status X"
- **"None" requires justification**: Follow "None." with an explanatory sentence.
