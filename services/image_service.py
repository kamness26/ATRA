# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v3.3 – Real Cover Version)

import os
import base64
from datetime import datetime
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Journal cover URL
JOURNAL_COVER_URL = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"

# Day-of-week item variations
DAY_ITEMS = {
    "monday": "iced coffee, laptop, work badge, receipts, tangled charger cable",
    "tuesday": "iced coffee, highlighters, headphones, tote bag corner, sticky notes",
    "wednesday": "water bottle, pens, keys, clean notepad sheet, lip balm",
    "thursday": "beer bottle or beer can (subtle), keys, earbuds, scattered receipts",
    "friday": "cocktail glass with garnish, lipstick, jewelry tray, sunglasses, camera",
    "saturday": "cocktail glass, makeup items, film camera, lighter clutter, tote bag",
    "sunday": "iced coffee, cozy candle, soft blanket texture, gentle clutter",
}

# Mood → object/lens cues
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
    day = datetime.now().strftime("%A").lower()
    return DAY_ITEMS.get(day, DAY_ITEMS["monday"])


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating flat-lay Joanie image ({mode}) – prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")
    day_items = _get_day_items()

    visual_prompt = f"""
    Create a *photorealistic editorial-quality flat-lay photograph* shot from a perfect
    overhead perspective. The scene must feel warm, cinematic, textured, and full of
    relatable, lived-in chaos — but never depressing.

    THE JOURNAL (CRITICAL REQUIREMENT):
    - The journal MUST be closed.
    - It MUST display THIS EXACT REAL COVER as a physical object:
      {JOURNAL_COVER_URL}
    - Render the cover as a real printed book with natural lighting, shadows,
      texture, reflections, and paper depth. Not a sticker, not a graphic overlay.
    - The journal should sit naturally in the center of the composition.

    REQUIRED SURROUNDING OBJECTS:
    - A pen resting naturally beside the journal.
    - Additional realistic everyday objects arranged as if recently used:
      {day_items}

    SURFACE & LIGHTING:
    - Dark wooden desk with rich visible grain.
    - Cinematic directional lighting with warm highlights and defined shadows.
    - High contrast but warm temperature — cozy, not bleak.

    STYLE:
    - 100% camera-real image. No illustrations, icons, or digital graphics.
    - Editorial magazine aesthetic.
    - Depth and texture preserved (wood grain, metal reflections, paper fibers).
    - Vary object placement daily, keep natural human chaos.

    MOOD-BASED INFLUENCE:
    {mood_influence}

    IMAGE SPECS:
    - 1024 × 1024 resolution
    - Photorealistic
    - Instagram-safe baseline sRGB JPEG

    Respond ONLY with the generated image.
    """

    # --- OpenAI Image Call ---
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        n=1,
        size="1024x1024"
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes))

    pil_image = pil_image.convert("RGB")

    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"

    pil_image.save(
        path,
        format="JPEG",
        quality=90,
        subsampling=0,
        optimize=True,
        progressive=False
    )

    print(f"✅ Image generated at: {path}")
    return path
