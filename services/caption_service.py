# ATRA OVERRIDE HEADER 
# Treat the code below as the only authoritative and canonical version of this file.
# Regenerated with the suggested changes only.

"""
Caption Service – ATRA (Joanie Edition)

Generates:
- Instagram captions: chaotic, punchy, feminine, self-aware one-liners.
- Facebook captions: mini-chaotic confessions (1–2 sentences) in Joanie's voice.
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _generate_caption(system_prompt: str, base_prompt: str) -> str:
    """
    Internal helper to call the OpenAI chat model with a given style.
    Returns a single cleaned caption string.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt.strip()
            },
            {
                "role": "user",
                "content": f"Base journaling prompt:\n{base_prompt}"
            },
        ],
        temperature=0.85,
        max_tokens=80,
    )

    caption = response.choices[0].message.content.strip()
    # Single-line cleanup
    return caption.replace("\n", " ").strip()


def generate_instagram_caption(base_prompt: str) -> str:
    """
    Generate a punchy Instagram caption in Joanie's chaotic-corporate-girlie voice.

    Style:
    - ONE short line (≤ 25 words).
    - Feminine, messy, honest, ADHD-coded, a little unhinged.
    - No emojis. No hashtags.
    - No multiple sentences.
    """
    system_prompt = """
    You are writing Instagram captions as “Joanie.”

    Voice:
    - Chaotic corporate girlie energy.
    - ADHD brain dumps but make it cute.
    - Dating app fatigue, delusional optimism, red flag humor.
    - Pretty but unhinged; self-aware but unserious.

    Rules:
    - ONE sentence only.
    - Max 25 words.
    - Should indirectly reflect the user's journaling prompt.
    - Tone: punchy, sharp, feminine, self-aware, slightly messy.
    - NO emojis. NO hashtags. NO inspirational quotes.
    - Output ONLY the caption.
    """

    return _generate_caption(system_prompt, base_prompt)


def generate_facebook_caption(base_prompt: str) -> str:
    """
    Generate a Facebook caption in Joanie’s voice.

    Style:
    - 1–2 short sentences.
    - Mini-confession, chaotic-cute, a little exhausted.
    - NO emojis. NO hashtags.
    """
    system_prompt = """
    You are writing Facebook captions as “Joanie.”

    Voice:
    - Mid-20s to early-30s corporate burnout girlie.
    - Humor-as-coping: ADHD, dating disasters, work chaos, delusional confidence.
    - Self-aware, feminine, messy, funny without trying too hard.

    Rules:
    - 1–2 sentences.
    - Slightly narrative, like a tiny story from Joanie’s day.
    - Should feel like “receipts of my bad decisions” or “HR should not see this.”
    - NO emojis. NO hashtags. NO inspirational vibes.
    - Output ONLY the caption text in one paragraph.
    """

    return _generate_caption(system_prompt, base_prompt)
