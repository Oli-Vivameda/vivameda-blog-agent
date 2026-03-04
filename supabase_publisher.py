"""
Vivameda Blog Agent — Supabase Publisher

Pushes blog posts to the Vivameda Lovable site via the Supabase Edge Function.
"""
import logging
import httpx

from config import SUPABASE_FUNCTION_URL, SUPABASE_ANON_KEY

logger = logging.getLogger(__name__)


def publish_to_supabase(
    topic: str,
    instructions: str = "",
    publish: bool = False,
) -> dict | None:
    """
    Call the Supabase Edge Function to generate and store a blog post.

    Args:
        topic: What the post should be about
        instructions: Extra guidance for tone/angle (optional)
        publish: If True, publish immediately. If False, save as draft.

    Returns:
        The response dict from the Edge Function, or None on failure.
    """
    if not SUPABASE_FUNCTION_URL:
        logger.error("SUPABASE_FUNCTION_URL not set in .env")
        return None

    headers = {
        "Content-Type": "application/json",
    }

    # Add auth header if anon key is available
    if SUPABASE_ANON_KEY:
        headers["Authorization"] = f"Bearer {SUPABASE_ANON_KEY}"

    payload = {
        "topic": topic,
        "publish": publish,
    }

    if instructions:
        payload["instructions"] = instructions

    logger.info(f"📡 Pushing to Supabase Edge Function...")
    logger.info(f"   Topic: {topic}")
    logger.info(f"   Mode: {'publish' if publish else 'draft'}")

    try:
        with httpx.Client(timeout=120) as client:  # Long timeout — AI generation takes time
            resp = client.post(
                SUPABASE_FUNCTION_URL,
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

            logger.info(f"✅ Post created successfully!")
            if "url" in data:
                logger.info(f"   URL: {data['url']}")
            if "title" in data:
                logger.info(f"   Title: {data['title']}")

            return data

    except httpx.HTTPStatusError as e:
        logger.error(f"Edge Function returned {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Failed to call Edge Function: {e}")
        return None
