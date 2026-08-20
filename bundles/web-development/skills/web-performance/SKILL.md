---
name: web-performance
description: >-
  Core Web Vitals, Lighthouse audits, bundle optimization, and lazy loading.
  Use when improving web application speed and user experience metrics.
tags: [web-development, performance, optimization]
---

# Web Performance

## When to Use

- Page load feels slow or Lighthouse scores are below target
- Optimizing Core Web Vitals (LCP, INP, CLS) for SEO or UX
- Reducing JavaScript bundle size for mobile users
- Profiling render performance in React/Vue/Angular apps

## Procedure

### Step 1: Measure baseline

- Run Lighthouse in Chrome DevTools (Performance + Best Practices)
- Check Core Web Vitals in PageSpeed Insights: https://pagespeed.web.dev/
- Target: LCP < 2.5s, INP < 200ms, CLS < 0.1
- Record current bundle size with `@next/bundle-analyzer` or `vite-bundle-visualizer`

### Step 2: Optimize loading

- Code-split routes with dynamic imports (`React.lazy`, Vue `defineAsyncComponent`)
- Preload critical assets; defer non-critical JS
- Use `next/image` or responsive images with modern formats (WebP, AVIF)
- Self-host fonts with `font-display: swap`; subset character sets

### Step 3: Reduce JavaScript cost

- Tree-shake: import named exports, avoid barrel file re-exports
- Replace heavy libs with lighter alternatives (check **web-ecosystem-catalog**)
- Move computation to Web Workers for CPU-heavy tasks
- Server Components (Next.js) to keep non-interactive UI off the client

### Step 4: Runtime performance

- Profile with React DevTools Profiler or Vue DevTools
- Virtualize long lists; memoize expensive renders
- Debounce/throttle scroll and resize handlers
- Cache API responses with TanStack Query or HTTP cache headers

### Step 5: Monitor in production

- Real User Monitoring (Vercel Analytics, web-vitals library, Datadog RUM)
- Set performance budgets in CI (bundle size limits)
- Re-audit after major feature additions

## Output

- Before/after Lighthouse or Web Vitals metrics
- List of optimizations applied with estimated impact

## References

- web.dev performance: https://web.dev/performance/
- Core Web Vitals: https://web.dev/vitals/
- Lighthouse: https://developer.chrome.com/docs/lighthouse/
- web-vitals library: https://github.com/GoogleChrome/web-vitals
- Next.js optimizing: https://nextjs.org/docs/app/building-your-application/optimizing
