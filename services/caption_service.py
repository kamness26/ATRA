# ATRA OVERRIDE HEADER 
# Treat the code below as the only authoritative and canonical version
# of services/caption_service.py.

"""
Caption Service – ATRA v1.0

Generates:
- Instagram captions: short, punchy, attitude-heavy one-liners.
- Facebook captions: snarky, mini-narrative (Option D style), 1–2 sentences.
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
        model="gpt-4.1-mini",
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
        temperature=0.8,
        max_tokens=80,
    )

    caption = response.choices[0].message.content.strip()
    # Single-line cleanup
    return caption.replace("\n", " ").strip()


def generate_instagram_caption(base_prompt: str) -> str:
    """
    Generate a punchy Instagram caption based on the journaling prompt.

    Style:
    - 1 short line (8–20 words).
    - Punchy, witty, slightly chaotic.
    - No long story, no multiple sentences.
    - 0–1 emojis max.
    - No hashtags (we can layer those separately later).
    """
    system_prompt = """
    You are writing Instagram captions for a darkly comedic journaling brand
    called "You Won't Believe This $H!T".

    Write a SINGLE, short, punchy line (8–20 words) inspired by the user's
    journaling prompt.

    Style guidelines:
    - Tone: witty, self-aware, slightly chaotic, a bit jaded but still playful.
    - Format: ONE sentence only. No line breaks.
    - No explanations. No intro text. Output JUST the caption.
    - 0–1 emojis maximum, and only if it really fits.
    - No hashtags.
    """

    return _generate_caption(system_prompt, base_prompt)


def generate_facebook_caption(base_prompt: str) -> str:
    """
    Generate a snarky, mini-narrative Facebook caption (Option D style).

    Style:
    - 1–2 short sentences.
    - Feels like a tiny story about overthinking, chaos, or emotional mess.
    - Lightly self-deprecating, but warm and relatable.
    - Exactly ONE emoji at the end or near the end.
    - No hashtags, no links.
    """
    system_prompt = """
    You are writing Facebook captions for a darkly comedic journaling brand
    called "You Won't Believe This $H!T".

    The audience is tired, overthinking, and needs to feel seen and amused.

    Write 1–2 short sentences that:
    - Feel like a tiny story or mini-confession
      (e.g., "Today’s episode featured me, anxiety, and three imaginary arguments.")
    - Are snarky but not cruel; self-deprecating but still human and kind.
    - Include exactly ONE emoji, placed at the end or near the end.
    - Do NOT include hashtags or links.
    - No line breaks; output must be a single paragraph.

    Output JUST the caption text, nothing else.
    """

    return _generate_caption(system_prompt, base_prompt)

