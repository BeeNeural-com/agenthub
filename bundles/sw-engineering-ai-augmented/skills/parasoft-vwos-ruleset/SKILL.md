---
name: parasoft-vwos-ruleset
description: "VW.os C++ Parasoft static analysis (SCA) ruleset with forbidden patterns and compliance rules. Use when reviewing C++ source files for SCA compliance or writing SCA-compliance guidance for E3 Software Platform components."
---

# VW.os C++ Parasoft SCA Ruleset

## Official References

| Reference | URL |
|---|---|
| Confluence page (E3SWPAC) | `https://devstack.vwgroup.com/confluence/spaces/E3SWPAC/pages/271657699/1.2+-+VW.os+Core+-+C+Parasoft+Configuration+Documentation` |
| Parasoft AUTOSAR package docs | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/AUTOSAR.html` |
| Parasoft CERT_CPP package docs | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/CERT_CPP.html` |
| Parasoft HICPP package docs | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/HICPP.html` |
| Parasoft SECURITY package docs | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/SECURITY.html` |
| Parasoft METRIC package docs | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/METRIC.html` |
| AUTOSAR C++14 Coding Guidelines | AUTOSAR specification behind the rule IDs |
| MISRA C++ 2008 | MISRA rule origins referenced in AUTOSAR rule comments |
| CERT C++ Coding Standard | Referenced by CERT_CPP rules |
| HIC++ v4.0 Coding Standard | Referenced by HICPP rules |

---

## Overview

The **VW.os C++ Parasoft SCA Ruleset** (ruleset name `VW.os C++14 Hosted QM 1.7.0`, version 56) is the mandatory static analysis configuration for all VW.os (E³ Software Platform) C++ projects. It is enforced by **Parasoft C++test** as part of the CI pipeline and gates code quality metrics.

The ruleset aggregates rules from five standards into a single Parasoft configuration with per-rule severity, security-relevance classification, and attribute tuning:

| Package | Standard origin | Focus |
|---|---|---|
| AUTOSAR | AUTOSAR C++14 + MISRA C++ 2008 | Language safety, type safety, resource management, OOP, templates, exception safety, library usage |
| CERT_CPP | CERT C++ Coding Standard | Memory safety, string safety, concurrency, signal handling |
| HICPP | HIC++ Standard v4.0 | Reachability, type safety, threading and concurrency |
| SECURITY | VW.os-specific security rules | OS/system call security, buffer overflows, privilege escalation, TOCTOU |
| METRIC | Code quality metrics | Cyclomatic complexity, coupling, comment ratio, fan-out |

### Rulesets / Severity Levels

Rules are filtered into subset rulesets by severity:

| Subset | Content |
|---|---|
| `standard` | All active rules (applied to all VW.os projects) |
| `highest` | Rules with severity "highest" only |
| `high` | Rules with severity "high" or "highest" |
| `medium` | Rules with severity "high", "highest", or "medium" |
| `NOMV` | Rules contributing to the NOMV (Number of Metric Violations) metric |
| `NOSECV` | Rules contributing to the NOSECV metric (Security relevant = "yes") |
| `NOMV/NOSECV` | Union of NOMV and NOSECV |

### Taint Analysis

Several AUTOSAR rules (A5-2-5-d, A27-0-1) activate Parasoft's interprocedural taint analysis engine. Enabled taint sources: socket, files, low-level input, network, pipes, system calls, user input, `main()` parameters. Streams are disabled (too many false positives).

---

## Best Practices

The following checklist is derived from the ruleset's active rules across all severity levels. Each item corresponds to an enforced requirement. **The target is zero Parasoft findings at any severity level** — treat every violation as a build-blocking defect, regardless of severity.

### Memory and Lifetime Safety

- **Never access an object outside its lifetime** (A3-8-1, M7-5-2): dangling pointers and references are build-blocking defects.
- **Never dereference a null pointer** (A5-3-2): guard all pointer dereferences; use `assert` or explicit null checks.
- **Never access an array or container beyond its range** (A5-2-5): validated by taint analysis from socket, network, file, and user-input sources.
- **Never read a moved-from object** (A12-8-3): after `std::move`, the source is in a valid-but-unspecified state — do not read it.
- **Initialize all memory before reading** (A8-5-0): uninitialized reads are undefined behaviour.

### Type and Cast Safety

- **Use only C++ named casts** (A5-2-2): `static_cast`, `const_cast`, `dynamic_cast`. C-style casts are forbidden.
- **Never use `reinterpret_cast`** (A5-2-4) unless unavoidable for hardware interface types; document every use.
- **Never cast away `const` or `volatile`** (A5-2-3).
- **Never use `volatile`** (A2-11-1): use proper synchronization primitives instead.

### Exception Safety

- **Provide at least basic exception safety for all operations** (A15-0-2): no resource leaks on exception exit.
- **If a function is declared `noexcept`, it must not exit with an exception** (A15-4-2, A15-1-4): destructors, move operators, and `swap` are implicitly expected to be `noexcept`.
- **Destructors, move constructors, move assignment operators, and `swap` shall not throw** (A15-5-1).
- **Implement the Rule of Five** (A12-0-1): if any of copy constructor, copy assignment, move constructor, move assignment, or destructor is declared, all five shall be declared.

### Thread Safety

- **Protect all shared mutable state with a single lock** (HICPP-18_2_2).
- **Use `std::call_once` for one-time initialization** (HICPP-18_2_4): the Double-Checked Locking pattern is forbidden.
- **Lock acquisition order must form a directed acyclic graph** (HICPP-18_3_2): document the lock hierarchy to prevent deadlocks.
- **No mutex locked twice in a single scope** (HICPP-18_3_1).
- **Do not use relaxed (non-sequentially-consistent) atomic operations** (HICPP-18_3_6): use `std::memory_order_seq_cst` or higher-level synchronization.
- **Do not use `std::recursive_mutex`** (HICPP-18_3_3): redesign to eliminate recursive locking.
- **Do not use platform-specific threading facilities** (HICPP-18_1_1): use `<thread>`, `<mutex>`, `<atomic>` from the C++14 standard library.

### Security (OS/System Calls)

- **Validate all external inputs before use** (A27-0-1, A5-2-5-d): socket data, file data, network data, user input, and pipe data are all taint sources.
- **Never use `exec`-family functions with dynamically constructed or non-const strings** (SECURITY-17, SECURITY-18).
- **Never call `system()`** (SECURITY-48, M18-0-3).
- **Never use `setuid`, `chmod`, `chown`, `chgrp`** (SECURITY-26, SECURITY-27): privilege escalation and TOCTOU vectors.
- **Use secure temporary file functions** (SECURITY-39): never `tmpnam` or `mktemp`.
- **Never use weak/broken cryptographic hash functions** (SECURITY-37).

### Code Complexity and Maintainability

- **Cyclomatic complexity (CC) ≤ 30** per function (METRIC.CC): refactor complex functions.
- **Coupling Between Objects (CBO) ≤ 30** per class (METRIC.CBO).
- **Fan-Out (FO) ≤ 30** per module (METRIC.FO).
- **Maintain the comment ratio** (METRIC.CLLOCRIF): document all public API surfaces with Doxygen comments.

### Prohibited Language Features

| Feature | Rule | Reason |
|---|---|---|
| C-style casts | A5-2-2 | Unsafe; bypasses type system |
| `reinterpret_cast` | A5-2-4 | Undefined behaviour risk |
| `volatile` | A2-11-1 | Does not provide synchronization; use `std::atomic` |
| `goto` | A6-6-1 | Unstructured control flow |
| `register` keyword | A7-1-4 | Deprecated in C++14 |
| `typedef` | A7-1-6 | Use `using` alias instead |
| `union` | A9-5-1 | Use `std::variant` instead |
| Scoped `enum` without underlying type | A7-2-2, A7-2-3 | Portability and clarity |
| `setjmp`/`longjmp` | M17-0-5 | Bypasses RAII and exception semantics |
| `errno` | M19-3-1 | Non-reentrant; use error return values |
| C-style I/O `<cstdio>` | M27-0-1 | Use C++ streams or POSIX I/O |
| `abort`, `exit`, `getenv`, `system` | M18-0-3 | Use application lifecycle management instead |
| Unbounded C string functions | M18-0-5 | Buffer overflow risk |
| `<csignal>` | M18-7-1 | Currently disabled but noted; use signalfd or self-pipe trick |
| Raw C arrays | A18-1-1 | Use `std::array` or `std::vector` |
| `std::auto_ptr` | A18-1-3 | Deprecated; use `std::unique_ptr` |

---

## Domain Glossary

This glossary classifies terms for use in requirements. Black-box terms describe externally observable behaviour and are allowed at any requirement level. White-box terms describe internal implementation details and are restricted to SWE.3/SWE.4 design and unit-test artefacts only.

### Black-Box Terms (approved for SWE.1 requirements)

**Static analysis violation**
Definition: A condition detected by the static analysis tool that matches a configured rule in the ruleset, resulting in a reported finding.
Rationale: Externally observable through CI pipeline reports and build gate results.

**Severity**
Definition: Classification of a rule violation into one of four levels — `highest`, `high`, `medium`, `low` — that determines which subset ruleset includes the rule and how urgently the finding must be addressed.
Rationale: Observable through tooling reports; drives acceptance criteria and build gates.

**Security-relevant finding**
Definition: A static analysis violation for a rule classified with "Security relevant = yes". These rules collectively form the NOSECV metric subset.
Rationale: Observable in tool reports and referenced in security-related acceptance criteria.

**Build-blocking defect**
Definition: A violation of a rule with severity `highest` or `high` that, by project policy, must be resolved before merging code.
Rationale: Externally observable as a failed build or review gate.

**Tainted input**
Definition: Data received from an external source (socket, network, file, pipe, user, or `main()` parameters) that has not yet been validated and may contain adversarial content.
Rationale: Observable from a component interface perspective — any data entering through an external interface is tainted until sanitized.

**Code complexity threshold**
Definition: A numeric limit (e.g., cyclomatic complexity ≤ 30) enforced by a metric rule. Exceeding the threshold generates a finding.
Rationale: Observable in metric reports; drives refactoring decisions.

**Coding guideline deviation**
Definition: A project-documented exception to an active rule, recorded as a Parasoft suppression annotation with justification.
Rationale: Observable through the suppression annotation in source code and review records.

### White-Box Terms (restricted to SWE.3 / SWE.4 artefacts)

**Parasoft rule attribute**
Definition: A named parameter of a specific Parasoft checker that refines its detection behaviour (e.g., `a-reportOnVariableDeclarations: true`, `d-taintedDataSourceSocket: true`).
Rationale: Internal to the static analysis tool configuration; not observable from a requirement perspective.

**Taint source category**
Definition: A Parasoft-internal classification of where tainted data originates (e.g., `taintedDataSourceSocket`, `taintedInputFiles`). Configured per rule subrule.
Rationale: Internal tool configuration detail; not observable at the component interface level.

**Subrule**
Definition: A Parasoft-specific subdivision of a rule (e.g., subrule `d` of AUTOSAR A5-2-5) that implements a distinct detection algorithm within the same rule ID.
Rationale: Internal to the Parasoft tool; not visible to external observers.

**Rule status (Active/Disabled)**
Definition: Whether a rule is switched on (Active) or off (Disabled) in the current Parasoft configuration.
Rationale: Internal tool configuration; externally only the reported findings are observable.

**NOMV / NOSECV metric**
Definition: Parasoft-internal composite metrics counting Number of Metric Violations (NOMV) and Number of Security Violations (NOSECV) aggregated across a project.
Rationale: Implementation detail of the CI quality gate configuration. SWE.1 requirements should refer to "violation count" or "finding count", not to NOMV/NOSECV by name.

**Ruleset name / version**
Definition: The internal identifier `VW.os C++14 Hosted QM 1.7.0` and version number of the Parasoft configuration package.
Rationale: Internal release management detail; requirements should refer to "the project's applicable static analysis configuration" rather than the version name.

---

## 1. Document Overview

| Field | Value |
|---|---|
| **Document title** | 1.2 - VW.os Core - C++ Parasoft Configuration Documentation |
| **Confluence space** | E3SWPAC, page ID 271657699 |
| **Ruleset name** | `VW.os C++14 Hosted QM 1.7.0` |
| **Status** | Approved |
| **Version** | 56 |
| **Last modified** | 2024-03-25 |
| **Approved** | 2024-03-26 |
| **Process** | SWE.3 - Software Detailed Design and Unit Construction |
| **Classification** | 4.2 |
| **Confidentiality** | internal (NDA + Export Control) |
| **Artifactory docs base URL** | `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/` |

> **Note**: This page was generated automatically from the Parasoft configuration. For this reason, no inline Confluence comments should be used.

---

## 2. Ruleset Subsets

The "Standard" ruleset is the one applied to all VW.os projects. In addition, the following subset rulesets exist (each omits certain rules from Standard):

| Subset name | Description |
|---|---|
| `highest` | All rules with Severity **"highest"** |
| `high` | All rules with Severity **"high"** or **"highest"** |
| `medium` | All rules with Severity **"high"**, **"highest"**, or **"medium"** |
| `NOMV` | All rules contributing to the **NOMV** metric |
| `NOSECV` | All rules contributing to the **NOSECV** metric (Security relevant = "yes") |
| `NOMV/NOSECV` | All rules contributing to either NOMV or NOSECV |

---

## 3. Package Summary

| Package | Section | Standard | Rule ID Prefix | Approx. Rule Count | Focus |
|---|---|---|---|---|---|
| AUTOSAR | 4.1 | AUTOSAR C++14 + MISRA C++ 2008 | `AUTOSAR A…` / `AUTOSAR M…` | ~280–300 | C++14 language safety, type safety, resource management, OOP, templates, exception safety, library usage |
| CERT_CPP | 4.2 | CERT C++ Coding Standard | `CERT_CPP-…` | ~8–10 | Memory safety, string safety, concurrency, signal handling |
| HICPP | 4.3 | HIC++ Standard | `HICPP-…` | ~19 | Reachability, type safety, threading/concurrency |
| SECURITY | 4.4 | VW.os security rules | `SECURITY-…` | 17 | OS/system call security, buffer overflows, privilege escalation |
| METRIC | 4.5 | Code quality metrics | `METRIC.…` | ~20+ | Cyclomatic complexity, coupling, comment ratio, fan-out |

---

## 4. Package AUTOSAR (4.1)

Rule documentation: `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/AUTOSAR.html`

Column key: **Cat** = Category (Req = Required, Adv = Advisory), **Sev** = Severity, **Sec** = Security relevant

### 4.1.1 A0 — General

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A0-1-1 | Req | No instances of non-volatile variables with unused assigned values | Active | medium | no |
| AUTOSAR A0-1-2 | Req | Return value of non-void non-overloaded-operator function shall be used | Active | medium | no |
| AUTOSAR A0-1-3 | Req | Functions shall not be unused | Active | medium | no |
| AUTOSAR A0-1-4 | Req | No unused named labels | Active | medium | no |
| AUTOSAR A0-4-1 | Req | The numeric value of a floating-point divisor shall not be zero | Active | **highest** | **yes** |
| AUTOSAR A0-4-2 | Req | Type `long double` shall not be used | Active | low | no |
| AUTOSAR A0-4-3 | Req | Linear order of arithmetic comparison of floating-point values | Active | medium | no |

### 4.1.2 A1 — Language, compiler, implementation

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A1-1-1 | Req | Code shall compile without any compiler warnings | Active | medium | no |
| AUTOSAR A1-1-2 | Req | No use of the features of the C++ language not conforming to the ISO standard | Active | medium | no |
| AUTOSAR A1-1-3 | Req | No use of the `#pragma` directive | Active | medium | no |
| AUTOSAR A1-2-1 | Req | When a third-party IP is needed, an ISO/IEC C99 or later standard shall be used | Active | medium | no |

### 4.1.3 A2 — Lexical conventions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A2-3-1 | Req | Only upper/lower ASCII characters allowed in identifiers | Active | low | no |
| AUTOSAR A2-5-1 | Req | Trigraph sequences shall not be used | Active | medium | no |
| AUTOSAR A2-5-2 | Req | Digraph sequences shall not be used | Active | medium | no |
| AUTOSAR A2-7-1 | Req | Single-line comments shall not begin with `//` unless the comment starts with code | Active | low | no |
| AUTOSAR A2-7-2 | Req | Sections of code shall not be commented out | Active | medium | no |
| AUTOSAR A2-7-3 | Adv | All declarations of "user-defined" types, static and non-static data members, functions, and methods shall be preceded by documentation comments | **Disabled** | low | no |
| AUTOSAR A2-10-1 | Req | An identifier declared in an inner scope shall not hide an identifier in an outer scope | Active | medium | no |
| AUTOSAR A2-10-2 | Req | Identifiers declared in an inner scope shall not be used to shadow an identifier in an outer scope | Active | medium | no |
| AUTOSAR A2-10-3 | Req | Type name shall be unique across the codebase | Active | medium | no |
| AUTOSAR A2-10-4 | Req | Identifier of anonymous union used in a member of the union shall not be used outside of the scope of the anonymous union | Active | medium | no |
| AUTOSAR A2-10-5 | Req | An identifier name of a function with external linkage shall be a unique identifier | **Disabled** | medium | no |
| AUTOSAR A2-10-6 | Req | A class or enumeration name shall not be hidden by a variable, function or enumerator in the same or in an enclosing scope | Active | **high** | **yes** |
| AUTOSAR A2-11-1 | Req | The `volatile` keyword shall not be used | Active | **highest** | **yes** |
| AUTOSAR A2-13-1 | Req | Only those escape sequences defined in ISO/IEC 14882:2014 shall be used | Active | medium | no |
| AUTOSAR A2-13-2 | Req | String literals with different encoding prefixes shall not be concatenated | Active | medium | no |
| AUTOSAR A2-13-3 | Req | Type used for a character represented as a numeric value shall be the smallest unsigned integer type | **Disabled** | medium | no |
| AUTOSAR A2-13-4 | Req | String literals shall not be assigned to non-const pointers | Active | low | no |
| AUTOSAR A2-13-5 | Req | Hexadecimal constants shall be uppercase | Active | medium | no |
| AUTOSAR A2-13-6 | Req | Universal character names shall not be used in character and non-wide string literals | Active | medium | no |

### 4.1.4 A3 — Source file organization

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A3-1-1 | Req | It shall be possible to include any header file in multiple translation units without violating the One Definition Rule | Active | **high** | **yes** |
| AUTOSAR A3-1-2 | Req | Header files, that are defined locally in the project, shall have a file name extension of one of: `.h`, `.hpp`, or `.hxx` | **Disabled** | medium | no |
| AUTOSAR A3-1-3 | Adv | Implementation files should have a file name extension of `.cpp` | **Disabled** | low | no |
| AUTOSAR A3-1-4 | Req | When an array with external linkage is declared, its size shall be stated explicitly | Active | medium | no |
| AUTOSAR A3-1-5 | Req | A function definition shall only be placed in a class definition if: (1) intended to be inlined, (2) a member function template, (3) member function of a class template | Active | low | no |
| AUTOSAR A3-3-1 | Req | Objects or functions with external linkage (including members of named namespaces) shall be declared in a header file | Active | medium | no |
| AUTOSAR A3-3-2 | Req | Static and thread-local objects shall be constant-initialized | **Disabled** | low | no |
| AUTOSAR A3-8-1 | Req | An object shall not be accessed outside of its lifetime | Active | **highest** | **yes** |

### 4.1.5 A4 — Expressions (type safety)

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A4-5-1 | Req | Expressions with type `enum` or `enum class` shall not be used as operands to built-in operators other than `[]`, `=`, `==`, `!=`, unary `&`, and relational operators | Active | medium | no |
| AUTOSAR A4-7-1 | Req | An integer expression shall not lead to data loss | Active | medium | no |
| AUTOSAR A4-10-1 | Req | Only `nullptr` literal shall be used as the null-pointer-constant | Active | medium | no |

### 4.1.6 A5 — Statements and expressions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A5-0-1 | Req | Expression value shall be same under any order of evaluation | Active | medium | no |
| AUTOSAR A5-0-2 | Req | `if`/iteration condition shall have type `bool` | Active | medium | no |
| AUTOSAR A5-0-3 | Req | Max two levels of pointer indirection | Active | low | no |
| AUTOSAR A5-0-4 | Req | Pointer arithmetic not with pointers to non-final classes | Active | medium | no |
| AUTOSAR A5-1-2 | Req | Variables shall not be implicitly captured in a lambda expression | Active | medium | no |
| AUTOSAR A5-1-3 | Req | Parameter list (possibly empty) shall be included in every lambda expression | Active | low | no |
| AUTOSAR A5-1-4 | Req | A lambda expression object shall not outlive any of its reference-captured objects | Active | **highest** | **yes** |
| AUTOSAR A5-1-6 | Adv | Return type of a non-void lambda should be explicitly specified | Active | low | no |
| AUTOSAR A5-1-7 | Req | A lambda shall not be an operand to `decltype` or `typeid` | Active | medium | no |
| AUTOSAR A5-1-8 | Adv | Lambda expressions should not be defined inside another lambda expression | Active | low | no |
| AUTOSAR A5-2-1 | Adv | `dynamic_cast` should not be used | Active | low | no |
| AUTOSAR A5-2-2 | Req | Traditional C-style casts shall not be used | Active | medium | no |
| AUTOSAR A5-2-3 | Req | A cast shall not remove any `const` or `volatile` qualification | Active | medium | no |
| AUTOSAR A5-2-4 | Req | `reinterpret_cast` shall not be used | Active | medium | no |
| AUTOSAR A5-2-5 | Req | An array or container shall not be accessed beyond its range | Active | **highest** | **yes** |
| AUTOSAR A5-2-6 | Req | Operands of `&&` or `\|\|` shall be parenthesized if they contain binary operators | Active | low | no |
| AUTOSAR A5-3-1 | Req | Evaluation of `typeid` operand shall not contain side effects | Active | medium | no |
| AUTOSAR A5-3-2 | Req | Null pointers shall not be dereferenced | Active | **highest** | **yes** |
| AUTOSAR A5-3-3 | Req | Pointers to incomplete class types shall not be deleted | Active | medium | no |
| AUTOSAR A5-5-1 | Req | A pointer to member shall not access non-existent class members | Active | medium | no |
| AUTOSAR A5-6-1 | Req | RHS of integer division or remainder operators shall not be zero | Active | **highest** | **yes** |
| AUTOSAR A5-10-1 | Req | Pointer-to-member-virtual-function tested for equality only with `nullptr` | Active | medium | no |
| AUTOSAR A5-16-1 | Req | Ternary conditional operator shall not be used as a sub-expression | Active | medium | no |

### 4.1.7 A6 — Statements (control flow)

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A6-2-1 | Req | Move/copy assignment operators shall move/copy all base classes and data members | Active | medium | no |
| AUTOSAR A6-2-2 | Req | Expression statements shall not be explicit calls to constructors of temporary objects only | Active | **highest** | **yes** |
| AUTOSAR A6-4-1 | Req | A switch statement shall have at least two case-clauses, distinct from the default label | Active | low | no |
| AUTOSAR A6-5-1 | Req | A range-based for shall not be used if the loop needs its loop-counter | Active | medium | no |
| AUTOSAR A6-5-2 | Req | A for loop shall contain a single non-float loop-counter | Active | medium | no |
| AUTOSAR A6-5-3 | Adv | `do` statements should not be used | Active | low | no |
| AUTOSAR A6-5-4 | Adv | `for` init-statement and expression should only perform loop-counter init/modification | Active | low | no |
| AUTOSAR A6-6-1 | Req | The `goto` statement shall not be used | Active | medium | no |

### 4.1.8 A7 — Declarations and definitions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A7-1-2 | Req | The `constexpr` specifier shall be used for values that can be determined at compile time | Active | medium | no |
| AUTOSAR A7-1-4 | Req | The `register` keyword shall not be used | Active | medium | no |
| AUTOSAR A7-1-5 | Req | `auto` specifier only in specified permitted cases | Active | medium | no |
| AUTOSAR A7-1-6 | Req | The `typedef` specifier shall not be used | Active | low | no |
| AUTOSAR A7-1-7 | Req | Each expression statement and identifier declaration shall be placed on a separate line | Active | low | no |
| AUTOSAR A7-1-8 | Req | A non-type specifier shall be placed before a type specifier in a declaration | Active | low | no |
| AUTOSAR A7-1-9 | Req | A class, structure, or enumeration shall not be declared in the definition of its type | Active | low | no |
| AUTOSAR A7-2-1 | Req | Enum expression shall only have values corresponding to the enumeration's enumerators | Active | medium | no |
| AUTOSAR A7-2-2 | Req | Enumeration underlying base type shall be explicitly defined | Active | medium | no |
| AUTOSAR A7-2-3 | Req | Enumerations shall be declared as scoped `enum class` | Active | medium | no |
| AUTOSAR A7-2-4 | Req | In an enumeration, either none, the first, or all enumerators shall be initialized | Active | low | no |
| AUTOSAR A7-2-5 | Adv | Enumerations should represent sets of related named constants | Active | low | no |
| AUTOSAR A7-3-1 | Req | All overloads of a function shall be visible from the call site | Active | medium | no |
| AUTOSAR A7-4-1 | Req | The `asm` declaration shall not be used | Active | medium | no |
| AUTOSAR A7-5-1 | Req | A function shall not return a reference or pointer to a `const` reference parameter | Active | medium | no |
| AUTOSAR A7-5-2 | Req | Functions shall not call themselves (directly or indirectly) | Active | medium | no |
| AUTOSAR A7-6-1 | Req | Functions declared with `[[noreturn]]` shall not return | Active | medium | no |

### 4.1.9 A8 — Declarators, parameters, initialization

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A8-2-1 | Req | Trailing return type syntax when return type depends on parameter types | Active | low | no |
| AUTOSAR A8-4-1 | Req | Functions shall not be defined using the ellipsis notation | Active | medium | no |
| AUTOSAR A8-4-2 | Req | All exit paths from a function with non-void return type shall have explicit `return` | Active | **highest** | **yes** |
| AUTOSAR A8-4-4 | Adv | Multiple output values should be returned as a struct or tuple | **Disabled** | low | no |
| AUTOSAR A8-4-5 | Req | `X&&` "consume" parameters shall always be moved from | Active | low | no |
| AUTOSAR A8-4-6 | Req | `T&&` "forward" parameters shall always be forwarded | Active | low | no |
| AUTOSAR A8-4-7 | Req | "Cheap to copy" `in` parameters passed by value | Active | low | no |
| AUTOSAR A8-4-8 | Req | Output parameters shall not be used | **Disabled** | low | no |
| AUTOSAR A8-4-9 | Req | `T&` "in-out" parameters shall be modified | Active | medium | no |
| AUTOSAR A8-4-10 | Req | A parameter shall be passed by reference if it can't be NULL | Active | medium | no |
| AUTOSAR A8-4-11 | Req | A smart pointer shall only be a parameter if it expresses lifetime semantics | Active | low | no |
| AUTOSAR A8-4-12 | Req | `std::unique_ptr` passed as copy (ownership transfer) or lvalue ref (replacement) | Active | low | no |
| AUTOSAR A8-4-13 | Req | `std::shared_ptr` passed as copy, lvalue ref, or const lvalue ref | Active | low | no |
| AUTOSAR A8-5-0 | Req | All memory shall be initialized before it is read | Active | medium | no |
| AUTOSAR A8-5-1 | Req | Initialization list order: virtual bases → direct bases → non-static data members | Active | medium | no |
| AUTOSAR A8-5-2 | Req | Braced-initialization `{}` without `=` shall be used for variable initialization | **Disabled** | medium | no |
| AUTOSAR A8-5-3 | Req | A variable of type `auto` shall not be initialized using `{}` or `={}` | Active | low | no |
| AUTOSAR A8-5-4 | Adv | Class with `initializer_list` constructor should have it as only non-special constructor | **Disabled** | low | no |

### 4.1.10 A9 — Classes and structs

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A9-3-1 | Req | Member functions shall not return non-const raw pointers/refs to private/protected data | Active | medium | no |
| AUTOSAR A9-5-1 | Req | Unions shall not be used | Active | medium | no |
| AUTOSAR A9-6-1 | Req | Hardware/protocol interface types shall be trivial, standard-layout, fixed-size members | Active | medium | no |
| AUTOSAR A9-6-2 | Req | Bit-fields shall be used only when interfacing to hardware or conforming to protocols | Active | low | no |

### 4.1.11 A10 — Derived classes

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A10-1-1 | Req | Class shall not be derived from more than one non-interface base class | Active | medium | no |
| AUTOSAR A10-2-1 | Req | Non-virtual member functions shall not be redefined in derived classes | Active | **high** | **yes** |
| AUTOSAR A10-3-1 | Req | Virtual function declaration shall contain exactly one of: `virtual`, `override`, `final` | Active | medium | no |
| AUTOSAR A10-3-2 | Req | Each overriding virtual function shall be declared with `override` or `final` | Active | medium | no |
| AUTOSAR A10-3-3 | Req | Virtual functions shall not be introduced in a `final` class | Active | medium | no |
| AUTOSAR A10-3-5 | Req | A user-defined assignment operator shall not be `virtual` | Active | medium | no |
| AUTOSAR A10-4-1 | Adv | Hierarchies should be based on interface classes | Active | low | no |

### 4.1.12 A11 — Member access control and special member functions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A11-0-1 | Adv | A non-POD type should be defined as `class` | Active | low | no |
| AUTOSAR A11-0-2 | Req | A struct shall: only public data members, no special member functions, not be a base, not inherit | Active | medium | no |
| AUTOSAR A11-3-1 | Req | Friend declarations shall not be used | Active | medium | no |

### 4.1.13 A12 — Special member functions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A12-0-1 | Req | Rule of Five: if any of copy/move/destructor declared, all five shall be declared | Active | medium | no |
| AUTOSAR A12-0-2 | Req | Bitwise operations shall not be performed on objects | Active | medium | no |
| AUTOSAR A12-1-1 | Req | Constructors shall explicitly initialize all virtual base classes, non-virtual direct base classes, and non-static data members | Active | medium | no |
| AUTOSAR A12-1-2 | Req | Both NSDMI and member initializer list shall not be used in the same type | Active | medium | no |
| AUTOSAR A12-1-3 | Req | If all user-defined constructors of a class initialize data members with the same constant values, use NSDMI | **Disabled** | medium | no |
| AUTOSAR A12-1-4 | Req | All constructors that are callable with a single argument of fundamental type shall be declared explicit | Active | medium | no |
| AUTOSAR A12-1-5 | Req | Common class initialization should be done by delegating constructor | Active | medium | no |
| AUTOSAR A12-1-6 | Req | Derived classes that do not need further explicit initialization and require all constructors from a non-virtual base class shall use inheriting constructors | **Disabled** | medium | no |
| AUTOSAR A12-4-1 | Req | Destructor of a base class shall be either public virtual or protected non-virtual | Active | medium | no |
| AUTOSAR A12-4-2 | Adv | If a public destructor of a class is non-virtual, then the class should be declared final | Active | low | no |
| AUTOSAR A12-6-1 | Req | All class data members that are initialized by the constructor shall be initialized using member initializers | Active | medium | no |
| AUTOSAR A12-7-1 | Req | If the behavior of a user-defined special member function is identical to implicitly defined function, then it shall be defined `=default` or not defined at all | Active | medium | no |
| AUTOSAR A12-8-1 | Req | Move and copy constructors shall move or copy base classes and data members of a class, without any side effects | Active | medium | no |
| AUTOSAR A12-8-2 | Adv | User-defined copy and move assignment operators should use the copy-and-swap idiom | **Disabled** | low | no |
| AUTOSAR A12-8-3 | Req | Moved-from objects shall not be read-accessed | Active | **highest** | **yes** |
| AUTOSAR A12-8-4 | Req | Move constructor shall not initialize its class members using copy semantics | Active | medium | no |
| AUTOSAR A12-8-5 | Req | A copy assignment operator shall handle self-assignment | Active | **high** | **yes** |
| AUTOSAR A12-8-6 | Req | Copy and move constructors and copy assignment and move assignment operators in base class shall be non-public or `=delete` | Active | medium | no |
| AUTOSAR A12-8-7 | Adv | Assignment operators should be declared with the ref-qualifier `&` | Active | low | no |

### 4.1.14 A13 — Overloading and UDL

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A13-1-2 | Req | User-defined literal operators shall only perform conversions of passed parameters | Active | medium | no |
| AUTOSAR A13-1-3 | Req | User-defined literal operators shall only perform conversions | Active | low | no |
| AUTOSAR A13-2-1 | Req | An assignment operator shall return a reference to "this" | Active | medium | no |
| AUTOSAR A13-2-2 | Req | A binary arithmetic or bitwise operator shall return a prvalue | Active | medium | no |
| AUTOSAR A13-2-3 | Req | A relational operator shall return a boolean | Active | medium | no |
| AUTOSAR A13-3-1 | Req | A function that contains a forwarding reference as its argument shall not be overloaded | Active | **high** | **yes** |
| AUTOSAR A13-5-1 | Req | If `operator[]` is to be overloaded with a non-const version, a const version shall be implemented as well | Active | medium | no |
| AUTOSAR A13-5-2 | Req | All user-defined conversion operators shall be defined explicit | Active | **high** | **yes** |
| AUTOSAR A13-5-3 | Adv | User-defined conversion operators should not be used | Active | low | no |
| AUTOSAR A13-5-4 | Req | If two opposite operators are defined, one shall be defined in terms of the other | Active | medium | no |
| AUTOSAR A13-5-5 | Req | Comparison operators shall be non-member, take identical parameter types, and be `noexcept` | Active | medium | no |
| AUTOSAR A13-6-1 | Req | Digit separators `'` shall only be used as follows: decimal every 3, hex every 2, binary every 4 | Active | medium | no |

### 4.1.15 A14 — Templates

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A14-5-1 | Req | A template constructor shall not participate in overload resolution for a copy or move constructor of the forwarding reference type | Active | **high** | **yes** |
| AUTOSAR A14-5-3 | Adv | A non-member generic operator for a type T shall only be declared in the namespace containing T | **Disabled** | low | no |
| AUTOSAR A14-7-2 | Req | Template specialization shall be declared in the same file as the primary template or in the file that declares the user-defined type | Active | medium | no |
| AUTOSAR A14-8-2 | Req | Explicit specializations of function templates shall not be used | Active | medium | no |

### 4.1.16 A15 — Exception handling

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A15-0-2 | Req | At least basic exception safety shall be provided for all operations | Active | medium | no |
| AUTOSAR A15-1-1 | Adv | Only instances of types derived from `std::exception` should be thrown | Active | low | no |
| AUTOSAR A15-1-2 | Req | An exception object shall not be a pointer | Active | medium | no |
| AUTOSAR A15-1-4 | Req | If a function is declared to be noexcept, noexcept(true) or noexcept(<true condition>), then it shall not exit with an exception. All objects and resources shall be in a valid state or deleted before the exception is thrown | Active | **highest** | **yes** |
| AUTOSAR A15-2-1 | Req | Constructors that are not noexcept shall not be invoked before program startup | Active | medium | no |
| AUTOSAR A15-3-2 | Req | If a function is not declared noexcept, it shall not exit with an uncaught exception | Active | medium | no |
| AUTOSAR A15-3-3 | Req | Main function and a task main function shall catch at least: base class exceptions, std::exception, and all otherwise unhandled exception types | Active | medium | no |
| AUTOSAR A15-3-4 | Req | Catch-all (ellipsis and std::exception) handlers shall be used only in main, task main functions, in the functions that are supposed to isolate independent components, and when calling third-party code that uses exceptions | Active | medium | no |
| AUTOSAR A15-3-5 | Req | A class type exception shall be caught by reference or const reference | Active | medium | no |
| AUTOSAR A15-4-1 | Req | Dynamic exception-specification shall not be used | Active | **high** | **yes** |
| AUTOSAR A15-4-2 | Req | If a function is declared to be noexcept, noexcept(true), it shall not exit with an exception | Active | **highest** | **yes** |
| AUTOSAR A15-4-3 | Req | The noexcept specification of a function shall either be identical across all translation units, or more restrictive in the overriding virtual function | Active | medium | no |
| AUTOSAR A15-4-5 | Req | Checked exceptions that could be thrown from a function shall be specified together with the function declaration | **Disabled** | medium | no |
| AUTOSAR A15-5-1 | Req | All user-provided class destructors, deallocation functions, `move` constructors, `move` assignment operators, and `swap` functions shall not exit with an exception | Active | medium | no |
| AUTOSAR A15-5-2 | Req | Program shall not be abruptly terminated | Active | medium | no |
| AUTOSAR A15-5-3 | Req | The `std::terminate()` function shall not be called implicitly | Active | medium | no |

### 4.1.17 A16 — Preprocessing directives

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A16-2-1 | Req | The `'`, `"`, `/*`, `//` characters shall not appear in a header file name | Active | medium | no |
| AUTOSAR A16-2-2 | Req | There shall be no unused `#include` directives | Active | medium | no |
| AUTOSAR A16-6-1 | Req | `#error` directive shall not be used | Active | medium | no |
| AUTOSAR A16-7-1 | Req | `#pragma` directive shall not be used | Active | medium | no |

### 4.1.18 A17–A19 — Identifiers, library usage, standard C library

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A17-0-1 | Req | Reserved identifiers, macros, and functions in the C standard library shall not be defined, redefined, or undefined | Active | medium | no |
| AUTOSAR A17-1-1 | Req | Use of the C standard library shall be encapsulated and isolated | Active | medium | no |
| AUTOSAR A17-6-1 | Req | Non-standard entities shall not be added to standard namespaces | Active | medium | no |
| AUTOSAR A18-0-1 | Req | The C library facilities shall only be accessed through C++ library headers | Active | medium | no |
| AUTOSAR A18-0-2 | Req | The error state of a conversion from string to a numeric value shall be checked | Active | **high** | **yes** |
| AUTOSAR A18-0-3 | Req | The `clocale` header and the `setlocale` function shall not be used | Active | medium | no |
| AUTOSAR A18-1-1 | Req | C-style arrays shall not be used | Active | medium | no |
| AUTOSAR A18-1-2 | Req | `std::vector<bool>` specialization shall not be used | Active | medium | no |
| AUTOSAR A18-1-3 | Req | `std::auto_ptr` shall not be used | Active | medium | no |

### 4.1.19 A26–A27 — Input/output

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR A27-0-1 | Req | Inputs from independent components shall be validated (with taint analysis sub-rules for socket, files, network, pipes, system, user, and main parameters) | Active | medium | no |
| AUTOSAR A27-0-2 | Adv | A C-string shall guarantee sufficient space for data and the null terminator | **Disabled** | low | no |
| AUTOSAR A27-0-3 | Req | Alternate input and output operations on a file stream shall not be performed without an intervening flush or positioning call | Active | medium | no |
| AUTOSAR A27-0-4 | Req | C-style strings shall not be used | **Disabled** | medium | no |

### 4.1.20 AUTOSAR M0 — Project-level, correctness

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M0-1-1 | Req | A project shall not contain unreachable code | Active | medium | no |
| AUTOSAR M0-1-2 | Req | A project shall not contain infeasible paths | Active | medium | no |
| AUTOSAR M0-1-3 | Req | A project shall not contain unused variables | Active | low | no |
| AUTOSAR M0-1-8 | Req | All functions with void return type shall have external side effects | Active | medium | no |
| AUTOSAR M0-1-9 | Req | There shall be no dead code | Active | medium | no |
| AUTOSAR M0-2-1 | Req | An object shall not be assigned to an overlapping object | Active | medium | no |
| AUTOSAR M0-3-1 | Req | Minimize the possibility of run-time failures (static analysis, dynamic analysis, explicit checks) | Active | medium | no |
| AUTOSAR M0-3-2 | Req | If a function generates error information, then that error information shall be tested | Active | **high** | **yes** |
| AUTOSAR M0-4-2 | Req | Use of floating-point arithmetic shall be documented | Active | medium | no |

### 4.1.21 AUTOSAR M2 — Lexical conventions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M2-7-1 | Req | The character sequence `/*` shall not be used within a C-style comment | Active | **high** | **yes** |
| AUTOSAR M2-13-2 | Req | Octal constants (other than zero) shall not be used | Active | low | no |
| AUTOSAR M2-13-3 | Req | A U suffix shall be applied to all octal or hexadecimal integer literals of unsigned type | Active | medium | no |
| AUTOSAR M2-13-4 | Req | Literal suffixes shall be upper case | Active | low | no |

### 4.1.22 AUTOSAR M3 — Declarations and definitions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M3-1-2 | Req | Functions shall not be declared at block scope | Active | medium | no |
| AUTOSAR M3-2-1 | Req | All declarations of an object or function shall have compatible types | Active | medium | no |
| AUTOSAR M3-2-2 | Req | The One Definition Rule shall not be violated | Active | **highest** | **yes** |
| AUTOSAR M3-2-3 | Req | A type, object or function that is used in multiple translation units shall be declared in one and only one file | Active | **high** | **yes** |
| AUTOSAR M3-2-4 | Req | An identifier with external linkage shall have exactly one definition | Active | **highest** | **yes** |
| AUTOSAR M3-3-2 | Req | If a function has internal linkage then all re-declarations shall include the static storage class specifier | Active | low | no |
| AUTOSAR M3-4-1 | Req | An identifier declared to be an object or type shall be defined in a block that minimizes its visibility | Active | low | no |
| AUTOSAR M3-9-1 | Req | The types used for an object, a function return type, or a function parameter shall be token-for-token identical in all declarations and re-declarations | Active | **high** | **yes** |
| AUTOSAR M3-9-3 | Req | The underlying bit representations of floating-point values shall not be used | Active | medium | no |

### 4.1.23 AUTOSAR M4 — Expressions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M4-5-1 | Req | Expressions of type `bool` shall only be used as bool operands (`=`, `&&`, `\|\|`, `!`, `==`, `!=`, bitwise-AND, ternary) | Active | medium | no |
| AUTOSAR M4-5-3 | Req | Expressions of type `char` and `wchar_t` shall only be used with operators `=`, `==`, `!=`, `&` | Active | medium | no |

### 4.1.24 AUTOSAR M6 — Statements

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M6-4-4 | Req | A switch-label shall only be used when the most closely-enclosing compound statement is the body of a switch statement | Active | medium | no |
| AUTOSAR M6-4-5 | Req | An unconditional throw or break statement shall terminate every non-empty switch-clause | **Disabled** | medium | no |
| AUTOSAR M6-4-6 | Req | The final clause of a switch statement shall be the default-clause | Active | medium | no |
| AUTOSAR M6-4-7 | Req | The condition of a switch statement shall not have bool type | Active | low | no |
| AUTOSAR M6-5-2 | Req | If loop-counter is not modified by `--` or `++`, then, within condition, the loop-counter shall only be used as an operand to `<=`, `<`, `>`, `>=` | Active | medium | no |
| AUTOSAR M6-5-3 | Req | The loop-counter shall not be modified within condition or statement | Active | medium | no |
| AUTOSAR M6-5-4 | Req | The loop-counter shall be modified by one of: `--`, `++`, `-=n`, or `+=n` | Active | medium | no |
| AUTOSAR M6-5-5 | Req | A loop-control-variable other than the loop-counter shall not be modified within condition or expression | Active | medium | no |
| AUTOSAR M6-5-6 | Req | A loop-control-variable which is modified in statement shall have type bool | Active | medium | no |
| AUTOSAR M6-6-1 | Req | Any label referenced by a goto statement shall be declared in the same block, or in a block enclosing the goto statement | Active | medium | no |
| AUTOSAR M6-6-2 | Req | The goto statement shall jump to a label declared later in the same function | Active | medium | no |
| AUTOSAR M6-6-3 | Req | The continue statement shall only be used within a well-formed for loop | Active | medium | no |

### 4.1.25 AUTOSAR M7 — Declarations

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M7-1-2 | Req | A pointer or reference parameter in a function shall be declared as pointer to const or reference to const if the corresponding object is not modified | Active | medium | no |
| AUTOSAR M7-3-1 | Req | The global namespace shall only contain `main`, namespace declarations, and `extern "C"` declarations | Active | medium | no |
| AUTOSAR M7-3-2 | Req | The identifier `main` shall not be used for a function other than the global function `main` | Active | **high** | **yes** |
| AUTOSAR M7-3-3 | Req | There shall be no unnamed namespaces in header files | Active | **highest** | **yes** |
| AUTOSAR M7-3-4 | Req | Using-directives shall not be used | **Disabled** | medium | no |
| AUTOSAR M7-3-6 | Req | Using-directives and using-declarations (excluding class scope or function scope using-declarations) shall not be used in header files | Active | medium | no |
| AUTOSAR M7-4-1 | Req | All usage of assembler shall be documented | Active | medium | no |
| AUTOSAR M7-4-2 | Req | Assembler instructions shall only be introduced using the `asm` declaration | Active | medium | no |
| AUTOSAR M7-4-3 | Req | Assembly language shall be encapsulated and isolated | Active | medium | no |
| AUTOSAR M7-5-1 | Req | A function shall not return a reference or a pointer to an automatic variable | Active | medium | no |
| AUTOSAR M7-5-2 | Req | The address of an object with automatic storage shall not be assigned to another object that may persist after the first object has ceased to exist | Active | **highest** | **yes** |

### 4.1.26 AUTOSAR M8 — Definitions

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M8-0-1 | Req | An init-declarator-list or a member-declarator-list shall consist of a single init-declarator or member-declarator respectively | Active | low | no |
| AUTOSAR M8-3-1 | Req | Parameters in an overriding virtual function shall either use the same default arguments as the function they override, or else shall not specify any default arguments | Active | **high** | **yes** |
| AUTOSAR M8-4-2 | Req | The identifiers used for the parameters in a re-declaration of a function shall be identical to those in the declaration | Active | low | no |
| AUTOSAR M8-4-4 | Req | A function identifier shall either be used to call the function or it shall be preceded by `&` | Active | low | no |
| AUTOSAR M8-5-2 | Req | Braces shall be used to indicate and match the structure in the non-zero initialization of arrays and structures | Active | medium | no |

### 4.1.27 AUTOSAR M9, M10, M12 — Classes, inheritance

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M9-3-1 | Req | Const member functions shall not return non-const pointers or references to class data | Active | medium | no |
| AUTOSAR M9-3-3 | Req | If a member function can be made static then it shall be made static, otherwise if it can be made const then it shall be made const | Active | medium | no |
| AUTOSAR M9-6-4 | Req | Named bit-fields with signed integer type shall have a length of more than one bit | Active | medium | no |
| AUTOSAR M10-1-1 | Adv | Classes should not be derived from virtual bases | Active | low | no |
| AUTOSAR M10-1-2 | Req | A base class shall only be declared virtual if it is used in a diamond hierarchy | Active | medium | no |
| AUTOSAR M10-1-3 | Req | An accessible base class shall not be both virtual and non-virtual in the same hierarchy | Active | medium | no |
| AUTOSAR M10-2-1 | Adv | All accessible entity names within a multiple inheritance hierarchy should be unique | Active | **high** | **yes** |
| AUTOSAR M10-3-3 | Req | A virtual function shall only be overridden by a pure virtual function if it is itself declared as pure virtual | Active | low | no |
| AUTOSAR M12-1-1 | Req | An object's dynamic type shall not be used from the body of its constructor or destructor | Active | **highest** | **yes** |

### 4.1.28 AUTOSAR M14–M16 — Templates, exception handling, preprocessing

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M14-5-3 | Req | A copy assignment operator shall be declared when there is a template assignment operator with a parameter that is a generic parameter | Active | **high** | **yes** |
| AUTOSAR M14-6-1 | Req | In a class template with a dependent base, any name that may be found in that dependent base shall be referred to using a qualified-id or `this->` | Active | medium | no |
| AUTOSAR M15-0-3 | Req | Control shall not be transferred into a try or catch block using a goto or a switch statement | Active | medium | no |
| AUTOSAR M15-1-1 | Req | The assignment-expression of a throw statement shall not itself cause an exception to be thrown | Active | medium | no |
| AUTOSAR M15-1-2 | Req | NULL shall not be thrown explicitly | Active | medium | no |
| AUTOSAR M15-1-3 | Req | An empty throw (throw;) shall only be used in the compound-statement of a catch handler | Active | **high** | **yes** |
| AUTOSAR M15-3-1 | Req | Exceptions shall be raised only after start-up and before termination of the program | Active | medium | no |
| AUTOSAR M15-3-3 | Req | Handlers of a function-try-block implementation of a class constructor or destructor shall not reference non-static members from this class or its bases | Active | medium | no |
| AUTOSAR M15-3-4 | Req | Each exception explicitly thrown in the code shall have a handler of a compatible type in all call paths that could lead to that point | Active | medium | no |
| AUTOSAR M15-3-6 | Req | Where multiple handlers are provided in a single try-catch statement or function-try-block, any ellipsis (catch-all) handler shall occur last | Active | medium | no |
| AUTOSAR M15-3-7 | Req | Where multiple handlers are provided in a single try-catch statement, the most derived class shall be handled first | Active | medium | no |
| AUTOSAR M16-0-1 | Req | `#include` directives in a file shall only be preceded by other preprocessor directives or comments | Active | medium | no |
| AUTOSAR M16-0-2 | Req | Macros shall only be `#define`'d or `#undef`'d in the global namespace | Active | low | no |
| AUTOSAR M16-0-5 | Req | Arguments to a function-like macro shall not contain tokens that look like preprocessing directives | **Disabled** | medium | no |
| AUTOSAR M16-0-6 | Req | In the definition of a function-like macro, each instance of a parameter shall be enclosed in parentheses | **Disabled** | medium | no |
| AUTOSAR M16-0-7 | Req | Undefined macro identifiers shall not be used in `#if` or `#elif` preprocessor directives, except as operands to the defined operator | **Disabled** | medium | no |
| AUTOSAR M16-0-8 | Req | If the `#` token appears as the first token on a line, then it shall be immediately followed by a preprocessing token | Active | medium | no |
| AUTOSAR M16-1-1 | Req | The `defined` preprocessor operator shall only be used in one of the two standard forms | **Disabled** | medium | no |
| AUTOSAR M16-1-2 | Req | All `#else`, `#elif`, and `#endif` preprocessor directives shall reside in the same file as the `#if`, `#ifdef`, or `#ifndef` directive to which they are related | **Disabled** | medium | no |
| AUTOSAR M16-2-3 | Req | Include guards shall be provided | Active | **high** | **yes** |
| AUTOSAR M16-3-1 | Req | There shall be at most one occurrence of the `#` or `##` operators in a single macro definition | **Disabled** | medium | no |
| AUTOSAR M16-3-2 | Adv | The `#` and `##` operators should not be used | Active | medium | no |

### 4.1.29 AUTOSAR M17–M19, M27 — Standard library, C standard library

| Rule ID | Cat | Description | Status | Sev | Sec |
|---|---|---|---|---|---|
| AUTOSAR M17-0-2 | Req | The names of standard library macros and objects shall not be reused | Active | medium | no |
| AUTOSAR M17-0-3 | Req | The names of standard library functions shall not be overridden | Active | medium | no |
| AUTOSAR M17-0-5 | Req | The `setjmp` macro and the `longjmp` function shall not be used | Active | medium | no |
| AUTOSAR M18-0-3 | Req | The library functions `abort`, `exit`, `getenv`, and `system` from `<cstdlib>` shall not be used | Active | medium | no |
| AUTOSAR M18-0-4 | Req | The time handling functions of library `<ctime>` shall not be used | Active | medium | no |
| AUTOSAR M18-0-5 | Req | The unbounded functions of library `<cstring>` shall not be used | Active | medium | no |
| AUTOSAR M18-2-1 | Req | The macro `offsetof` shall not be used | Active | medium | no |
| AUTOSAR M18-7-1 | Req | The signal handling facilities of `<csignal>` shall not be used | **Disabled** | medium | no |
| AUTOSAR M19-3-1 | Req | The error indicator `errno` shall not be used | Active | medium | no |
| AUTOSAR M27-0-1 | Req | The stream input/output library `<cstdio>` shall not be used | Active | medium | no |

---

## 5. Package CERT_CPP (4.2)

Rule documentation: `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/CERT_CPP.html`

CERT_CPP rules have no Required/Advisory distinction in the column structure used for AUTOSAR. Most are Disabled; only a few are Active.

| Rule ID | Description | Status | Sev | Sec |
|---|---|---|---|---|
| CERT_CPP-CON50 | Do not destroy a mutex while it is locked | **Disabled** | medium | no |
| CERT_CPP-MEM50 | Do not access freed memory | Active | medium | no |
| CERT_CPP-MSC54 | A signal handler must be a plain old function | **Disabled** | medium | no |
| CERT_CPP-OOP50 | Do not invoke virtual functions from constructors or destructors | **Disabled** | medium | no |
| CERT_CPP-STR50 | Guarantee that storage for strings has sufficient space for character data and the null terminator | Active | low | no |
| CERT_CPP-STR51 | Do not attempt to create a `std::string` from a null pointer | Active | medium | no |
| CERT_CPP-STR52 | Use valid references, pointers, and iterators to reference elements of a `basic_string` | **Disabled** | medium | no |
| CERT_CPP-STR53 | Range check element access | **Disabled** | medium | no |

> **Notes**: CON50, MSC54, OOP50 are Disabled because the corresponding AUTOSAR/HICPP rules already cover these areas. STR52 and STR53 are Disabled to avoid duplicating coverage from AUTOSAR array-bounds rules.

---

## 6. Package HICPP (4.3)

Rule documentation: `https://jfrog.devstack.vwgroup.com/artifactory/e3-e3sp-documents-release/e3-e3sp-documentation/parasoft/HICPP.html`

This package is strongly focused on **thread safety** (rules 18_x). Early rules 1–15 are mostly Disabled; nearly all 18_x threading rules are Active.

| Rule ID | Description | Status | Sev | Sec |
|---|---|---|---|---|
| HICPP-1_2_1 | Ensure all statements are reachable | **Disabled** | medium | no |
| HICPP-3_5_1 | Do not make assumptions about the internal representation of a value | **Disabled** | low | no |
| HICPP-4_2_2 | Ensure that data loss does not demonstrably occur in an integral expression | **Disabled** | medium | no |
| HICPP-5_2_1 | Ensure that pointer or array access is demonstrably within bounds of a valid object | **Disabled** | medium | no |
| HICPP-5_4_3 | Do not convert from a pointer to a base class to a pointer to a derived class | **Disabled** | medium | no |
| HICPP-5_5_1 | Ensure that the right-hand operand of the division or remainder operator is demonstrably non-zero | **Disabled** | medium | no |
| HICPP-7_4_1 | Objects that need only be accessible to functions in a single translation unit should be defined in an unnamed namespace in that file | **Disabled** | medium | no |
| HICPP-8_4_1 | Do not access an invalid object or an indeterminate value | Active | low | no |
| HICPP-12_4_1 | Do not use an object's dynamic type during construction or destruction | **Disabled** | medium | no |
| HICPP-15_1_1 | Only instances of types derived from `std::exception` should be thrown | **Disabled** | medium | no |
| HICPP-15_3_2 | The program code shall not result in a call to `std::terminate()` | **Disabled** | medium | no |
| HICPP-18_1_1 | Do not use platform-specific multi-threading facilities | Active | medium | no |
| HICPP-18_2_2 | Shared data that can be accessed from multiple threads shall be synchronized using a single lock | Active | **high** | **yes** |
| HICPP-18_2_4 | Use `std::call_once` instead of the Double-Checked Locking pattern | Active | **high** | **yes** |
| HICPP-18_3_1 | No static path of execution results in the same mutex being locked twice within a lock scope | Active | **high** | **yes** |
| HICPP-18_3_2 | The nesting order of locks in a program shall form a DAG (no lock cycles) | Active | **high** | **yes** |
| HICPP-18_3_3 | Do not use `std::recursive_mutex` | Active | medium | no |
| HICPP-18_3_4 | Use `std::unique_lock` instead of `std::lock_guard` only if the former's additional functionality is needed | Active | medium | no |
| HICPP-18_3_5 | Do not access members of `std::mutex` directly | Active | medium | no |
| HICPP-18_3_6 | Do not use relaxed (non-sequentially-consistent) atomics | Active | **high** | **yes** |
| HICPP-18_4_1 | Do not use `std::condition_variable_any` with `std::mutex` | Active | medium | no |

---

## 7. Package SECURITY (4.4)

**All rules in this package**: Category = Required, Security relevant = **yes**, Severity = **highest**.

| Rule ID | Description | Status | Notes |
|---|---|---|---|
| SECURITY-09 | Avoid `string::data()` | **Disabled** | C++11 provides same null-termination guarantee as `c_str()` |
| SECURITY-12 | Avoid unsafe string functions that may cause buffer overflows (`strcpy`, `sprintf`, etc.) | Active | Backup rule if AUTOSAR M18-0-5 is suppressed |
| SECURITY-17 | Avoid passing non-const parameters into `exec` calls | Active | — |
| SECURITY-18 | Avoid passing dynamically-created strings into `exec` calls | Active | — |
| SECURITY-20 | Avoid passing user input into methods as parameters without sanitization | Active | — |
| SECURITY-21 | Do not use `syslog` for logging | Active | — |
| SECURITY-26 | Do not use `setuid` | Active | — |
| SECURITY-27 | Do not use `chmod`, `chown`, or `chgrp` | Active | TOCTOU vulnerability |
| SECURITY-29 | Do not use the obsolete `ulimit()` | Active | — |
| SECURITY-31 | Do not use `cuserid` | Active | — |
| SECURITY-32 | Avoid using the obsolete `usleep` | Active | — |
| SECURITY-35 | Do not trust command-line values if an attacker can set them | **Disabled** | No way around this if command-line arguments are required |
| SECURITY-37 | Do not use weak or broken cryptographic hash functions | Active | — |
| SECURITY-39 | Use secure temporary file name functions (avoid `tmpnam`, `mktemp`) | Active | — |
| SECURITY-40 | Call `umask` before `mkstemp` | **Disabled** | Expected to never use pre-POSIX-2008 functions |
| SECURITY-41 | Call `chdir` if calling `chroot` | Active | — |
| SECURITY-48 | Do not call `system()` with a non-null argument | Active | Backup rule if AUTOSAR M18-0-3 is suppressed |

---

## 8. Package METRIC (4.5)

**All rules in this package**: Severity = low, Security relevant = no.

Metrics monitor code complexity and quality. Active metrics are enforced with thresholds.

| Rule ID | Metric | Status | Threshold | Notes |
|---|---|---|---|---|
| METRIC.CBO | Coupling Between Objects | Active | ≤ 30 | Measures class dependencies |
| METRIC.CC | McCabe Cyclomatic Complexity v(G) | Active | ≤ 30 | Per KGAS_2770 recommendation |
| METRIC.CLLOCRIF | Ratio of Comment Lines to Logical Lines of Code (files) | Active | configured | Per KGAS_3462 recommendation |
| METRIC.CLLOCRIM | Ratio in methods | **Disabled** | > 0.1 | — |
| METRIC.CLLOCRIT | Ratio in types | **Disabled** | > 0.1 | — |
| METRIC.DIF | Halstead Difficulty | **Disabled** | < 5 | — |
| METRIC.ECC | Essential Cyclomatic Complexity | **Disabled** | < 15 | — |
| METRIC.FO | Fan Out | Active | ≤ 30 | Measures calls out of a module |
| METRIC.HDIFM | Halstead Difficulty (methods) | **Disabled** | — | — |
| METRIC.HEFM | Halstead Effort (methods) | **Disabled** | — | — |
| METRIC.HICM | Halstead IC (methods) | **Disabled** | — | — |
| METRIC.HLENM | Halstead Length (methods) | **Disabled** | — | — |
| METRIC.HLEVM | Halstead Level (methods) | **Disabled** | — | — |
| METRIC.HNOBM | Halstead Number of Bugs (methods) | **Disabled** | — | — |

---

## 9. Notable Patterns

### 9.1 "Highest" Severity + Security-Relevant Rules

These rules represent the most critical safety and security requirements:

| Rule ID | Area | Issue |
|---|---|---|
| AUTOSAR A0-4-1 | Arithmetic | Floating-point division by zero |
| AUTOSAR A2-11-1 | Language | Use of `volatile` keyword |
| AUTOSAR A3-8-1 | Lifetime | Object accessed outside lifetime |
| AUTOSAR A5-1-4 | Lambda | Lambda outlives its reference-captured objects |
| AUTOSAR A5-2-5 | Bounds | Array/container access beyond range |
| AUTOSAR A5-3-2 | Pointers | Null pointer dereference |
| AUTOSAR A5-6-1 | Arithmetic | Integer division/remainder with zero RHS |
| AUTOSAR A6-2-2 | Statements | Expression statement is constructor of temp only |
| AUTOSAR A8-4-2 | Functions | Non-void function has exit path without explicit `return` |
| AUTOSAR A12-8-3 | Move semantics | Moved-from object read-accessed |
| AUTOSAR A15-1-4 | Exceptions | Resources not in valid state before `throw` |
| AUTOSAR A15-4-2 | `noexcept` | `noexcept` function exits with exception |
| AUTOSAR M3-2-2 | ODR | One Definition Rule violated |
| AUTOSAR M3-2-4 | Linkage | External linkage identifier has multiple definitions |
| AUTOSAR M7-3-3 | Namespaces | Unnamed namespace in header file |
| AUTOSAR M7-5-2 | Lifetime | Address of automatic object persists after object destroyed |
| AUTOSAR M12-1-1 | OOP | Dynamic type used in constructor/destructor body |
| SECURITY-09 to SECURITY-48 | Security | All security rules are highest severity |

### 9.2 Disabled Rules — Rationale Patterns

| Pattern | Examples | Reason |
|---|---|---|
| **Replaced by project convention** | A3-1-2, A3-1-3 | Replaced by C++ Coding Style Guide |
| **Replaced by custom E3 rule** | A15-4-5 | Replaced by E3-2 (no checked exceptions) |
| **Too many false positives** | A2-10-5, A2-7-3 | Implementation produces FP; "needs refinement" |
| **Contradicts other active rules** | A12-1-3 | Contradicts A12-1-1 and A12-1-2 |
| **Intentional project deviation** | M7-3-4 | `using`-directives allowed in source files for readability; forbidden in headers via M7-3-6 |
| **Intentional deviation — OS signals** | M18-7-1 | SIGTERM/SIGINT handlers are needed; pending further analysis |
| **Redundant — stricter rule active** | M16-0-5, M16-0-6, M16-0-7, M16-1-1, M16-1-2, M16-3-1 | All disabled because A16-0-1 already forbids all function-like macros |
| **Readability concern** | A8-5-2 | Braced-init `{}` has worse readability; same benefit from A4-7-1 + compiler warnings |
| **Design choice** | A27-0-4, A27-0-2 | C-style strings disabled; redundant given string library rules |
| **No known use case** | SECURITY-40 | Pre-POSIX-2008 functions not expected to be used |

### 9.3 Thread Safety Rules (HICPP-18_x)

All six active high-severity HICPP rules address thread safety:

```
HICPP-18_2_2 → Single lock for shared data
HICPP-18_2_4 → std::call_once (no Double-Checked Locking)
HICPP-18_3_1 → No same mutex locked twice in one scope
HICPP-18_3_2 → Lock nesting order forms DAG (no deadlock cycles)
HICPP-18_3_6 → No relaxed atomics
```

### 9.4 Taint Analysis Sub-Rules (A5-2-5-d, A27-0-1)

Several AUTOSAR rules activate Parasoft's taint analysis engine with explicit source categories:

| Taint source | Enabled for A5-2-5 | Enabled for A27-0-1 |
|---|---|---|
| Socket (`taintedDataSourceSocket`) | ✅ | ✅ |
| Files (`taintedInputFiles`) | ✅ | ✅ |
| Low-level input (`taintedInputLowLevel`) | ✅ | ✅ |
| Network (`taintedInputNetwork`) | ✅ | ✅ |
| Pipes (`taintedInputPipes`) | ✅ | ✅ |
| Streams (`taintedInputStreams`) | ❌ | ❌ |
| System calls (`taintedInputSystem`) | ✅ | ✅ |
| User input (`taintedInputUser`) | ✅ | ✅ |
| `main()` parameters | ✅ | ✅ |

---

## 10. Mapping: Rule Area → Rule IDs (Quick Reference)

| Topic | Key Rule IDs |
|---|---|
| Memory safety / lifetime | A3-8-1, A5-1-4, A5-2-5, A5-3-2, A8-5-0, A12-8-3, M7-5-2, CERT_CPP-MEM50 |
| Move semantics | A12-8-3, A12-8-4, A12-8-5, A8-4-5, A8-4-6 |
| Exception safety | A15-0-2, A15-1-4, A15-4-2, A15-5-1, M15-1-2, M15-1-3 |
| Type safety / casting | A5-2-1, A5-2-2, A5-2-3, A5-2-4, A4-7-1, A4-5-1 |
| Thread safety | HICPP-18_2_2, HICPP-18_2_4, HICPP-18_3_1, HICPP-18_3_2, HICPP-18_3_6, HICPP-18_3_3, HICPP-18_3_4 |
| ODR / linkage | M3-2-2, M3-2-4, A3-1-1 |
| Namespace / scope | M7-3-3, M7-3-4, M7-3-6, A2-10-6 |
| Resource management (RAII) | A12-0-1, A12-4-1, A8-4-11, A8-4-12, A8-4-13 |
| `noexcept` correctness | A15-4-2, A15-4-3, A15-5-1 |
| C library prohibited | M18-0-3, M18-0-4, M18-0-5, M27-0-1, A18-1-1, A18-0-1 |
| Macro / preprocessor | A16-0-1 (implied), M16-2-3, M16-3-2, A16-2-2 |
| Arithmetic safety | A0-4-1, A5-6-1, A4-7-1 |
| Security (OS calls) | SECURITY-12, SECURITY-17–SECURITY-48 |
| Complexity metrics | METRIC.CC (≤30), METRIC.CBO (≤30), METRIC.FO (≤30), METRIC.CLLOCRIF |
