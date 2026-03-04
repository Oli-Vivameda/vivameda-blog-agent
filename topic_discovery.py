"""
Vivameda Blog Agent — Topic Discovery

Discovers trending topics relevant to workforce intelligence using:
  1. Brave Search API (primary)
  2. NewsAPI (fallback)
  3. Static rotation (emergency fallback)
"""
import json
import random
import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx

from config import (
    BRAVE_API_KEY,
    NEWSAPI_KEY,
    TOPIC_DOMAINS,
    RELEVANCE_KEYWORDS,
)

logger = logging.getLogger(__name__)


async def discover_topics() -> list[dict]:
    """
    Returns a list of trending topic dicts: [{"title": ..., "snippet": ..., "url": ...}]
    Tries Brave first, then NewsAPI, then falls back to static topics.
    """
    topics = []

    # ── Primary: Brave Search API ────────────────────────────────
    if BRAVE_API_KEY:
        topics = await _brave_search()
        if topics:
            logger.info(f"Brave Search returned {len(topics)} topics")
            return topics

    # ── Fallback: NewsAPI ────────────────────────────────────────
    if NEWSAPI_KEY:
        topics = await _newsapi_search()
        if topics:
            logger.info(f"NewsAPI returned {len(topics)} topics")
            return topics

    # ── Emergency fallback: static topic rotation ────────────────
    logger.warning("No search API available — using static topic rotation")
    return _static_fallback()


async def _brave_search() -> list[dict]:
    """Query Brave Search API for trending workforce/data topics."""
    topics = []
    # Pick 2 random domains to keep searches varied day-to-day
    queries = random.sample(TOPIC_DOMAINS, min(2, len(TOPIC_DOMAINS)))

    async with httpx.AsyncClient(timeout=15) as client:
        for query in queries:
            try:
                resp = await client.get(
                    "https://api.search.brave.com/res/v1/news/search",
                    headers={
                        "X-Subscription-Token": BRAVE_API_KEY,
                        "Accept": "application/json",
                    },
                    params={
                        "q": query,
                        "count": 5,
                        "freshness": "pw",  # past week
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                for result in data.get("results", []):
                    topics.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("description", ""),
                        "url": result.get("url", ""),
                        "source": "brave",
                    })
            except Exception as e:
                logger.error(f"Brave search failed for '{query}': {e}")

    return _score_and_rank(topics)


async def _newsapi_search() -> list[dict]:
    """Query NewsAPI for relevant articles from the past 3 days."""
    topics = []
    query = " OR ".join(random.sample(TOPIC_DOMAINS, min(3, len(TOPIC_DOMAINS))))
    from_date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d")

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "from": from_date,
                    "sortBy": "relevancy",
                    "pageSize": 10,
                    "language": "en",
                    "apiKey": NEWSAPI_KEY,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for article in data.get("articles", []):
                topics.append({
                    "title": article.get("title", ""),
                    "snippet": article.get("description", ""),
                    "url": article.get("url", ""),
                    "source": "newsapi",
                })
        except Exception as e:
            logger.error(f"NewsAPI search failed: {e}")

    return _score_and_rank(topics)


def _score_and_rank(topics: list[dict]) -> list[dict]:
    """Score topics by relevance keyword density and return top 8."""
    for topic in topics:
        text = f"{topic['title']} {topic['snippet']}".lower()
        topic["score"] = sum(1 for kw in RELEVANCE_KEYWORDS if kw.lower() in text)

    topics.sort(key=lambda t: t["score"], reverse=True)
    return topics[:8]


def _static_fallback() -> list[dict]:
    """Emergency fallback: rotating evergreen topics when APIs are unavailable."""
    evergreen = [
        {
            "title": "The Hidden Cost of Bad Workforce Data",
            "snippet": "Most companies make talent decisions on incomplete or outdated data. "
                       "What does that actually cost them?",
            "url": "",
            "source": "static",
        },
        {
            "title": "Why Longitudinal Data Beats Snapshots for Talent Intelligence",
            "snippet": "A single data pull tells you where someone is. Fifteen years of data "
                       "tells you where they're going.",
            "url": "",
            "source": "static",
        },
        {
            "title": "AI Labs Are Hiring — But From Where?",
            "snippet": "Tracking the talent migration patterns into frontier AI companies "
                       "reveals surprising feeder industries.",
            "url": "",
            "source": "static",
        },
        {
            "title": "The Death of the Job Board and the Rise of Intelligence-Led Recruiting",
            "snippet": "Enterprise hiring is shifting from reactive job postings to proactive "
                       "talent pipeline intelligence.",
            "url": "",
            "source": "static",
        },
        {
            "title": "What 250 Million Professional Records Tell Us About Career Velocity",
            "snippet": "Mapping promotion speed across industries, geographies, and company sizes "
                       "using longitudinal workforce data.",
            "url": "",
            "source": "static",
        },
        {
            "title": "HR-Tech Is Drowning in Dashboards — Where's the Intelligence?",
            "snippet": "The difference between workforce analytics and workforce intelligence "
                       "is the difference between reporting and prediction.",
            "url": "",
            "source": "static",
        },
        {
            "title": "How Investment Firms Use Workforce Data as an Alternative Signal",
            "snippet": "Headcount growth, attrition spikes, and hiring velocity as leading "
                       "indicators for company performance.",
            "url": "",
            "source": "static",
        },
        {
            "title": "The Skills Gap Isn't What You Think It Is",
            "snippet": "When you look at actual workforce data instead of survey results, "
                       "the skills gap narrative changes dramatically.",
            "url": "",
            "source": "static",
        },
    ]

    # Rotate based on day of year so it's not random
    day = datetime.utcnow().timetuple().tm_yday
    start = day % len(evergreen)
    return evergreen[start:] + evergreen[:start]
