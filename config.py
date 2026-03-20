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
    # Investment & Alternative Data
    "alternative data investing trends",
    "venture capital deal intelligence",
    "private equity data due diligence",
    "hedge fund alternative data",
    "M&A market intelligence data",
    "ESG data analytics investing",
    "portfolio analytics technology",
    "investment research data tools",
    "alpha generation data signals",
    "quant fund data strategy",

    # AI & Machine Learning
    "machine learning training data",
    "enterprise AI adoption trends",
    "foundation model competition",
    "AI infrastructure spending",
    "synthetic data market",
    "large language model business",
    "AI agent automation business",
    "AI regulation policy",
    "generative AI revenue models",
    "AI chip semiconductor competition",

    # Data Industry & Infrastructure
    "data marketplace business model",
    "data monetization strategy",
    "data as a service market",
    "data governance compliance",
    "data quality enterprise",
    "cloud data warehouse trends",
    "data licensing business",
    "data broker regulation",
    "data privacy regulation impact",
    "real time data analytics",

    # Corporate Strategy & Intelligence
    "competitive intelligence technology",
    "market intelligence platform",
    "business intelligence trends",
    "predictive analytics enterprise",
    "corporate strategy data driven",
    "decision intelligence analytics",
    "company growth signals data",
    "digital transformation metrics",
    "strategic workforce planning",
    "B2B sales intelligence",

    # Industry News & Trends
    "technology industry news",
    "startup funding rounds",
    "fintech industry trends",
    "cybersecurity industry news",
    "climate tech business",
    "semiconductor industry trends",
    "biotech pharma deals",
    "robotics automation industry",
    "quantum computing business",
    "space industry commercial",
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

# Blog generation settings
MAX_TOKENS = 4096
OUTPUT_DIR = BLOG_OUTPUT_DIR
TARGET_WORD_COUNT_MIN = 800
TARGET_WORD_COUNT_MAX = 1500
