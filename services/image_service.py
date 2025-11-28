# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Joanie Edition v2.0)
# Subtle mood influence:
# - corporate_burnout          → flatter, colder, minimal contrast
# - adhd_spiral                → slightly more energetic composition cues
# - delusional_romantic        → warm, dreamy micro-tones
# - existentially_exhausted    → cool, empty-space bias
# - sunday_scaries             → slightly darker atmospheric cues
#
# STILL strict brand rules:
# - Atty = upside-down SMILEY (smiling, not frowning), must be visible
# - 8% padding safe zone ALWAYS
# - headline only (8–12 words)
# - bold sans-serif or distressed
# - no cartoons, no people, no mascots
# - 1024x1024 JPEG output

import os
import base64
import random
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mood → subtle stylistic hints
MOOD_STYLES = {
    "corporate_burnout": """
        Overall mood: minimal contrast, colder tones, flatter paper texture.
        Lighting: soft, office-like neutrality.
        Composition: slightly rigid alignment.
    """,
    "adhd_spiral": """
        Overall mood: a touch more energetic, mild visual tension.
        Lighting: lively micro-contrast.
        Composition: slightly dynamic, but still clean and readable.
    """,
    "delusional_romantic": """
        Overall mood: subtle warmth, delicate dreamy undertone.
        Lighting: soft, warm highlights.
        Composition: gentle curves, softer spatial balance.
    """,
    "existentially_exhausted": """
        Overall mood: cooler palette bias, emptier negative space.
        Lighting: muted, slightly dim.
        Composition: sparse, minimal, slightly distant.
    """,
    "sunday_scaries": """
        Overall mood: mild darkness, heavier shadows.
        Lighting: soft vignette energy.
        Composition: grounded, still, slightly heavy at the bottom.
    """,
}


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating Joanie image ({mode}) for prompt: {prompt}")

    # core vs campaign mode still alive
    palette_mode = random.choice(["core", "campaign"])
    print(f"🖤 Visual palette: {palette_mode.upper()}")

    palette_rules = (
        "Colors: pure black & white only."
        if palette_mode == "core" else
        "Colors: mustard yellow, warm beige, and black only."
    )

    mood_style = MOOD_STYLES[mode]

    visual_prompt = f"""
    Create a clean poster-style graphic for the journal 'You Won’t Believe This $H!T'.

    TEXT RULES:
    - Use ONE short headline only (8–12 words) derived from: "{prompt}"
    - No paragraphs, no secondary text, no tiny copy.
    - Typography: bold sans-serif or distressed; high legibility.

    BRAND RULES:
    - Include Atty: an upside-down SMILEY FACE (smiling). Orientation must be inverted.
    - Atty may be hero or watermark but must be present.
    - No people, mascots, cartoons, illustrations of characters.

    LAYOUT / CROPPING:
    - Keep 8% padding on ALL sides.
    - Nothing may touch the edges.
    - Main text must never be cropped.
    - Balanced, modern composition.

    {palette_rules}

    MOOD INFLUENCE (subtle):
    {mood_style}

    Background: matte paper texture (very subtle).
    Output: square 1024x1024 image, photorealistic poster aesthetic.

    Respond ONLY with a finished image.
    """

    # --- OpenAI Image Call ---
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        n=1,
        size="1024x1024"
    )

    # Decode base64 → PIL Image
    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Output directory
    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"

    # Save JPEG (IG safe)
    pil_image.save(path, format="JPEG", quality=92)

    print(f"✅ Generated: {path}")
    return path
