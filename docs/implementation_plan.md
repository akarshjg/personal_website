# Implementation Plan - Goodreads Pipeline Automation & Script Integration

This plan outlines the steps to integrate the Goodreads CSV import script directly into a Netlify build pipeline, organize all Python helper scripts into the repository, and sync the project documentation (`walkthrough.md` and `implementation_plan.md`) into Git.

## Proposed Changes

### 1. Build Pipeline Automation
We will update `netlify.toml` to run the Goodreads CSV import script automatically before the Hugo build on Netlify's servers. This means when you download a new Goodreads export, you only need to replace the CSV file and push it; Netlify will handle the re-classification and rendering on the fly.

#### [MODIFY] [netlify.toml](file:///Users/akarsh/Documents/Personal%20Website/personal_website/netlify.toml)
- Update the build command from:
  ```toml
  command = "hugo"
  ```
  to:
  ```toml
  command = "python3 scripts/import_goodreads_csv.py goodreads_library_export.csv && hugo"
  ```

### 2. Organize and Integrate Python Scripts
We will move the verification/sorting script from the temporary scratch area into the repository's `scripts/` folder so it is tracked and available for you to run locally.

#### [NEW] [verify_sorting.py](file:///Users/akarsh/Documents/Personal%20Website/personal_website/scripts/verify_sorting.py)
- Move and save the sorting checker utility to `scripts/verify_sorting.py`.

### 3. Sync Documentation to Git
We will create a `docs/` folder in the repository and copy the implementation plan and walkthrough markdown files so they are tracked in Git.

#### [NEW] [docs/implementation_plan.md](file:///Users/akarsh/Documents/Personal%20Website/personal_website/docs/implementation_plan.md)
#### [NEW] [docs/walkthrough.md](file:///Users/akarsh/Documents/Personal%20Website/personal_website/docs/walkthrough.md)

---

## Verification Plan

### Automated Tests
- Run `netlify build --dry` (if Netlify CLI is available) or run the command locally:
  `python3 scripts/import_goodreads_csv.py goodreads_library_export.csv && hugo`
  to verify that it executes without errors.

### Manual Verification
- Commit the changes and push to GitHub, then monitor the Netlify build log to ensure the pipeline builds and deploys successfully.
