---
applyTo: ".github/skills/**/*.md"
---

# Skill File Authoring Rules

This instruction defines the required structure, naming conventions, and content constraints for SKILL.md files in `.github/skills/<topic>/`.

---

## Required SKILL.md Structure

Every SKILL.md must follow this 7-section template (include only sections relevant to the skill topic):

```markdown
---
name: <topic-slug>
description: "<Routing signal: one or two sentences that tell the router WHEN to inject this skill — include the trigger scenario and what the skill provides>"
---

# <Title> Skill

<One paragraph summary of what this skill provides and who uses it.>

---

## Overview
<High-level summary of the domain, concept, or technique.>

---

## Reference / API
<Canonical tables, block formats, attribute rules, classification tables — the normative reference content.>

---

## Lifecycle & Usage Pattern
<How the content is used in practice: workflow steps, state model, sequencing rules.>

---

## Examples
<Generic worked examples. Must use <placeholder> syntax for any component-specific names.>

---

## Best Practices / Anti-patterns
<Dos and don'ts. Common mistakes. Quality criteria.>

---

## Domain Glossary
<Term definitions relevant to this skill's domain (optional; omit if handled by doc/<component>/glossary.md).>
```

---

## Description Field — The Router Signal

The `description` field is the primary signal Copilot uses to decide when to inject this skill. Rules:

1. **Start with a trigger scenario**: "Use when writing…", "Use when reviewing…", "Use when the user asks about…"
2. **State what the skill provides**: tables, examples, criteria, state models, format patterns.
3. **Avoid generic phrasing** like "contains useful information about X" — be specific about what X is.
4. **Keep it under 50 words** — longer descriptions lose router precision.

**Good example:**
```yaml
description: "SWE.1 requirements authoring reference. Use when writing or reviewing component_requirements .md files. Provides format patterns, abstraction level guidance, info: vs req: rules, and ASPICE BP3/BP4 evidence attributes."
```

**Bad example:**
```yaml
description: "Contains information about ASPICE SWE.1 requirements and how to write them."
```

---

## Knowledge Base State Model

Track the maturity of each skill using these states:

| State | Definition |
|---|---|
| **Absent** | No SKILL.md exists for this topic |
| **Stub** | SKILL.md exists with only frontmatter and a title |
| **Partial** | Some sections present but key reference tables or examples are missing |
| **Draft** | All sections present; content is AI-generated or unreviewed |
| **Current** | All sections present; content has been reviewed and is considered accurate |

Use the state to prioritize which skills to improve next. Aim for **Draft** or better before an agent references the skill in its `> See skill:` directives.

---

## What Must Never Appear in Skill Files

Skill files are component-agnostic. Never include:

| Forbidden content | Generic alternative |
|---|---|
| Component name (e.g., `my-server-lib`) | `<component>` |
| Specific class name (e.g., `MyServerClass`) | `<ComponentName>` |
| Specific method name (e.g., `doOperation()`) | `<operationName>()` |
| Specific req: ID (e.g., `req:my-lib-topic-success`) | `req:<component>-<topic>-<aspect>` |
| Specific arch: ID (e.g., `arch:my-lib-some-service`) | `arch:<component>-<element>` |
| File paths specific to one project | Generic path patterns |

**Exception**: Illustrative examples in a clearly marked "Example" or "Anti-pattern" section may use concrete names, but must also show the generic placeholder equivalent.

---

## C++ Code Example Quality

Code examples in skill files are the canonical reference agents use when generating production code. Violations in skill examples propagate into every file an agent writes.

### `.clang-format` compliance

- Do not write single-line function bodies. Place the body on its own line with a closing `}` on its own line.
- Open braces for functions, classes, structs, and control statements go on their own line (Allman style).
- Empty function bodies must be split: `{\n}`, never `{}` on one line.

**Wrong:**
```cpp
int value() const { return mValue; }      // short function on one line
struct Foo { int mX; };                   // struct brace on same line
```

**Correct:**
```cpp
int value() const
{
    return mValue;
}

struct Foo
{
    int mX;
};
```

### CP10 naming compliance

Rules from `.github/instructions/cpp-naming-conventions.instructions.md` apply to all C++ code in skill files:

| Element | Convention | Wrong | Correct |
|---|---|---|---|
| Parameters | `camelBack`, no prefix | `aHandler`, `a_handler`, `pFoo` | `handler`, `foo` |
| Local variables | `camelBack`, no prefix | `eventVal`, `tmpBuf` | `eventValue`, `tempBuffer` |
| Private class members | `m`-prefix `CamelCase` | `fd_`, `m_fd`, `onEvent_` | `mFd`, `mOnEvent` |
| Constants | `k`-prefix `CamelCase` | `MAX_SIZE`, `defaultTimeout` | `kMaxSize`, `kDefaultTimeout` |
| Abbreviations in names | Expand fully | `fd`, `addr`, `buf`, `ptr`, `val` | `fileDescriptor`, `address`, `buffer`, `pointer`, `value` |

The `a`-prefix on parameters is **never correct** in this codebase. It originates from a different convention and must not appear in examples.

---

## File Location and Naming

- Location: `.github/skills/<skill-name>/SKILL.md`
- Skill name: lowercase-kebab-case, matching the `name` frontmatter field
- **Flat layout required**: all skills are direct children of `.github/skills/`. Do not create category or group subdirectories. GitHub Copilot discovers skills by scanning direct children of `.github/skills/`.
- One SKILL.md per skill directory

## Adding a New Skill

1. Create `.github/skills/<skill-name>/` directory.
2. Create `SKILL.md` with frontmatter + title only (Stub state).
3. Add content in draft passes, following the 7-section template.
4. **Update `.github/skills/README.md`**: add a row to the matching section table with the file link, `name` frontmatter value, and `description` frontmatter value. If no existing section fits the skill's topic domain, create a new section.
5. Update any agent files that should reference this skill with `> See skill: .github/skills/<skill-name>/SKILL.md`.
6. Update `.github/AGENTS.md` if the new skill adds a new entry to the Shared Services or Role Agent tables.
