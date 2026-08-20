---
name: react-development
description: >-
  React components, hooks, state management, performance, and accessibility basics.
  Use when building or reviewing React UI.
tags: [web-development, react, frontend]
---

# React Development

## When to Use

- Building reusable UI components and page layouts in React
- Managing state with hooks or external libraries (Zustand, Redux, Jotai)
- Optimizing render performance or fixing hook dependency bugs
- Adding accessibility to interactive React components

## Procedure

### Step 1: Confirm React version and patterns

- Check `react` and `react-dom` versions via **npm-package-research**
- React 19+: use current docs for Actions, `use()`, and ref-as-prop patterns
- Prefer function components and hooks; avoid class components in new code

### Step 2: Component design

- Single responsibility per component; compose smaller pieces
- Colocate styles, tests, and types with components when project convention allows
- Lift state only as high as needed; avoid prop drilling with context or state libs
- Use **web-ecosystem-catalog** to pick state and UI libraries consistently

### Step 3: Hooks and side effects

- `useState` for local UI state; `useReducer` for complex transitions
- `useEffect` only for synchronizing with external systems (not derived state)
- Memoize expensive computations with `useMemo`; stable callbacks with `useCallback`
- Custom hooks for reusable logic (`useFetch`, `useForm`, etc.)

### Step 4: Performance

- Profile before optimizing; use React DevTools Profiler
- `React.memo` for expensive pure components receiving stable props
- Virtualize long lists (`@tanstack/react-virtual`, `react-window`)
- Code-split routes with `React.lazy` and `Suspense`

### Step 5: Accessibility

- Semantic HTML first; ARIA only when native elements insufficient
- Keyboard navigation and focus management for modals and menus
- Associate labels with inputs; provide alt text and live regions where needed
- Follow **web-ux-workflow** WCAG baseline

## Output

- React component(s) with clear props interface and documented state flow
- Accessibility notes for interactive elements

## References

- React docs: https://react.dev/
- Hooks: https://react.dev/reference/react
- Accessibility: https://react.dev/learn/accessibility
- Performance: https://react.dev/learn/render-and-commit
