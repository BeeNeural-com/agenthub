---
description: Parasoft static code analysis zero-findings mandate and VWOS ruleset compliance rules for production and test source files
applyTo: "**/src/**/*.{h,hpp,cpp},**/tests/**/*.cpp"
---

# Static Analysis (SCA) Compliance

All production source files and test files must achieve zero Parasoft findings at any severity level. Treat every rule as a hard constraint — a finding at any severity makes the code unacceptable regardless of other design considerations.

## Reference

Read `.github/skills/parasoft-vwos-ruleset/SKILL.md` in full before reviewing or writing any source file. The skill contains:
- The **Best Practices checklist** — apply all items
- The **Prohibited Language Features table** — none of these features may appear in any submitted code

## Prohibited patterns (most common violations)

**C-style casts** (A5-2-2): use `static_cast`, `dynamic_cast`, or `reinterpret_cast` with justification; never `(Type)expr`

**`reinterpret_cast`** (A5-2-4): permitted only where unavoidable at OS API boundaries; must be accompanied by a comment explaining why no alternative exists

**`volatile`** (A2-11-1): not permitted; use `std::atomic` for shared state

**Null pointer dereference** (A5-3-2): all pointer results from OS/POSIX calls must be checked before use

**Out-of-lifetime access** (A3-8-1): no references or pointers to destroyed objects

**Integer division by zero** (A5-6-1): guard divisors before division

**`noexcept` violation** (A15-4-2): functions declared `noexcept` must not propagate exceptions

**ODR violation** (M3-2-2): each class/function defined in exactly one translation unit

**C library functions** (Prohibited Language Features table): no `printf`, `malloc`, `free`, `memcpy` without explicit justification

## Enforcement

- **Before submitting any source file**: mentally apply the Best Practices checklist
- **During SWE.3 review**: run DR08 against every `.h` and `.cpp` under review
- **During SWE.4 review**: apply to test files as well — test code is production-quality code
- **Target**: zero findings at any severity level; no waivers without explicit user confirmation and a recorded justification comment in the source
