#!/usr/bin/env python3
"""
Website Performance Auditor
Analyzes web assets, font configurations, render-blocking scripts, caching headers,
and Core Web Vitals best practices for static websites.
"""

import os
import re
import sys
import glob
import urllib.request
import time

def audit_asset_sizes(root_dir):
    findings = []
    large_assets = []
    
    # Common asset patterns
    exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js', '.woff', '.woff2', '.ttf')
    
    for base_dir in [os.path.join(root_dir, 'static'), os.path.join(root_dir, 'public'), os.path.join(root_dir, 'themes')]:
        if not os.path.exists(base_dir):
            continue
        for root, _, files in os.walk(base_dir):
            for f in files:
                if f.lower().endswith(exts):
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp)
                        rel_path = os.path.relpath(fp, root_dir)
                        if sz > 100 * 1024:  # > 100 KB
                            large_assets.append((rel_path, sz, f.split('.')[-1].lower()))
                    except OSError:
                        pass

    # Sort largest first
    large_assets.sort(key=lambda x: x[1], reverse=True)
    
    # Check for images > 300KB
    for path, sz, ext in large_assets:
        sz_kb = sz / 1024
        if ext in ['png', 'jpg', 'jpeg'] and sz > 300 * 1024:
            findings.append({
                'category': 'Oversized Image',
                'severity': 'HIGH',
                'message': f"Image `{path}` is {sz_kb:.1f} KB. Recommend converting to WebP/optimized JPEG or resizing."
            })
        elif ext in ['ttf', 'otf', 'woff'] and sz > 150 * 1024:
            findings.append({
                'category': 'Heavy Font',
                'severity': 'MEDIUM',
                'message': f"Font file `{path}` is {sz_kb:.1f} KB. Prefer WOFF2 variable fonts."
            })
            
    return findings, large_assets

def audit_templates_and_scripts(root_dir):
    findings = []
    layouts_dir = os.path.join(root_dir, 'layouts')
    themes_dir = os.path.join(root_dir, 'themes')
    
    html_files = []
    for d in [layouts_dir, themes_dir]:
        if os.path.exists(d):
            html_files.extend(glob.glob(os.path.join(d, '**', '*.html'), recursive=True))

    has_preconnect = False
    has_lcp_preload = False
    blocking_scripts = []
    font_observer_delays = []

    for hf in html_files:
        try:
            with open(hf, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        rel_path = os.path.relpath(hf, root_dir)

        # Check for preconnect
        if 'rel="preconnect"' in content:
            has_preconnect = True

        # Check for hero / LCP preload
        if 'rel="preload"' in content and 'as="image"' in content:
            has_lcp_preload = True

        # Check for blocking script tags in head
        if 'head.html' in hf or '<head>' in content:
            scripts = re.findall(r'<script\b([^>]*)>', content, re.IGNORECASE)
            for s in scripts:
                if 'src=' in s and 'defer' not in s and 'async' not in s and 'type="application/ld+json"' not in s:
                    blocking_scripts.append((rel_path, s.strip()))

        # Check for fontfaceobserver or fallback delay animations
        if 'rad-fade-in-fallback' in content:
            duration_match = re.search(r'animation-duration:\s*([0-9]+s)', content)
            if duration_match:
                font_observer_delays.append((rel_path, duration_match.group(1)))

    if not has_preconnect:
        findings.append({
            'category': 'Resource Hints',
            'severity': 'MEDIUM',
            'message': "Missing `<link rel=\"preconnect\">` hints for third-party origins (Google Fonts, CDNs)."
        })

    if not has_lcp_preload:
        findings.append({
            'category': 'LCP Optimization',
            'severity': 'HIGH',
            'message': "Hero / LCP image does not have `<link rel=\"preload\" as=\"image\" fetchpriority=\"high\">` in `<head>`."
        })

    for path, script in blocking_scripts:
        findings.append({
            'category': 'Render Blocking JS',
            'severity': 'HIGH',
            'message': f"Synchronous script without `defer` or `async` found in `{path}`: `<script {script}>`"
        })

    for path, dur in font_observer_delays:
        findings.append({
            'category': 'Font Delay / Invisible Text',
            'severity': 'CRITICAL',
            'message': f"CSS animation fallback `{path}` delays content visibility by {dur} waiting for font observer. Content appears blank to users on slow connections!"
        })

    return findings

def audit_netlify_caching(root_dir):
    findings = []
    netlify_path = os.path.join(root_dir, 'netlify.toml')
    if not os.path.exists(netlify_path):
        findings.append({
            'category': 'Cache Headers',
            'severity': 'MEDIUM',
            'message': "No `netlify.toml` found to configure HTTP cache-control headers."
        })
        return findings

    try:
        with open(netlify_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return findings

    if '[[headers]]' not in content or 'Cache-Control' not in content:
        findings.append({
            'category': 'Cache Headers',
            'severity': 'HIGH',
            'message': "Missing `[[headers]]` in `netlify.toml`. Static assets (images, fonts, css, js) should have `Cache-Control: public, max-age=31536000, immutable`."
        })

    return findings

def audit_live_site(url):
    findings = []
    print(f"Testing live site response: {url}...")
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 WebsiteSpeedAudit/1.0'}
        )
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read()
            ttfb = (time.time() - start) * 1000
            headers = dict(response.info())

        findings.append({
            'category': 'Live TTFB',
            'severity': 'PASS' if ttfb < 400 else ('MEDIUM' if ttfb < 800 else 'HIGH'),
            'message': f"Initial HTML response time (TTFB): {ttfb:.0f} ms ({len(html)} bytes HTML transferred)"
        })

        content_encoding = headers.get('Content-Encoding', 'none')
        if content_encoding in ['gzip', 'br']:
            findings.append({
                'category': 'Live Compression',
                'severity': 'PASS',
                'message': f"HTML is compressed using `{content_encoding}`"
            })
        else:
            findings.append({
                'category': 'Live Compression',
                'severity': 'HIGH',
                'message': "HTML response is uncompressed (no gzip or brotli)"
            })

    except Exception as e:
        findings.append({
            'category': 'Live Connection',
            'severity': 'WARN',
            'message': f"Could not test live site {url}: {e}"
        })

    return findings

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    url = sys.argv[2] if len(sys.argv) > 2 else "https://www.akarsh.xyz/"

    print(f"# Website Performance Audit Report: {os.path.abspath(root)}\n")

    asset_findings, large_assets = audit_asset_sizes(root)
    template_findings = audit_templates_and_scripts(root)
    caching_findings = audit_netlify_caching(root)
    live_findings = audit_live_site(url)

    all_findings = asset_findings + template_findings + caching_findings + live_findings

    critical = [f for f in all_findings if f['severity'] == 'CRITICAL']
    high = [f for f in all_findings if f['severity'] == 'HIGH']
    medium = [f for f in all_findings if f['severity'] == 'MEDIUM']
    passes = [f for f in all_findings if f['severity'] == 'PASS']

    print("## Executive Summary")
    print(f"- 🚨 **Critical**: {len(critical)}")
    print(f"- ⚠️ **High Priority**: {len(high)}")
    print(f"- ℹ️ **Medium Priority**: {len(medium)}")
    print(f"- ✅ **Passing**: {len(passes)}\n")

    print("## Detailed Audit Findings")
    print("| Severity | Category | Issue & Recommendation |")
    print("| :--- | :--- | :--- |")
    for f in all_findings:
        sev_icon = "🚨 CRITICAL" if f['severity'] == 'CRITICAL' else (
            "⚠️ HIGH" if f['severity'] == 'HIGH' else (
                "ℹ️ MEDIUM" if f['severity'] == 'MEDIUM' else (
                    "✅ PASS" if f['severity'] == 'PASS' else "⚠️ WARN"
                )
            )
        )
        print(f"| {sev_icon} | {f['category']} | {f['message']} |")
    print()

    if large_assets:
        print("## Largest Static Assets Inventory")
        print("| Size | File |")
        print("| :--- | :--- |")
        for path, sz, ext in large_assets[:15]:
            print(f"| {sz / 1024:.1f} KB | `{path}` |")
        print()

if __name__ == "__main__":
    main()
