#!/usr/bin/env python3
"""
Website Content & SEO Auditor
Scans markdown content, frontmatter, image alt texts, heading hierarchies,
placeholder words, and HTML metadata for a Hugo or static website.
"""

import os
import re
import sys
import glob
from pathlib import Path

def audit_markdown_files(content_dir):
    results = []
    placeholder_patterns = [
        re.compile(r'\b(lorem ipsum|placeholder|todo|fixme|xxx)\b', re.IGNORECASE),
        re.compile(r'\b(company [a-z]|podcast [a-z]|specific year|major city)\b', re.IGNORECASE)
    ]
    
    for md_path in glob.glob(os.path.join(content_dir, '**', '*.md'), recursive=True):
        rel_path = os.path.relpath(md_path, content_dir)
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            results.append({'file': rel_path, 'status': 'ERROR', 'issues': [f"Could not read file: {e}"]})
            continue

        issues = []
        warnings = []
        
        # Check Frontmatter
        frontmatter = {}
        body = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm_raw = parts[1]
                body = parts[2]
                for line in fm_raw.splitlines():
                    if ':' in line:
                        k, v = line.split(':', 1)
                        frontmatter[k.strip()] = v.strip().strip('"\'')
        elif content.startswith('+++'):
            parts = content.split('+++', 2)
            if len(parts) >= 3:
                fm_raw = parts[1]
                body = parts[2]
                for line in fm_raw.splitlines():
                    if '=' in line:
                        k, v = line.split('=', 1)
                        frontmatter[k.strip()] = v.strip().strip('"\'')

        if not frontmatter.get('title'):
            issues.append("Missing frontmatter 'title'")
        if not frontmatter.get('description'):
            warnings.append("Missing frontmatter 'description' (recommended for SEO)")
        if frontmatter.get('draft') in ['true', True]:
            warnings.append("Marked as 'draft: true' (won't render in production)")

        # Check Headings Hierarchy
        headings = re.findall(r'^(#{1,6})\s+(.+)$', body, re.MULTILINE)
        levels = [len(h[0]) for h in headings]
        for i in range(len(levels) - 1):
            if levels[i+1] > levels[i] + 1:
                warnings.append(f"Skipped heading level: h{levels[i]} jumped to h{levels[i+1]} at '{headings[i+1][1][:30]}...'")

        # Check Image Alt Texts
        images = re.findall(r'!\[(.*?)\]\((.*?)\)', body)
        for alt, src in images:
            if not alt.strip():
                issues.append(f"Image without alt text: {src}")

        # Check Placeholders
        for pat in placeholder_patterns:
            matches = pat.findall(body)
            if matches:
                warnings.append(f"Possible placeholder text detected: {', '.join(set(matches))}")

        # Word count
        words = len(re.findall(r'\b\w+\b', body))

        results.append({
            'file': rel_path,
            'title': frontmatter.get('title', '(No Title)'),
            'words': words,
            'headings_count': len(headings),
            'issues': issues,
            'warnings': warnings,
            'status': 'FAIL' if issues else ('WARN' if warnings else 'PASS')
        })

    return results

def audit_html_metadata(public_dir):
    results = []
    if not os.path.exists(public_dir):
        return results

    for html_path in glob.glob(os.path.join(public_dir, '**', '*.html'), recursive=True):
        rel_path = os.path.relpath(html_path, public_dir)
        # Check only top-level index or key landing pages
        if not (rel_path == 'index.html' or rel_path.endswith('/index.html')):
            continue

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
        except Exception:
            continue

        issues = []
        warnings = []

        if '<title>' not in html or '</title>' not in html:
            issues.append("Missing <title> tag")
        elif re.search(r'<title>\s*</title>', html):
            issues.append("Empty <title> tag")

        if not re.search(r'<meta[^>]*name=["\']description["\']', html, re.IGNORECASE):
            warnings.append("Missing meta description")

        if not re.search(r'<meta[^>]*name=["\']viewport["\']', html, re.IGNORECASE):
            issues.append("Missing viewport meta tag")

        # Check for multiple H1 tags
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
        if len(h1s) > 1:
            warnings.append(f"Multiple <h1> tags found ({len(h1s)} tags)")
        elif len(h1s) == 0:
            warnings.append("No <h1> tag found on page")

        # Check images missing alt attribute
        imgs = re.findall(r'<img\b([^>]*)>', html, re.IGNORECASE)
        missing_alt = 0
        for img_attrs in imgs:
            if 'alt=' not in img_attrs:
                missing_alt += 1
        if missing_alt > 0:
            warnings.append(f"{missing_alt} <img> tags missing 'alt' attribute")

        results.append({
            'page': rel_path,
            'issues': issues,
            'warnings': warnings,
            'status': 'FAIL' if issues else ('WARN' if warnings else 'PASS')
        })

    return results

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    content_dir = os.path.join(root, "content")
    public_dir = os.path.join(root, "public")

    print(f"# Content & SEO Audit Report: {os.path.abspath(root)}\n")

    if os.path.exists(content_dir):
        md_results = audit_markdown_files(content_dir)
        total_md = len(md_results)
        passed_md = sum(1 for r in md_results if r['status'] == 'PASS')
        warned_md = sum(1 for r in md_results if r['status'] == 'WARN')
        failed_md = sum(1 for r in md_results if r['status'] == 'FAIL')

        print(f"## Markdown Content Audit ({total_md} files)")
        print(f"- **Passed**: {passed_md} | **Warnings**: {warned_md} | **Errors**: {failed_md}\n")

        print("| Status | File | Title | Words | Issues / Warnings |")
        print("| :--- | :--- | :--- | :--- | :--- |")
        for r in md_results:
            status_icon = "✅ PASS" if r['status'] == 'PASS' else ("⚠️ WARN" if r['status'] == 'WARN' else "❌ FAIL")
            msgs = r['issues'] + r['warnings']
            msg_str = "; ".join(msgs) if msgs else "None"
            print(f"| {status_icon} | `{r['file']}` | {r['title']} | {r['words']} | {msg_str} |")
        print()

    if os.path.exists(public_dir):
        html_results = audit_html_metadata(public_dir)
        print(f"## HTML Metadata & Semantic SEO Audit ({len(html_results)} pages)")
        print("| Status | Page | Issues / Warnings |")
        print("| :--- | :--- | :--- |")
        for r in html_results:
            status_icon = "✅ PASS" if r['status'] == 'PASS' else ("⚠️ WARN" if r['status'] == 'WARN' else "❌ FAIL")
            msgs = r['issues'] + r['warnings']
            msg_str = "; ".join(msgs) if msgs else "None"
            print(f"| {status_icon} | `{r['page']}` | {msg_str} |")
        print()

if __name__ == "__main__":
    main()
