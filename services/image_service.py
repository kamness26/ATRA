# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v4.2 – Compatibility Fix)

import base64
import os
from datetime import datetime
from io import BytesIO

import requests
from openai import OpenAI
from PIL import Image

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Exact Cloudinary cover asset
JOURNAL_COVER_URL = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"
COVER_CACHE_PATH = "output/_journal_cover_cache.jpg"

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


def _load_cover_asset() -> Image.Image:
    """
    Retrieve the canonical journal cover image from Cloudinary.
    Cached locally to avoid repeated downloads.
    """
    try:
        os.makedirs("output", exist_ok=True)

        if os.path.isfile(COVER_CACHE_PATH):
            return Image.open(COVER_CACHE_PATH).convert("RGBA")

        response = requests.get(JOURNAL_COVER_URL, timeout=20)
        response.raise_for_status()
        cover_image = Image.open(BytesIO(response.content)).convert("RGBA")
        cover_image.save(COVER_CACHE_PATH)
        return cover_image
    except Exception as exc:
        raise RuntimeError(f"Failed to load canonical journal cover: {exc}") from exc


def _place_cover_on_image(base: Image.Image, cover: Image.Image) -> Image.Image:
    """
    Paste the canonical cover onto the generated flat-lay to guarantee
    the correct journal appears in the final post.
    """
    base_rgba = base.convert("RGBA")

    # Scale cover to a consistent footprint within the frame
    target_width = int(base_rgba.width * 0.55)
    aspect_ratio = cover.height / cover.width
    target_height = int(target_width * aspect_ratio)
    cover_resized = cover.resize((target_width, target_height), Image.LANCZOS)

    x = (base_rgba.width - target_width) // 2
    y = (base_rgba.height - target_height) // 2

    base_rgba.paste(cover_resized, (x, y), cover_resized)
    return base_rgba.convert("RGB")


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating grounded flat-lay Joanie image ({mode}) – prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")
    day_items = _get_day_items()

    # ----------------------------------------------------------
    # PROMPT-BASED GROUNDING (since reference-image parameter is unsupported)
    # ----------------------------------------------------------
    visual_prompt = f"""
    Create a *photorealistic editorial-quality flat-lay photograph* shot perfectly from above.
    Warm, cinematic, textured, lived-in chaos — but not depressing.

    ## USE THIS EXACT REAL JOURNAL COVER (DO NOT MODIFY)
    - The cover appears at this URL: {JOURNAL_COVER_URL}
    - Reproduce it *exactly* as printed: same colors, text, layout, proportions.
    - Do NOT alter or reinterpret anything. This is the canonical asset.
    - Render as a physical matte-black paperback book with the cover perfectly centered.
    - Full cover visible in the frame, no cropping or objects on top.
    - Natural shadows, reflections, and paper thickness visible.

    ## REQUIRED OBJECTS
    - A pen beside the journal.
    - Everyday clutter items for the day of week:
      {day_items}

    ## SURFACE & LIGHTING
    - Dark wood desk with visible grain.
    - Cinematic directional warm lighting, defined shadows.

    ## STYLE
    - 100% camera-real. No illustrations, digital UI, or stickers.
    - Preserve wood grain, metal shine, paper texture.

    ## MOOD INFLUENCE
    {mood_influence}

    Respond ONLY with the generated image.
    """

    # ----------------------------------------------------------
    # Image generation (NO image= parameter — fully compatible)
    # ----------------------------------------------------------
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        size="1024x1024",
        n=1,
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    cover_image = _load_cover_asset()
    print("📚 Overlaying canonical journal cover onto generated frame.")
    pil_image = _place_cover_on_image(pil_image, cover_image)

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
