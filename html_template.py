"""
Vivameda Blog Agent — HTML Template

Generates clean, responsive HTML blog posts styled for Vivameda's brand.
"""
import re
from datetime import datetime

import markdown

from config import SITE_NAME, SITE_URL, AUTHOR_NAME


def render_html(
    title: str,
    meta_description: str,
    body_markdown: str,
    date: str | None = None,
    slug: str | None = None,
) -> str:
    """
    Convert a Markdown blog post into a complete, styled HTML page.
    """
    if date is None:
        date = datetime.utcnow().strftime("%B %d, %Y")

    # Convert markdown body to HTML
    body_html = markdown.markdown(
        body_markdown,
        extensions=["fenced_code", "tables", "toc", "smarty"],
    )

    # Generate slug from title if not provided
    if slug is None:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

    canonical_url = f"{SITE_URL}/blog/{slug}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {SITE_NAME}</title>
    <meta name="description" content="{meta_description}">
    <meta name="author" content="{AUTHOR_NAME}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="{SITE_NAME}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{meta_description}">

    <!-- Article metadata -->
    <meta property="article:published_time" content="{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}">
    <meta property="article:author" content="{AUTHOR_NAME}">

    <style>
        :root {{
            --bg: #0a0a0f;
            --surface: #12121a;
            --border: #1e1e2e;
            --text: #e0e0e8;
            --text-muted: #8888a0;
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.15);
            --heading: #f0f0f8;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.75;
            font-size: 17px;
        }}

        .container {{
            max-width: 740px;
            margin: 0 auto;
            padding: 60px 24px 100px;
        }}

        /* ─── Header ─── */
        .blog-header {{
            margin-bottom: 48px;
            padding-bottom: 32px;
            border-bottom: 1px solid var(--border);
        }}

        .blog-header .meta {{
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .blog-header h1 {{
            font-size: 2.4rem;
            font-weight: 800;
            color: var(--heading);
            line-height: 1.2;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
        }}

        .blog-header .description {{
            font-size: 1.15rem;
            color: var(--text-muted);
            line-height: 1.6;
        }}

        /* ─── Content ─── */
        article h2 {{
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--heading);
            margin: 48px 0 16px;
            letter-spacing: -0.01em;
        }}

        article h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--heading);
            margin: 36px 0 12px;
        }}

        article p {{
            margin-bottom: 20px;
        }}

        article strong {{
            color: var(--heading);
            font-weight: 600;
        }}

        article em {{
            color: var(--accent);
            font-style: italic;
        }}

        article a {{
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s;
        }}

        article a:hover {{
            border-bottom-color: var(--accent);
        }}

        article ul, article ol {{
            margin: 0 0 20px 24px;
        }}

        article li {{
            margin-bottom: 8px;
        }}

        article blockquote {{
            border-left: 3px solid var(--accent);
            margin: 24px 0;
            padding: 16px 24px;
            background: var(--accent-glow);
            border-radius: 0 8px 8px 0;
            color: var(--text);
        }}

        article blockquote p {{
            margin-bottom: 0;
        }}

        article code {{
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            background: var(--surface);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            border: 1px solid var(--border);
        }}

        article pre {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin: 24px 0;
        }}

        article pre code {{
            background: none;
            border: none;
            padding: 0;
        }}

        /* ─── Table of Contents ─── */
        article ul:first-of-type {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px 20px 20px 40px;
            margin-bottom: 36px;
        }}

        /* ─── Footer ─── */
        .blog-footer {{
            margin-top: 64px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 14px;
            color: var(--text-muted);
        }}

        .blog-footer a {{
            color: var(--accent);
            text-decoration: none;
        }}

        /* ─── Responsive ─── */
        @media (max-width: 640px) {{
            .blog-header h1 {{
                font-size: 1.8rem;
            }}
            .container {{
                padding: 32px 16px 60px;
            }}
        }}
    </style>

    <!-- Inter font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="blog-header">
            <div class="meta">{SITE_NAME} &middot; {date} &middot; {AUTHOR_NAME}</div>
            <h1>{title}</h1>
            <p class="description">{meta_description}</p>
        </header>

        <article>
            {body_html}
        </article>

        <footer class="blog-footer">
            <p>&copy; {datetime.utcnow().year} <a href="{SITE_URL}">{SITE_NAME}</a>. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>"""
