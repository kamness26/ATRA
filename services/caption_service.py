# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Caption Service – ATRA (Joanie Edition v2.0)
#
# Medium Joanie personality influence:
# - IG captions: punchy, witty, mood-tinted  
# - FB captions: mini-narrative, warm, self-aware, mood-flavored  
#
# Mixed explicitness:
#   corporate_burnout      → explicit tone  
#   sunday_scaries         → explicit tone  
#   adhd_spiral            → implicit tone  
#   delusional_romantic    → implicit tone  
#   existentially_exhausted → implicit tone  
#

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
        max_tokens=80,
    )

    caption = response.choices[0].message.content.strip()
    return caption.replace("\n", " ").strip()


def generate_instagram_caption(base_prompt: str, mode: str) -> str:
    """
    IG Caption Rules:
    - One punchy line (8–20 words)
    - Slight Joanie-mode flavor
    - 0–1 emojis max
    - No hashtags
    """

    # Prepare mood flavor
    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = f"{EXPLICIT_CAPTION_PHRASES[mode][0]}. "
    else:
        mood_hint = f"{IMPLICIT_SCENTS[mode]}, "  # implicit

    system_prompt = f"""
    You are Joanie writing Instagram captions for 'You Won't Believe This $H!T'.

    Requirements:
    - ONE punchy, clever line (8–20 words)
    - Incorporate this mood hint naturally: "{mood_hint}"
    - Slightly chaotic, witty, self-aware
    - 0–1 emojis MAX
    - No hashtags
    - No line breaks
    - Should connect loosely to the journaling prompt
    """

    return _generate_caption(system_prompt, base_prompt, mode)


def generate_facebook_caption(base_prompt: str, mode: str) -> str:
    """
    FB Caption Rules:
    - 1–2 short sentences
    - Mini-narrative, tiny confession or emotional moment
    - Includes EXACTLY one emoji
    - Slight Joanie-mode flavor
    - No hashtags, no links
    """

    # Select explicit or implicit mood flavor
    if mode in EXPLICIT_CAPTION_PHRASES:
        mood_hint = EXPLICIT_CAPTION_PHRASES[mode][1]
    else:
        mood_hint = IMPLICIT_SCENTS[mode]

    system_prompt = f"""
    You are Joanie writing Facebook captions for 'You Won't Believe This $H!T'.

    Requirements:
    - Write 1–2 short sentences as a mini story/confession.
    - Incorporate this tone subtly: "{mood_hint}"
    - Mix humor with emotional self-awareness.
    - End with EXACTLY one emoji.
    - No hashtags, no links.
    - No line breaks.
    """

    return _generate_caption(system_prompt, base_prompt, mode)
