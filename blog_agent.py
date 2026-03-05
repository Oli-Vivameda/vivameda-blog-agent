"""
Vivameda Blog Agent — Main Script

Automated daily blog post generation pipeline:
  1. Discover trending topics via search APIs
  2. Select the best topic using Claude
  3. Push to Lovable site via Supabase Edge Function (default)
  4. Optionally also save a local HTML copy

Usage:
    python blog_agent.py                  # Generate + push to Lovable as draft
    python blog_agent.py --publish        # Generate + publish live immediately
    python blog_agent.py --local-only     # Generate local HTML only (no Supabase)
    python blog_agent.py --dry-run        # Show topic selection without writing
    python blog_agent.py --topic "..."    # Override with a specific topic
"""
import asyncio
import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic

from config import (
    ANTHROPIC_API_KEY,
    MODEL,
    MAX_TOKENS,
    OUTPUT_DIR,
    TARGET_WORD_COUNT_MIN,
    TARGET_WORD_COUNT_MAX,
)
from style_guide import SYSTEM_PROMPT, BLOG_GENERATION_PROMPT, TOPIC_SELECTION_PROMPT
from topic_discovery import discover_topics
from html_template import render_html
from supabase_publisher import publish_to_supabase

# ─── Logging ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── History tracking (prevents repeat topics) ──────────────────
HISTORY_FILE = Path(OUTPUT_DIR) / ".topic_history.json"


def load_topic_history() -> list[str]:
    """Load previously written topic titles."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_topic_history(history: list[str]):
    """Save topic history, keeping last 90 entries."""
    history = history[-90:]  # Rolling 90-day window
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# ─── Claude API ──────────────────────────────────────────────────
def get_client() -> anthropic.Anthropic:
    """Initialize Anthropic client."""
    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY not set. Export it or add to .env")
        sys.exit(1)
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def call_claude(client: anthropic.Anthropic, system: str, prompt: str) -> str:
    """Send a message to Claude and return the text response."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ─── Pipeline Steps ─────────────────────────────────────────────
async def step_discover(client: anthropic.Anthropic) -> dict:
    """Step 1 & 2: Discover trending topics and select the best one."""
    logger.info("🔍 Discovering trending topics...")
    raw_topics = await discover_topics()

    if not raw_topics:
        logger.error("No topics found from any source")
        sys.exit(1)

    # Format topics for Claude
    topics_text = "\n".join(
        f"- {t['title']}: {t['snippet']}" for t in raw_topics
    )

    previous = load_topic_history()
    previous_text = "\n".join(f"- {t}" for t in previous[-30:]) or "None yet"

    logger.info("🧠 Selecting best topic with Claude...")
    selection_raw = call_claude(
        client,
        "You are a content strategist. Respond ONLY with valid JSON, no markdown fences.",
        TOPIC_SELECTION_PROMPT.format(
            topics=topics_text,
            previous_topics=previous_text,
        ),
    )

    # Parse JSON response (strip markdown fences if present)
    cleaned = re.sub(r"```json\s*|\s*```", "", selection_raw).strip()
    try:
        selection = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse topic selection:\n{selection_raw}")
        # Fallback: use the top-scored topic directly
        selection = {
            "selected_topic": raw_topics[0]["title"],
            "context": raw_topics[0]["snippet"],
            "angle": "Analyze this from a workforce intelligence perspective",
            "why": "Top-ranked topic by relevance score",
        }

    logger.info(f"📌 Selected: {selection['selected_topic']}")
    logger.info(f"   Angle: {selection.get('angle', 'N/A')}")

    return selection


def step_generate(client: anthropic.Anthropic, topic_info: dict) -> str:
    """Step 3: Generate the blog post."""
    logger.info("✍️  Generating blog post...")

    context = (
        f"Topic: {topic_info['selected_topic']}\n"
        f"Context: {topic_info.get('context', '')}\n"
        f"Angle: {topic_info.get('angle', '')}"
    )

    post_markdown = call_claude(
        client,
        SYSTEM_PROMPT,
        BLOG_GENERATION_PROMPT.format(
            topic=topic_info["selected_topic"],
            context=context,
        ),
    )

    # Word count check
    word_count = len(post_markdown.split())
    logger.info(f"📝 Generated {word_count} words")

    if word_count < TARGET_WORD_COUNT_MIN:
        logger.warning(f"Post is short ({word_count} words). Requesting expansion...")
        post_markdown = call_claude(
            client,
            SYSTEM_PROMPT,
            f"The following blog post is too short at {word_count} words. "
            f"Expand it to {TARGET_WORD_COUNT_MIN} to {TARGET_WORD_COUNT_MAX} words "
            f"while maintaining the same voice and structure. Add depth to existing "
            f"sections, do NOT add filler.\n\n{post_markdown}",
        )
        logger.info(f"📝 Expanded to {len(post_markdown.split())} words")

    # Strip any em/en dashes that slipped through
    post_markdown = post_markdown.replace("—", ",").replace("–", ",")

    return post_markdown


def step_render(post_markdown: str) -> tuple[str, str, str]:
    """Step 4: Parse markdown and render to HTML."""
    lines = post_markdown.strip().split("\n")

    # Extract title (first H1 line)
    title = "Untitled Post"
    meta = ""
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            title = line.lstrip("# ").strip()
            body_start = i + 1
            break

    # Extract meta description
    for i in range(body_start, min(body_start + 3, len(lines))):
        if lines[i].startswith("META:"):
            meta = lines[i].replace("META:", "").strip()
            body_start = i + 1
            break

    body_markdown = "\n".join(lines[body_start:]).strip()

    # Generate slug
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    date_prefix = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{date_prefix}-{slug}.html"

    html = render_html(
        title=title,
        meta_description=meta,
        body_markdown=body_markdown,
        slug=slug,
    )

    return html, filename, title


def step_save(html: str, filename: str):
    """Step 5: Save HTML file to output directory."""
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    filepath = output_path / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info(f"✅ Saved: {filepath}")
    return filepath


# ─── Main ────────────────────────────────────────────────────────
async def main():
    parser = argparse.ArgumentParser(description="Vivameda Daily Blog Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show topic selection only, don't generate a post",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Override automatic topic selection with a specific topic",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately (default is draft)",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Save local HTML only, don't push to Supabase",
    )
    args = parser.parse_args()

    client = get_client()

    # ── Topic selection ──────────────────────────────────────────
    if args.topic:
        topic_info = {
            "selected_topic": args.topic,
            "context": "",
            "angle": "Write from a workforce intelligence perspective",
        }
        logger.info(f"📌 Using manual topic: {args.topic}")
    else:
        topic_info = await step_discover(client)

    if args.dry_run:
        print("\n" + "═" * 60)
        print("DRY RUN — Topic Selection")
        print("═" * 60)
        print(json.dumps(topic_info, indent=2))
        return

    # ── Publish to Lovable via Supabase (default) ────────────────
    if not args.local_only:
        instructions = (
            f"Angle: {topic_info.get('angle', '')}\n"
            f"Context: {topic_info.get('context', '')}\n\n"
            f"STYLE GUIDE:\n"
            f"- Conversational and direct. Address the reader as 'you.'\n"
            f"- Use relatable analogies from everyday life.\n"
            f"- Bold key insights at the end of each section.\n"
            f"- End with a provocative closing statement.\n"
            f"- 800-1200 words. No generic AI language.\n"
            f"- Position workforce data as infrastructure, not a contact database.\n"
            f"- Target audience: VPs of Data, Talent Analytics leads, Investment Research Directors."
        )

        result = publish_to_supabase(
            topic=topic_info["selected_topic"],
            instructions=instructions,
            publish=args.publish,
        )

        # Update history
        history = load_topic_history()
        history.append(topic_info["selected_topic"])
        save_topic_history(history)

        if result:
            print("\n" + "═" * 60)
            print(f"Blog Post {'Published' if args.publish else 'Saved as Draft'}!")
            print("═" * 60)
            print(f"  Title:  {result.get('title', topic_info['selected_topic'])}")
            print(f"  URL:    {result.get('url', 'N/A')}")
            print(f"  Status: {'live' if args.publish else 'draft'}")
            print(f"  Topic:  {topic_info['selected_topic']}")
            print("═" * 60)
        else:
            logger.error("Supabase publish failed. Run with --local-only to save locally.")
        return

    # ── Local-only: Generate with Claude + save HTML ─────────────
    post_markdown = step_generate(client, topic_info)

    html, filename, title = step_render(post_markdown)
    filepath = step_save(html, filename)

    history = load_topic_history()
    history.append(topic_info["selected_topic"])
    save_topic_history(history)

    print("\n" + "═" * 60)
    print("Blog Post Generated (local only)")
    print("═" * 60)
    print(f"  Title:  {title}")
    print(f"  File:   {filepath}")
    print(f"  Words:  {len(post_markdown.split())}")
    print(f"  Topic:  {topic_info['selected_topic']}")
    print("═" * 60)


if __name__ == "__main__":
    asyncio.run(main())
