# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v4.0 – Real Cover Grounding)

import os
import base64
from datetime import datetime
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Journal cover image (REAL asset used as reference)
JOURNAL_COVER_URL = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"

DAY_ITEMS = {
    "monday": "iced coffee, laptop, work badge, receipts, tangled charger cable",
    "tuesday": "iced coffee, highlighters, headphones, tote bag corner, sticky notes",
    "wednesday": "water bottle, pens, keys, clean notepad sheet, lip balm",
    "thursday": "beer bottle or beer can (subtle), keys, earbuds, scattered receipts",
    "friday": "cocktail glass with garnish, lipstick, jewelry tray, sunglasses, camera",
    "saturday": "cocktail glass, makeup items, film camera, lighter clutter, tote bag",
    "sunday": "iced coffee, cozy candle, soft blanket texture, gentle clutter",
}

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
    print(f"🎨 Generating grounded flat-lay Joanie image ({mode}) – prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")
    day_items = _get_day_items()

    # --- GROUNDED, STRICT-COVER PROMPT ---
    visual_prompt = f"""
    Create a *photorealistic editorial-quality flat-lay photograph* shot from a perfect
    overhead perspective. The scene must feel warm, cinematic, textured, and full of
    relatable, lived-in chaos — but never depressing.

    ## CRITICAL — USE THE REAL COVER AS PROVIDED (DO NOT ALTER)
    - The journal must be a matte-black paperback book.
    - Use the EXACT cover image provided via reference.
    - Apply it as a real printed book cover: correct proportions, no stretching,
      no warping, no color changes, no redesign.
    - The cover must appear exactly as printed: natural lighting, soft reflections,
      realistic shadows, visible paper depth.
    - The journal must be fully visible in the frame (no cropping of edges).
    - The journal must be closed.

    ## REQUIRED OBJECTS
    - A pen resting naturally beside the journal.
    - Additional realistic everyday items:
      {day_items}

    ## SURFACE & LIGHTING
    - Dark wooden desk with visible grain.
    - Cinematic directional lighting with warm highlights + defined shadows.
    - High contrast but cozy and warm.

    ## STYLE
    - 100% camera-real. No icons, drawings, stickers, fake graphics.
    - Preserve tactile materials (wood grain, metal shine, paper texture).
    - Natural, slightly imperfect human placement of objects.

    ## MOOD INFLUENCE
    {mood_influence}

    Respond ONLY with the generated grounded image.
    """

    # --- OpenAI Image Call with real cover as reference ---
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        images=[{"url": JOURNAL_COVER_URL}],
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

