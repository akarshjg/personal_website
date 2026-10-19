---
name: website-performance-audit
description: Comprehensive skill for analyzing website performance, Core Web Vitals (LCP, INP, CLS), TTFB, asset payloads, render-blocking scripts, font loading delays, and HTTP cache headers. Use whenever the user asks to analyze website performance, audit page speed, optimize load times, debug LCP, or make the website load faster.
---

# Website Performance Audit Skill

This skill provides procedures, benchmarks, and automated audit scripts to diagnose and accelerate web page load speed, improve Core Web Vitals (CWV), reduce Time to First Byte (TTFB), and eliminate render-blocking bottlenecks.

## Performance Benchmarks & Targets

| Metric | Target (Good) | Description |
| :--- | :--- | :--- |
| **LCP (Largest Contentful Paint)** | `< 2.5s` | Time for largest visual block (hero image or heading) to render |
| **INP (Interaction to Next Paint)** | `< 200ms` | Responsiveness to clicks/taps/key presses |
| **CLS (Cumulative Layout Shift)** | `< 0.1` | Visual stability of elements as assets load |
| **TTFB (Time to First Byte)** | `< 400ms` | Server latency to deliver first byte of HTML |
| **Total Page Weight** | `< 1.5MB` | Uncompressed total transferred payload |

## Audit Procedure

### 1. Run Automated Performance Audit
Run the provided audit script to inspect static assets, template configurations, resource hints, and caching rules:
```bash
python3 .agents/skills/website-performance-audit/scripts/audit_performance.py personal_website https://www.akarsh.xyz/
```

### 2. Check Key Bottlenecks

#### A. Largest Contentful Paint (LCP)
- Ensure the hero image has `fetchpriority="high"` and `loading="eager"`.
- Preload the hero image in `<head>`:
  `<link rel="preload" as="image" href="..." fetchpriority="high">`
- **Never** apply `lozad` or lazy-loading to the LCP hero image.

#### B. Eliminate Invisible Text & Font Observer Delays
- Avoid `fontfaceobserver` animations that keep elements at `opacity: 0` for seconds (e.g. `rad-fade-in-fallback`).
- Use CSS `@font-face { font-display: swap; }` to allow system fonts to render immediately while webfonts download.
- Preload primary font weights (e.g., `Inter-Medium` or `Inter.var.woff2`).

#### C. Eliminate Render-Blocking Scripts
- Place non-critical analytics (Google Tag Manager, Segment, GA4) in deferred execution (`defer`, `async`, or post-`load` event listeners).
- Avoid synchronous `<script src="...">` tags in the `<head>`.

#### D. Image Compression & Modern Formats
- Convert large PNGs (>300KB) to modern JPEG, WebP, or AVIF.
- Ensure 2x retina images are appropriately compressed with quality 80-85%.

#### E. Static Asset Caching
- Configure HTTP headers in hosting configuration (e.g. `netlify.toml`) with immutable long-term caching:
  `Cache-Control: public, max-age=31536000, immutable` for `/img/*`, `/fonts/*`, `/css/*`, `/js/*`.
