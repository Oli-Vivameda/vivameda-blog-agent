"""
Vivameda Blog Agent — Configuration
"""
import os

# ─── LLM Settings ───────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("BLOG_MODEL", "claude-sonnet-4-5-20250929")
MAX_TOKENS = 4096

# ─── Content Settings ───────────────────────────────────────────
TARGET_WORD_COUNT_MIN = 800
TARGET_WORD_COUNT_MAX = 1200
OUTPUT_DIR = os.getenv("BLOG_OUTPUT_DIR", "./output")

# ─── Topic Discovery ────────────────────────────────────────────
# Brave Search API (free tier: 2,000 queries/month — perfect for daily use)
# Sign up: https://brave.com/search/api/
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")

# Fallback: NewsAPI (free tier: 100 requests/day)
# Sign up: https://newsapi.org/
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# Core topic domains for Vivameda
TOPIC_DOMAINS = [
    "workforce intelligence",
    "workforce analytics",
    "HR technology",
    "talent data",
    "organizational intelligence",
    "people analytics",
    "labor market trends",
    "enterprise data intelligence",
    "AI in HR",
    "B2B data industry",
]

# Keywords to boost relevance
RELEVANCE_KEYWORDS = [
    "data", "intelligence", "workforce", "talent", "HR",
    "analytics", "enterprise", "AI", "machine learning",
    "hiring", "retention", "labor market", "skills gap",
    "recruitment", "employee", "organizational",
]

# ─── Supabase / Lovable Publishing ──────────────────────────────
SUPABASE_FUNCTION_URL = os.getenv(
    "SUPABASE_FUNCTION_URL",
    "https://whxhqmagoqagcxbzzumz.supabase.co/functions/v1/blog-agent",
)
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# ─── HTML Template Settings ─────────────────────────────────────
SITE_NAME = "Vivameda"
SITE_URL = "https://vivameda.com"
AUTHOR_NAME = "Vivameda Intelligence"
