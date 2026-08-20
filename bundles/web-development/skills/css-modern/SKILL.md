---
name: css-modern
description: >-
  Tailwind CSS, CSS Modules, styled-components, and modern layout techniques.
  Use when styling web applications.
tags: [web-development, css, styling]
---

# Modern CSS

## When to Use

- Setting up or extending styling approach in a web project
- Implementing responsive layouts with Flexbox or Grid
- Choosing between Tailwind, CSS Modules, or CSS-in-JS
- Applying modern CSS features (container queries, `:has()`, layers)

## Procedure

### Step 1: Choose styling strategy

| Approach | Best for |
|----------|----------|
| Tailwind CSS | Utility-first, rapid prototyping, design tokens via config |
| CSS Modules | Scoped class names, minimal runtime, any framework |
| styled-components / Emotion | Dynamic theming, co-located styles in React |
| Vanilla CSS + layers | Maximum control, `@layer` for cascade management |

Align with existing project conventions; consult **web-ecosystem-catalog**.

### Step 2: Layout fundamentals

- Flexbox: one-dimensional alignment (nav bars, card rows)
- CSS Grid: two-dimensional layouts (dashboards, page shells)
- Container queries (`@container`) for component-responsive design
- Logical properties (`margin-inline`, `padding-block`) for i18n

### Step 3: Tailwind workflow (if selected)

- Configure `tailwind.config.js` with design tokens and content paths
- Use `@apply` sparingly; prefer utilities in markup
- `dark:` variant for dark mode; `group-*` and `peer-*` for state styling
- Install official plugins: `@tailwindcss/forms`, `@tailwindcss/typography`

### Step 4: Maintainability

- Avoid deep selector nesting and `!important` overrides
- Extract repeated patterns into components, not duplicated utility strings
- Use CSS variables for theme values shared across approaches
- Verify browser support via **web-docs-research** / caniuse.com

## Output

- Styled components/pages with consistent token usage
- Styling approach documented if new pattern introduced

## References

- MDN CSS: https://developer.mozilla.org/en-US/docs/Web/CSS
- Tailwind CSS: https://tailwindcss.com/docs
- CSS Modules: https://github.com/css-modules/css-modules
- styled-components: https://styled-components.com/docs
- Container queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
