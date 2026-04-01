#!/usr/bin/env python3
"""Generate sitemap.xml for Nashville Dog Training site on GitHub Pages."""

import os
from datetime import date
from pathlib import Path

BASE_URL = "https://magsbrother.github.io/nashvilledogtraining"
SITE_ROOT = Path("/home/justin-malinow/nashvilledogtraining")
BLOG_DIR = SITE_ROOT / "blog"
OUTPUT = SITE_ROOT / "sitemap.xml"
TODAY = date.today().isoformat()


def collect_urls():
    urls = []

    # Main index page
    urls.append((f"{BASE_URL}/", "1.0"))

    # Blog index page
    urls.append((f"{BASE_URL}/blog/", "0.7"))

    # Directory-based blog posts: blog/<slug>/index.html
    for entry in sorted(BLOG_DIR.iterdir()):
        if entry.is_dir() and (entry / "index.html").exists():
            slug = entry.name
            urls.append((f"{BASE_URL}/blog/{slug}/", "0.7"))

    # Flat-file blog posts: blog/<slug>.html
    for entry in sorted(BLOG_DIR.iterdir()):
        if entry.is_file() and entry.suffix == ".html" and entry.name != "index.html":
            urls.append((f"{BASE_URL}/blog/{entry.name}", "0.7"))

    return urls


def generate_sitemap(urls):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    urls = collect_urls()
    sitemap_xml = generate_sitemap(urls)
    OUTPUT.write_text(sitemap_xml)
    print(f"Sitemap written to {OUTPUT}")
    print(f"Total URLs: {len(urls)}")
    # Breakdown
    dir_posts = sum(1 for u, _ in urls if u.endswith("/") and "/blog/" in u and u != f"{BASE_URL}/blog/")
    flat_posts = sum(1 for u, _ in urls if u.endswith(".html"))
    print(f"  Main index: 1")
    print(f"  Blog index: 1")
    print(f"  Directory-based posts: {dir_posts}")
    print(f"  Flat-file posts: {flat_posts}")
