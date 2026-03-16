"""Vivameda Blog Agent — Configuration"""
import os

# ─── API Keys ──────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# ─── Model Settings ───────────────────────────────────────────
MODEL = "claude-sonnet-4-20250514"
BLOG_OUTPUT_DIR = os.getenv("BLOG_OUTPUT_DIR", "./output")

# ─── Topic Discovery ─────────────────────────────────────────
# 50 diverse search domains. 2 random ones picked per run.
# The blog agent's job: find trending news in ANY of these areas,
# then Claude flips it into a Vivameda workforce intelligence angle.
TOPIC_DOMAINS = [
    # Core
    "workforce intelligence",
    "people analytics trends",
    "talent data insights",
    "organizational intelligence",
    "labor market analysis",
    "HR technology news",

    # AI & ML
    "artificial intelligence jobs impact",
    "generative AI workforce",
    "machine learning enterprise",
    "AI automation replacing jobs",
    "AI hiring tools trends",
    "large language model business",

    # Big data & infrastructure
    "big data market trends",
    "data infrastructure spending",
    "data pipeline engineering",
    "Snowflake Databricks news",
    "data governance enterprise",
    "data quality management",
    "data monetization business",
    "data marketplace trends",
    "data privacy regulation",

    # Business intelligence
    "business intelligence trends",
    "predictive analytics enterprise",
    "competitive intelligence tools",
    "market intelligence platform",

    # B2B & SaaS
    "B2B data industry news",
    "SaaS growth metrics",
    "startup funding news",
    "vertical SaaS trends",
    "API economy growth",

    # Investment
    "alternative data investing",
    "private equity acquisitions",
    "human capital due diligence",
    "headcount data investment",
    "ESG workforce metrics",

    # Economics
    "labor market report",
    "wage growth trends",
    "job openings data",
    "remote work productivity",
    "gig economy statistics",

    # Industry verticals
    "marketing agency industry",
    "fintech hiring trends",
    "cybersecurity talent gap",
    "climate tech workforce",
    "healthcare staffing shortage",
    "semiconductor workforce",

    # Future of work
    "four day work week data",
    "hybrid work research",
    "employee burnout data",
    "upskilling reskilling trends",
    "digital nomad workforce",

    # Geopolitics
    "US China tech talent",
    "nearshoring reshoring jobs",
    "India tech outsourcing",
    "European tech trends",

    # Contrarian
    "HR tech failing",
    "job title inflation",
    "quiet quitting data",
    "performance review broken",

    # Emerging tech
    "quantum computing talent",
    "robotics workforce",
    "autonomous vehicles jobs",
    "edge computing growth",
]

# Keywords to boost relevance (expanded)
RELEVANCE_KEYWORDS = [
    "data", "intelligence", "workforce", "talent", "HR",
    "analytics", "enterprise", "AI", "machine learning",
    "hiring", "retention", "labor market", "skills gap",
    "recruitment", "employee", "organizational",
    "alternative data", "headcount", "attrition",
    "gig economy", "remote work", "automation",
    "private equity", "investment", "startup",
    "infrastructure", "pipeline", "big data",
    "governance", "monetization", "platform",
    "prediction", "signal", "trend",
    "disruption", "transformation", "future",
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
