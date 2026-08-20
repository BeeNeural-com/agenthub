---
description: Rules for generating blast-radius change impact reports when requirement, architecture, or design IDs are renamed, deleted, or split
applyTo: "**/agents/**/*change-impact*"
---

# Change Impact Agent Rules

## Read-only declaration

Change impact agents **never modify any files**. They produce impact reports only. After delivering the report, they recommend which writer agent to invoke for each required update. The user decides whether and when to proceed.

## Risk classification symbols

Use these symbols consistently in all impact tables and TODO lists:

**🔴 CRITICAL** — The change will cause a compile error or a broken traceability chain if applied without updating this artifact. Must be fixed before the change is committed.

**🟡 WARNING** — The artifact will still compile and run but will produce a wrong result, stale test coverage, or an ASPICE audit finding. Must be fixed before the next test run.

**🟢 LOW** — Annotation-only update required (e.g., `@covers`, `@req`, `:covers:` ID rename). The code is correct but the ASPICE audit will flag a stale ID.

## Impact report format

```
## <SWE.X> Change Impact Report — <Component> — <date>

**Changed items**: <N>

### Impact table

For each changed item, list: changed item | change type | affected file | lines | required update | risk symbol

### TODO(<SWE.X>) — Change Impact

- [ ] 🔴 <file> — <description of required update>
- [ ] 🟡 <file> — <description>
- [ ] 🟢 <file> — <annotation update>
```

## Post-report recommendation

After delivering the report, always recommend running the corresponding traceability checker to verify all remaining links are consistent once the updates are applied.

## Downstream Artifact Registry

When an ID in a given namespace changes (rename, delete, split), the change impact agent must check **all** downstream paths listed for that namespace. This is the single source of truth for downstream artifact locations — agents must not hardcode their own scope lists.

| ID namespace | Upstream location | Downstream artifact paths |
|---|---|---|
| `req:` | `doc/component_requirements/<component>/` | `doc/component_architecture/<component>/*.md` (`covers:`), `src/**/*.{h,hpp}` (`@req`), `tests/unit/**/*.cpp` (`@req`), `tests/qualification/**/*.cpp` (`@req`), `doc/component_qualification_tests/<component>/*.md` (`verifies:`), `doc/component_qualification_tests/<component>/_briefing.md` (briefing items) |
| `arch:` (elements) | `doc/component_architecture/<component>/` | `src/**/*.{h,hpp}` (`@elaborates`), `tests/unit/**/*.cpp` (`@covers`) |
| `arch:` (sequences, interfaces) | `doc/component_architecture/<component>/` | `tests/integration/**/*.cpp` (`@arch`), `doc/component_integration_tests/<component>/*.md` (`verifies:`), `doc/component_integration_tests/<component>/_briefing.md` (briefing items) |

**Usage:** When a change impact agent runs T6/T8 (or equivalent), it looks up the changed ID's namespace in this table and scans every listed downstream path for references. The impact table and TODO list must include findings from all paths — not just the ones the calling agent "owns".

**Briefing files:** `_briefing.md` files are downstream artifacts. When upstream IDs change, the briefing becomes stale. Include `_briefing.md` in the blast-radius report with 🟡 WARNING severity (the briefing is still usable but will produce false coverage gaps at tester Triage).

## Self-improvement protocol

1. Complete the impact report first.
2. Propose improvements explicitly before modifying any agent file.
3. Never delete existing rules — only extend or correct.
