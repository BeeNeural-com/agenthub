# General Engineering Standards

Language-agnostic software engineering practices.

## Code review

- Reviews are blocking for correctness, security, and maintainability
- Author provides context: intent, test plan, rollout notes
- Prefer small PRs (<400 lines changed) for effective review

## Design before build

- Use **system-design** or **technical-rfc** for cross-team or irreversible decisions
- Document trade-offs and rejected alternatives
- Link ADRs/RFCs from code comments where relevant

## Testing

- Tests prove behavior, not implementation details
- Follow test pyramid: many unit, fewer integration, minimal E2E
- No merge without CI green and reviewer approval

## Documentation

- Update changelogs and README for user-visible changes
- Deprecate with migration path, not silent removal