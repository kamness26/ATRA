# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Caption Service – ATRA (Joanie Edition v2.2)
#
# IG captions now automatically append the Amazon link.
# FB captions remain unchanged.

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        "https://a.co/d/5IG67WF"
    )

    return caption + amazon_block

# -------------------------------------------------
# FACEBOOK CAPTIONS (unchanged)
# -------------------------------------------------

def generate_facebook_caption(base_prompt: str, mode: str) -> str:
    """
    FB Caption Rules:
    - 1–2 short sentences
    - Mini-narrative
    - Ends with EXACTLY one emoji
    - No hashtags, no links
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
    - End with EXACTLY one emoji.
    - No hashtags, no links.
    - No line breaks.
    """

    return _generate_caption(system_prompt, base_prompt, mode)
