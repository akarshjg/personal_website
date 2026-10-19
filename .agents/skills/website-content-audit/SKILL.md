---
name: website-content-audit
description: Comprehensive skill for analyzing website content, SEO metadata, reading level, heading hierarchy, image alt text, broken links, placeholder text, and Open Graph tags. Use whenever the user asks to analyze website content, audit pages for SEO/readability, check for broken links, or review copywriting and completeness.
---

# Website Content & SEO Audit Skill

This skill provides a structured workflow and automated tools to audit static websites (Hugo, Jekyll, Astro, Next.js, or raw HTML) for content quality, copywriting, SEO hygiene, accessibility, and metadata integrity.

## Audit Workflow

### 1. Run Automated Content & SEO Audit
Execute the included helper script:
```bash
python3 .agents/skills/website-content-audit/scripts/audit_content.py personal_website
```

The script audits:
- **Frontmatter Hygiene**: Checks for missing `title`, missing `description`, and unexpected `draft` flags.
- **Headings Structure**: Ensures a single `<h1>` per page and valid sequential heading progression (`<h2>` -> `<h3>`, no skipping levels).
- **Image Accessibility**: Flags missing or empty `alt` attributes.
- **Placeholder Detection**: Flags unintentional placeholder text (e.g., "Lorem Ipsum", "TODO", "Company X", "specific year").
- **HTML Metadata**: Verifies `<title>`, `<meta name="viewport">`, meta descriptions, and Open Graph tags on generated HTML pages.

### 2. Copywriting & Tone Review
When reviewing text content on personal or portfolio websites:
- **Authenticity**: Avoid generic tropes ("dynamic results-driven professional"). Use concrete projects, tools (e.g. Tableau, Python, PySpark), metrics, and personal narratives.
- **Scannability**: Break long walls of text into short, 2–3 sentence paragraphs with bold lead-ins or bullet points.
- **Grammar & Voice**: Ensure active voice and first-person consistency ("I led", "I built").

### 3. Link & Asset Verification
- Verify that internal markdown links resolve to valid published routes.
- Check that all images referenced in markdown exist in the `static/` or asset directory.
