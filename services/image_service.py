# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v4.1 – Real Cover Grounding Fix)

import os
import base64
from datetime import datetime
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ JOURNAL COVER IMAGE (Provide exact final Cloudinary URL here)
JOURNAL_COVER_URL = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"

# Day-of-week clutter items
DAY_ITEMS = {
    "monday": "iced coffee, laptop, work badge, receipts, tangled charger cable",
    "tuesday": "iced coffee, highlighters, headphones, tote bag corner, sticky notes",
    "wednesday": "water bottle, pens, keys, clean notepad sheet, lip balm",
    "thursday": "beer bottle or beer can (subtle), keys, earbuds, scattered receipts",
    "friday": "cocktail glass with garnish, lipstick, jewelry tray, sunglasses, camera",
    "saturday": "cocktail glass, makeup items, film camera, lighter clutter, tote bag",
    "sunday": "iced coffee, cozy candle, soft blanket texture, gentle clutter",
}

# Mood-driven visual cues
MOOD_OBJECTS = {
    "corporate_burnout": """
        Items: laptop corner, dried highlighter, work badge, cold coffee,
        half-used sticky notes. Lighting: warm desk-lamp cinematic glow.
    """,
    "adhd_spiral": """
        Items: tangled earbuds, scattered pens, lipstick half open,
        slightly chaotic key placement. Lighting: energetic but warm.
    """,
    "delusional_romantic": """
        Items: soft lipstick, flower petal, warm coffee, heart doodle.
        Lighting: dreamy warm highlights.
    """,
    "existentially_exhausted": """
        Items: water bottle, minimal clutter, clean pen, blank note.
        Lighting: soft cool-but-warm-balanced cinematics.
    """,
    "sunday_scaries": """
        Items: iced coffee, crumpled receipt, keys, tote bag corner.
        Lighting: warm side lighting, slight vignette.
    """
}


def _get_day_items() -> str:
    """Returns clutter items based on day of week."""
    day = datetime.now().strftime("%A").lower()
    return DAY_ITEMS.get(day, DAY_ITEMS["monday"])


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating grounded flat-lay Joanie image ({mode}) – prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")
    day_items = _get_day_items()

    # ------------------------------------------------------------
    # PHOTOREALISTIC FLAT-LAY + REAL COVER GROUNDING PROMPT
    # ------------------------------------------------------------
    visual_prompt = f"""
    Create a *photorealistic editorial-quality flat-lay photograph* shot from a perfect
    overhead perspective. The scene must feel warm, cinematic, textured, and full of
    relatable, lived-in chaos — but never depressing.

    ## CRITICAL — USE THE REAL COVER EXACTLY AS PROVIDED
    - The journal must be a matte-black paperback book.
    - Use the EXACT provided cover image as the book's printed front cover.
    - Do NOT modify, redesign, recolor, warp, or reinterpret the cover.
    - The printed cover must appear physically real with shadows, texture, and paper depth.
    - The journal must be fully visible in the frame (no cropping).
    - The journal must be closed and centered naturally.

    ## REQUIRED OBJECTS
    - A pen placed naturally beside the journal.
    - Additional everyday objects creating natural human clutter:
      {day_items}

    ## SURFACE & LIGHTING
    - Dark wooden desk with rich visible grain.
    - Cinematic directional lighting with warm highlights and defined shadows.
    - Warm, editorial-quality contrast.

    ## STYLE
    - 100% camera-real. Absolutely no illustrated or digital UI elements.
    - Maintain tactile materials: wood grain, metal reflections, paper texture.

    ## MOOD INFLUENCE
    {mood_influence}

    Respond ONLY with the generated grounded image.
    """

    # ------------------------------------------------------------
    # OpenAI Image Generation (Correct Parameter: image=[...])
    # ------------------------------------------------------------
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        image=[{"url": JOURNAL_COVER_URL}],  # ← FIXED (singular key)
        size="1024x1024",
        n=1,
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"

    pil_image.save(
        path,
        format="JPEG",
        quality=90,
        subsampling=0,
        optimize=True,
    )

    print(f"✅ Grounded image generated at: {path}")
    return path
