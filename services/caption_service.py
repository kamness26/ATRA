# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Caption Service – ATRA (Joanie Edition v2.2 – Warm Chaos IG)
#
# Joanie personality rules:
# - IG captions → warm, witty, lightly chaotic, never depressing
# - FB captions → unchanged (mini-narrative, mood-influenced)
#
# Explicit modes:
#   corporate_burnout, sunday_scaries
# Implicit modes:
#   adhd_spiral, delusional_romantic, existentially_exhausted
#
# NOTE:
# FB functionality remains fully intact from v2.1.

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Explicit mood signals for captions
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

# Implicit emotional shading for other modes
IMPLICIT_SCENTS = {
    "adhd_spiral": "with a brain sprinting in twelve directions",
    "delusional_romantic": "with dangerously delusional romantic optimism",
    "existentially_exhausted": "while questioning every life choice ever",
}

def _generate_caption(system_prompt: str, base_prompt: str, mode: str) -> str:
    """Internal helper to generate caption text."""
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
# INSTAGRAM CAPTIONS (UPDATED — Warm Chaos Edition)
# -------------------------------------------------

def generate_instagram_caption(base_prompt: str, mode: str) -> str:
    """
    IG Caption Rules (Warm Chaos):
    - One warm, witty, relatable line (8–20 words)
    - Light Joanie flavor but NEVER sad or heavy
    - 0–1 emojis max
    - No hashtags
    """

    # Mood hints kept SAME — but usage changes to warm tone
    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = EXPLICIT_CAPTION_PHRASES[mode][0]
    else:
        mood_hint = IMPLICIT_SCENTS[mode]

    system_prompt = f"""
    You are Joanie writing Instagram captions for 'You Won't Believe This $H!T'.

    NEW TONE:
    - Warm, lightly chaotic, relatable, human
    - Messy life moments, but in a funny, cozy, “we’re all in this together” way
    - Absolutely NO darkness, sadness, doom, existential pain, or bleak humor

    Requirements:
    - ONE line, 8–20 words max
    - Slight flavor of this mood: "{mood_hint}"
    - Light, witty, gently self-aware
    - 0–1 emojis MAX
    - No hashtags
    - No line breaks
    - Should loosely connect to the journaling prompt

    Style examples (DO NOT copy — match tone):
    - "My brain scheduled three thoughts at once and somehow they all showed up."
    - "Today’s chaos was weirdly wholesome, and honestly I’m not mad at it."
    - "Trying to be an adult but also vibing through the confusion."
    """

    return _generate_caption(system_prompt, base_prompt, mode)

# -------------------------------------------------
# FACEBOOK CAPTIONS (unchanged)
# -------------------------------------------------

def generate_facebook_caption(base_prompt: str, mode: str) -> str:
    """
    FB Caption Rules:
    - 1–2 short sentences
    - Mini-narrative, tiny confession or emotional moment
    - Includes EXACTLY one emoji
    - Slight Joanie-mode flavor
    - No hashtags, no links
    """

    # Explicit or implicit mood flavor
    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = EXPLICIT_CAPTION_PHRASES[mode][1]
    else:
        mood_hint = IMPLICIT_SCENTS[mode]

    system_prompt = f"""
    You are Joanie writing Facebook captions for 'You Won't Believe This $H!T'.

    Requirements:
    - Write 1–2 short sentences as a mini story/confession.
    - Incorporate this tone subtly: "{mood_hint}"
    - Blend humor with emotional self-awareness.
    - End with EXACTLY one emoji.
    - No hashtags, no links.
    - No line breaks.
    """

    return _generate_caption(system_prompt, base_prompt, mode)
