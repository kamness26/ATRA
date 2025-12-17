# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Caption Service – ATRA (Joanie Edition v2.2)
#
# IG captions now automatically append the Amazon link.
# FB captions remain unchanged.

import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Amazon CTA settings
AMAZON_URL = os.getenv("AMAZON_URL", "https://a.co/d/5IG67WF")

# Explicit mood signals
EXPLICIT_CAPTION_PHRASES = {
    "corporate_burnout": [
        "Corporate burnout is doing numbers", 
        "Peak burnout vibes today",
        "Running on fumes and sarcasm",
    ],
    "sunday_scaries": [
        "The Sunday Scaries are creeping",
        "Sunday dread is loud",
        "Mentally preparing for Monday (and failing)",
    ],
}

# Implicit emotional shading
IMPLICIT_SCENTS = {
    "adhd_spiral": "with a brain sprinting in twelve directions",
    "delusional_romantic": "with dangerously delusional romantic optimism",
    "existentially_exhausted": "while questioning every life choice ever",
}

def _generate_caption(system_prompt: str, base_prompt: str, mode: str) -> str:
    """Internal helper for generating caption text."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": f"Prompt:\n{base_prompt}\nMode:\n{mode}"},
        ],
        temperature=0.85,
        max_tokens=120,
    )
    caption = response.choices[0].message.content.strip()
    return caption.replace("\n", " ").strip()

def _strip_emojis(text: str) -> str:
    if not text:
        return text
    emoji_pattern = re.compile(
        "["  # broadly covers most emoji + symbols used as emoji
        "\U0001F1E6-\U0001F1FF"  # flags
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # geometric shapes extended
        "\U0001F800-\U0001F8FF"  # supplemental arrows-c
        "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
        "\U0001FA00-\U0001FAFF"  # symbols & pictographs extended-a
        "\u2600-\u26FF"          # misc symbols
        "\u2700-\u27BF"          # dingbats
        "\uFE0F"                 # variation selector-16
        "]",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()

# -------------------------------------------------
# INSTAGRAM CAPTIONS (with Amazon link appended)
# -------------------------------------------------

def generate_instagram_caption(base_prompt: str, mode: str) -> str:
    """
    IG Caption Rules:
    - One punchy line (8–20 words)
    - Slight Joanie-mode flavor
    - 0–1 emojis max
    - No hashtags
    """

    # Mood hint
    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = f"{EXPLICIT_CAPTION_PHRASES[mode][0]}. "
    else:
        mood_hint = f"{IMPLICIT_SCENTS[mode]}, "

    system_prompt = f"""
    You are Joanie writing Instagram captions for 'You Won't Believe This $H!T'.

    Requirements:
    - ONE punchy, clever line (8–20 words)
    - Incorporate this mood hint naturally: "{mood_hint}"
    - Slightly chaotic, witty, self-aware
    - 0–1 emojis MAX
    - No hashtags
    - No line breaks
    - Connect loosely to the journaling prompt
    """

    # Base caption from GPT
    caption = _generate_caption(system_prompt, base_prompt, mode)

    # Amazon CTA (always added)
    amazon_block = (
        "\n\n📖 Available now on Amazon 👇\n"
        f"{AMAZON_URL}"
    )

    return caption + amazon_block

# -------------------------------------------------
# FACEBOOK CAPTIONS (with Amazon CTA appended)
# -------------------------------------------------

def generate_facebook_caption(base_prompt: str, mode: str) -> str:
    """
    FB Caption Rules:
    - 1–2 short sentences
    - Mini-narrative
    - No hashtags
    """

    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = EXPLICIT_CAPTION_PHRASES[mode][1]
    else:
        mood_hint = IMPLICIT_SCENTS[mode]

    system_prompt = f"""
    You are Joanie writing Facebook captions for 'You Won't Believe This $H!T'.

    Requirements:
    - Write 1–2 short sentences as a mini confession/story.
    - Incorporate this tone subtly: "{mood_hint}"
    - Blend humor with emotional self-awareness.
    - Do NOT use any emoji. (CTA block includes emojis.)
    - No hashtags.
    - No line breaks.
    """

    caption = _generate_caption(system_prompt, base_prompt, mode)
    caption = _strip_emojis(caption)

    # Use the same CTA block as IG
    amazon_block = (
        "\n\n📖 Available now on Amazon 👇\n"
        f"{AMAZON_URL}"
    )

    return caption + amazon_block
