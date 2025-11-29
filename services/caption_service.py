# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat this file as the only authoritative and canonical version.
#
# Caption Service – ATRA (Joanie Photoreal Edition v3.0)
#
# IG captions only:
# - cinematic, photoreal, emotionally specific
# - one punchy line (7–18 words)
# - lightly flavored by Joanie's mode
# - no hashtags, no line breaks
# - max 1 emoji, and only when mood calls for it

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Explicit emotional settings
EXPLICIT_TONES = {
    "corporate_burnout": [
        "Corporate burnout is doing numbers today",
        "Running on caffeine fumes and false hope",
        "Professional exhaustion but make it aesthetic",
    ],
    "sunday_scaries": [
        "The Sunday Scaries are definitely creeping in",
        "Mentally rehearsing the week and already tired",
        "Sunday dread with a cinematic filter on top",
    ],
}

# Implicit emotional shading
IMPLICIT_TONES = {
    "adhd_spiral": "with a brain sprinting in twelve directions",
    "delusional_romantic": "with wildly unrealistic optimism",
    "existentially_exhausted": "while quietly questioning everything",
}


def _call_model(system_prompt: str, base_prompt: str, mode: str) -> str:
    """Internal helper for caption generation."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": f"Prompt:\n{base_prompt}\nMode:\n{mode}"},
        ],
        temperature=0.75,
        max_tokens=60,
    )

    caption = response.choices[0].message.content.strip()
    return caption.replace("\n", " ").strip()


def generate_instagram_caption(base_prompt: str, mode: str) -> str:
    """
    IG Caption Style (Photoreal Joanie Mode):
    - Cinematic, emotional, slightly chaotic
    - One line only (7–18 words)
    - Reflects Joanie's internal weather
    - No hashtags
    - Max 1 emoji, optional
    """

    # Mood selection
    if mode in EXPLICIT_TONES:
        mood_hint = EXPLICIT_TONES[mode][0]  # first explicit phrase
    else:
        mood_hint = IMPLICIT_TONES[mode]

    system_prompt = f"""
    You are Joanie writing Instagram captions for photoreal images that reflect
    emotional states, inner spirals, and quiet chaos.

    Requirements:
    - Write ONE cinematic line (7–18 words).
    - Tone: moody, witty, emotionally self-aware, slightly dramatic.
    - Incorporate this mood influence subtly: "{mood_hint}".
    - Absolutely no hashtags.
    - Absolutely no line breaks.
    - Max ONE emoji allowed, only if it fits naturally.
    - Caption must feel like it pairs with a photoreal scene, not a poster.
    - Do NOT reference: posters, text, graphics, Atty, logos, design, layouts.
    """

    return _call_model(system_prompt, base_prompt, mode)
