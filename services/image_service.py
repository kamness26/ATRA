# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Joanie Edition v2.2 – Warm Chaos)
#
# Updated to remove depressing / dark tones:
# - NO heavy shadows
# - NO gray, cold, empty spaces
# - NO bleakness or sterile minimalism
#
# New aesthetic target:
# - Warm, cozy, lived-in chaos
# - Golden-hour lighting, natural light, soft highlights
# - Real-life clutter (keys, notebooks, bags, coffee cups, headphones, receipts)
# - Scenes that look human, relatable, funny in their messiness
# - A snapshot of everyday life, not sad or lonely
#
# Modes still influence subtle flavor, but stay warm:
#   corporate_burnout        → warm office clutter, cozy desk chaos
#   adhd_spiral              → energetic but bright & playful clutter
#   delusional_romantic      → dreamy warm tones, soft highlights
#   existentially_exhausted  → gentle, quiet, but still warm & lived-in
#   sunday_scaries           → warm late-night or warm-lamp lighting, never dark
#
# Still outputs photorealistic 1024x1024 JPEG images.

import os
import base64
import random
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------
# Mood → Warm Chaos Variations
# -------------------------------------------------

MOOD_STYLES = {
    "corporate_burnout": """
        Warm, cozy desk chaos. Soft golden light hitting paperwork, half-finished coffee,
        sticky notes, pens everywhere. Busy energy but comforting, not stressful.
        Vibrant warm neutrals. Nothing cold, dim, or bleak.
    """,
    "adhd_spiral": """
        Bright, lively clutter. Open books, scattered objects, colorful notes, headphones,
        half-zipped bags, keys tossed, sunlight streaks. Energetic but fun, not overwhelming.
        Warm tones only. Zero darkness.
    """,
    "delusional_romantic": """
        Dreamy warm aesthetic. Soft-focus golden lighting, flowers, open journal, cozy fabrics,
        sentimental clutter, little romantic touches. Whimsical, hopeful, warm.
        No gloom, no shadows.
    """,
    "existentially_exhausted": """
        Still warm, just quieter. Soft lamp glow on scattered blankets, open laptop,
        pillows, notes, coffee mug. Lived-in, gentle chaos — never empty, bleak, or dim.
        Golden, amber, or soft daylight only.
    """,
    "sunday_scaries": """
        Warm-lamp evening chaos. Couch or bed with cozy clutter—hoodie, snacks, journal,
        soft blanket, dim-but-warm ambient lighting. Slight anticipation energy but NEVER
        dark, cold, or heavy. Soft oranges + warm neutrals.
    """,
}

# -------------------------------------------------
# Image Generator
# -------------------------------------------------

def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating Joanie warm-chaos image ({mode}) for prompt: {prompt}")

    mood_style = MOOD_STYLES[mode]

    visual_prompt = f"""
    Create a cozy, warm, photorealistic snapshot of everyday life chaos.

    STYLE:
    - Warm tones ONLY: golden hour light, soft lamp glow, natural sunlight.
    - Zero darkness, zero heavy shadows, zero bleakness.
    - Cozy, relatable clutter: keys, notebooks, open bags, receipts, pens,
      coffee cups, sweaters, books, blankets, tech gadgets.
    - Scene should feel lived-in, human, warm, and emotionally safe.
    - No people visible.

    MOOD INFLUENCE:
    {mood_style}

    PROMPT INSPIRATION:
    - The mood should subtly echo: "{prompt}"
    - But DO NOT include text, quotes, posters, or writing on walls.
    - No Atty symbol in this version.

    OUTPUT REQUIREMENTS:
    - Photorealistic.
    - Square 1024x1024.
    - Soft highlights, warm gradients, cozy shadows (never dark).
    - High detail textures (fabric, paper, wood grain).
    - Respond ONLY with the generated image.
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

    print(f"✅ Generated warm-chaos image: {path}")
    return path
