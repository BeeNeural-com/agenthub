# Web Development Standards

Conventions for consistent, maintainable, and accessible web applications.

## Language and typing

- Prefer **TypeScript** for new frontend and Node.js code
- Enable `strict` mode in tsconfig; avoid `any` without documented justification
- Share types between client and server when in a monorepo

## Documentation and research

- **Official docs first**: MDN for web platform, framework docs for React/Vue/Angular/Next/Node
- Use **web-docs-research** and **npm-package-research** skills before implementing APIs or adding packages
- Do not rely on training data for version-specific behavior; verify against live docs
- Cite official doc URLs in PRs and implementation notes

## Dependencies

- Pin semver ranges intentionally: `^` for libraries, exact for tooling when reproducibility matters
- Run `npm audit` after adding dependencies; address high/critical advisories
- Check bundle size for client-side imports via Bundlephobia before adopting heavy packages
- Prefer established libraries from **web-ecosystem-catalog** over unmaintained alternatives

## Accessibility

- Target **WCAG 2.2 Level AA** for user-facing interfaces
- Semantic HTML before ARIA; keyboard navigation for all interactive elements
- Color contrast >= 4.5:1 for normal text; test with axe or Lighthouse accessibility audit

## Code quality

- Match existing project conventions for file structure, naming, and import style
- Components: single responsibility; colocate tests with source files
- API routes: validate input, return consistent error envelopes, use parameterized queries
- No secrets in client bundles, logs, or committed `.env` files

## Performance

- Code-split routes; lazy-load below-the-fold content
- Optimize images and fonts; monitor Core Web Vitals in production
- Profile before micro-optimizing; measure bundle size on PRs for significant changes
