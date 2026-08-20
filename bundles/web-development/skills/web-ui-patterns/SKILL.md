---
name: web-ui-patterns
description: >-
  Layout, responsive design, component libraries (shadcn, MUI, Tailwind), and design tokens.
  Use when implementing web interfaces and design systems.
tags: [web-development, ui, design]
---

# Web UI Patterns

## When to Use

- Building responsive layouts and page structures
- Integrating a component library (shadcn/ui, MUI, Radix, Headless UI)
- Setting up design tokens, theming, and dark mode
- Standardizing buttons, forms, modals, and navigation patterns

## Procedure

### Step 1: Establish design foundation

- Define breakpoints (mobile-first): sm 640px, md 768px, lg 1024px, xl 1280px
- Set design tokens: colors, spacing scale, typography, border-radius, shadows
- Use CSS variables or Tailwind `@theme` for token-driven theming
- Consult **web-ecosystem-catalog** CSS section for library selection

### Step 2: Choose component strategy

- **shadcn/ui**: copy-paste Radix + Tailwind components; full ownership
- **MUI / Chakra**: batteries-included with theming API
- **Headless UI + Tailwind**: unstyled primitives, custom design
- Match library to framework (React/Vue/Angular) and existing project stack

### Step 3: Layout patterns

- App shell: header + sidebar + main content area
- Grid: CSS Grid for page layout; Flexbox for component internals
- Container max-width and consistent horizontal padding
- Sticky headers, scrollable content regions, and safe-area insets for mobile

### Step 4: Component conventions

- Buttons: primary / secondary / ghost / destructive variants with consistent sizing
- Forms: label above input, inline validation, disabled and loading states
- Modals: focus trap, ESC to close, aria-modal and role="dialog"
- Tables: responsive overflow, sortable headers, empty states
- Toasts/notifications: non-blocking, auto-dismiss, accessible live regions

### Step 5: Responsive and performance

- Mobile-first CSS; test at 320px, 768px, and 1440px widths
- Optimize images (`next/image`, responsive srcset, WebP/AVIF)
- Avoid layout shift (CLS): reserve space for async content
- Use **web-docs-research** for CSS features and browser support

## Output

- UI component implementation with responsive behavior documented
- Token/theming configuration if new design primitives added

## References

- Tailwind CSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com
- MUI: https://mui.com/material-ui/getting-started/
- Radix UI: https://www.radix-ui.com/primitives
- MDN CSS Grid: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
