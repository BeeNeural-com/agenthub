---
name: glossary-authoring
description: Guidelines for authoring glossary entries in the specification of a component. Terms defined in the glossary are used in the component specification to ensure consistent terminology across the whole development lifecycle.
applyTo: '**/doc/*/glossary.md'
---

# Glossary Authoring

A component glossary contains domain-specific technical terms that may not be self-evident to readers of the component specification.

## Format and Storage

The glossary for a component is stored in `doc/<component>/glossary.md`.

The glossary file is a Markdown document with the following structure:

````markdown
# Glossary: <Component Name>

This glossary defines terms used across the specifications of the <Component Name> component.
All terms are specific to this component. Where a term carries a different meaning in general usage, that distinction is noted.

---

## <Category or group name>

### <Term name>
<Definition of the term.>

### <Term name using other terms in definition>
<Definition of the term, which includes [Other term name](#<other-term-name>) in its definition.>

### <Term name related to other term>
<Definition of the term.> <See also: [<Related term name>](#<related-term-name>).>

---
````

The format of a glossary entry link is `[Term name](#term-name)`, where `term-name` is the lowercase form of the term name, with:
- spaces replaced by `-`
- `-` and `_` preserved
- the special characters `@#$%^&*()[]{}<>+.,;:?!'"\|/``~` removed.

Examples:

| Term name               | Link anchor (fragment identifier) |
| ---                     | ---                               |
| Client Application      | `#client-application`             |
| User-defined limit      | `#user-defined-limit`             |
| C/C++ naming convention | `#cc-naming-convention`           |


The term "Client Application" would be linked from `glossary.md` as `[Client Application](#client-application)`.

## Rules

- **Group terms by category**, not alphabetically (e.g., Roles, Connection Lifecycle, Sockets and Filesystem, Capacity, Event Processing).
- **Keep definitions short**: 1–2 sentences.
- **Avoid using special characters in term names**.
- **Use cross-reference links** in the term definitions, which make use of use other glossary terms.
- **Add 'See also:'** to link related terms in the glossary for more clarity (optional).
