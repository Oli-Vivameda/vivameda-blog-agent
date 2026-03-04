# Vivameda Blog Agent

Automated daily blog post generator for [Vivameda](https://vivameda.com). Discovers trending workforce intelligence topics, generates opinionated long-form content using Claude, and outputs styled HTML ready for publishing.

## How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Topic Discovery │────▶│  Topic Selection │────▶│  Blog Generation│
│  (Brave/NewsAPI) │     │  (Claude)        │     │  (Claude)       │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                         ┌──────────────────┐     ┌───────▼────────┐
                         │   Save HTML +    │◀────│  Render HTML   │
                         │   Update History │     │  (Template)    │
                         └──────────────────┘     └────────────────┘
```

**Pipeline:**
1. **Discover** — Queries Brave Search or NewsAPI for trending topics in workforce data, HR-tech, and AI
2. **Select** — Claude picks the best topic, avoids repeats using a rolling 90-day history
3. **Generate** — Claude writes an 800–1,200 word post using a custom style guide
4. **Render** — Markdown is converted to a responsive, dark-themed HTML page with SEO metadata
5. **Save** — HTML file is saved to `./output/` with a date-prefixed filename

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/your-org/vivameda-blog-agent.git
cd vivameda-blog-agent
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env with your keys

# 3. Export keys (or use a .env loader)
export ANTHROPIC_API_KEY="sk-ant-..."
export BRAVE_API_KEY="..."        # optional but recommended

# 4. Run
python blog_agent.py
```

## Usage

```bash
# Generate a post (full pipeline)
python blog_agent.py

# Preview topic selection only
python blog_agent.py --dry-run

# Write about a specific topic
python blog_agent.py --topic "Why longitudinal data beats point-in-time snapshots"
```

## Automated Daily Runs (GitHub Actions)

The included workflow runs daily at 07:00 UTC (09:00 Cyprus time).

**Setup:**
1. Push this repo to GitHub
2. Add these repository secrets (Settings → Secrets → Actions):
   - `ANTHROPIC_API_KEY` (required)
   - `BRAVE_API_KEY` (recommended)
   - `NEWSAPI_KEY` (optional fallback)
3. The workflow auto-commits new posts to `output/`

You can also trigger it manually from the Actions tab.

## Configuration

Edit `config.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `MODEL` | `claude-sonnet-4-5-20250929` | Claude model for generation |
| `TARGET_WORD_COUNT_MIN` | 800 | Minimum word count |
| `TARGET_WORD_COUNT_MAX` | 1200 | Maximum word count |
| `TOPIC_DOMAINS` | workforce/HR/AI topics | Search query domains |
| `SITE_NAME` | Vivameda | Brand name in HTML |
| `SITE_URL` | https://vivameda.com | Canonical URL base |

## Writing Style

The style guide in `style_guide.py` is extracted from these reference posts:
- [Supervised Thought: AI's Rule-based Training vs. Unchecked Learning](https://www.mechanosophism.com/blog/rules-in-ai-vs-human-learning/)
- [AI Models Are Generating Religious Outputs](https://www.mechanosophism.com/blog/religous-output-from-ai/)
- [What Are Halvings?](https://ycash.substack.com/p/what-are-halvings)

Key characteristics: conversational authority, relatable analogies, bold punchline insights, and a provocative close. See `style_guide.py` for the full prompt.

## Output

Each run produces a file like:
```
output/2026-03-04-why-workforce-data-beats-gut-feel.html
```

The HTML includes:
- Responsive dark-themed styling
- Open Graph + Twitter Card meta tags
- SEO-friendly canonical URLs
- Clean typography (Inter font family)
- Mobile-optimized layout

## Project Structure

```
vivameda-blog-agent/
├── blog_agent.py          # Main pipeline script
├── config.py              # Configuration and API keys
├── style_guide.py         # Writing style prompts (extracted from examples)
├── topic_discovery.py     # Trending topic discovery (Brave/NewsAPI)
├── html_template.py       # HTML rendering with styling
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .github/
│   └── workflows/
│       └── daily-blog.yml # GitHub Actions daily cron
└── output/                # Generated blog posts
    └── .topic_history.json
```

## Cost Estimate

Per daily run (2 Claude API calls):
- Topic selection: ~500 input + ~200 output tokens
- Blog generation: ~800 input + ~2,000 output tokens
- **≈ $0.02–0.05/day** on Claude Sonnet

Search API: Brave free tier (2,000/month) covers daily use with headroom.

## License

Proprietary — Vivameda Ltd.
