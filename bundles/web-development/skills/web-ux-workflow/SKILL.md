---
name: web-ux-workflow
description: >-
  User flows, wireframes, usability heuristics, accessibility (WCAG), and developer handoff.
  Use when planning or reviewing user experience for web features.
tags: [web-development, ux, accessibility]
---

# Web UX Workflow

## When to Use

- Planning a new web feature from user need to implementation
- Creating user flows and low-fidelity wireframes before coding
- Reviewing usability and accessibility of an existing interface
- Preparing design handoff specifications for developers

## Procedure

### Step 1: Define user goals and flows

- Identify primary persona and job-to-be-done
- Map happy path and error/recovery paths as a flow diagram
- List entry points (navigation, deep link, notification)
- Define success metric (task completion rate, time-on-task)

### Step 2: Wireframe and information architecture

- Low-fidelity wireframes: layout blocks, hierarchy, CTA placement
- Group related actions; minimize cognitive load (7 +/- 2 rule as guide)
- Consistent navigation patterns across sections
- Empty states, loading states, and error states designed upfront

### Step 3: Usability heuristics (Nielsen)

- Visibility of system status (loading indicators, progress)
- Match between system and real world (familiar labels)
- User control and freedom (undo, cancel, back navigation)
- Consistency and standards across the application
- Error prevention and clear recovery messages
- Recognition over recall (visible options vs memorized commands)

### Step 4: Accessibility (WCAG 2.2 baseline)

- Target **Level AA** compliance for public-facing web apps
- Perceivable: text alternatives, color contrast >= 4.5:1, resizable text
- Operable: keyboard accessible, no seizure triggers, sufficient time limits
- Understandable: predictable navigation, input assistance, readable content
- Robust: valid semantic HTML, ARIA only when necessary
- Test with screen reader (NVDA/VoiceOver) and keyboard-only navigation

### Step 5: Developer handoff

- Annotate spacing, breakpoints, and interaction states
- Specify focus order and ARIA attributes for custom widgets
- Link to design tokens from **web-ui-patterns**
- Acceptance criteria: user stories + accessibility checklist

## Output

- User flow diagram and wireframe description (or linked design file)
- Accessibility checklist with WCAG criteria addressed
- Handoff notes for implementation team

## References

- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- WAI-ARIA practices: https://www.w3.org/WAI/ARIA/apg/
- Nielsen heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- web.dev accessibility: https://web.dev/accessibility/
- Axe DevTools: https://www.deque.com/axe/
