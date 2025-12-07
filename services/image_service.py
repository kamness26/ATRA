# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v3.2)
#
# Updates:
# - Journal is ALWAYS CLOSED
# - Journal MUST show official cover: https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg
# - Day-specific objects added (beer Thu, cocktails Fri/Sat)
# - Drinks appear as background chaos, NOT as a hero element
# - Same photorealistic flat-lay cinematic style preserved

import os
import base64
from datetime import datetime
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------------------
# DAY-SPECIFIC CHAOS ITEMS
# -------------------------------------------------------------
DAY_ITEMS = {
    "Monday": "a stressed work badge, scattered sticky notes, an overworked pen",
    "Tuesday": "a laptop corner, iced coffee, tangled earbuds",
    "Wednesday": "multiple pens, receipts, a half-open makeup bag",
    "Thursday": "a casual beer bottle or can placed subtly in the layout",
    "Friday": "a cocktail glass or shaker, slightly festive but not dominant",
    "Saturday": "a weekend cocktail or spritz, relaxed energy, not a hero item",
    "Sunday": "no alcohol — instead use iced coffee, a tote bag, resting keys",
}

# -------------------------------------------------------------
# Joanie mood cues → influences subtle object and lighting decisions
# -------------------------------------------------------------
MOOD_OBJECTS = {
    "corporate_burnout": """
        Add: laptop corner, dead highlighter, cold coffee, work badge,
        half-used sticky notes, receipts, simple jewelry.
        Lighting: warm desk lamp energy — never cold or sad.
    """,

    "adhd_spiral": """
        Add: tangled earbuds, scattered pens, half-open lipstick,
        multiple sticky notes, keys slightly off-frame.
        Lighting: lively, bright pockets without harsh contrast.
    """,

    "delusional_romantic": """
        Add: soft lipstick, a tiny flower, heart doodle, warm coffee.
        Lighting: warm, dreamy highlights with crisp focus.
    """,

    "existentially_exhausted": """
        Add: water bottle, clean pen, minimal clutter, calm sticky notes.
        Lighting: balanced cinematic, slightly cool but not depressing.
    """,

    "sunday_scaries": """
        Add: iced coffee, crumpled receipts, keys, tote bag corner.
        Lighting: warm directional, subtle vignette, never dark.
    """,
}

# -------------------------------------------------------------
# IMAGE GENERATION
# -------------------------------------------------------------
def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating Joanie flat-lay image ({mode}) for prompt: {prompt}")

    today = datetime.now().strftime("%A")
    day_items = DAY_ITEMS.get(today, "")
    mood_items = MOOD_OBJECTS.get(mode, "")

    visual_prompt = f"""
    Create a 100% photorealistic editorial flat-lay photograph shot from a perfect overhead
    angle. The image should feel warm, cinematic, high-contrast, and full of relatable,
    lived-in chaos — but NEVER depressing.

    REQUIRED VISUAL RULES:
    - The CLOSED journal must be centered as the main character.
    - The journal MUST show THIS EXACT COVER (no reinterpretation):
      https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg
    - A pen should rest naturally near the journal.
    - Objects arranged like real daily chaos: keys, earbuds, lipstick, receipts,
      sticky notes, iced coffee, water bottle, tote bag, makeup items, etc.
    - Use a dark wooden desk surface with rich texture.
    - Use warm, cinematic directional lighting with natural shadows.

    DAY-SPECIFIC OBJECTS TO INCLUDE:
    {day_items}

    MOOD-BASED OBJECTS TO SUBTLY INCLUDE:
    {mood_items}

    DRINKS RULE:
    - If Thursday → include a casual beer bottle/can in the chaos.
    - If Friday or Saturday → include a cocktail, spritz, or shaker.
    - Drinks must NEVER be the central or dominant element — they blend into the scene.

    STYLE:
    - Editorial magazine quality.
    - Earth tones: deep browns, blacks, tans, olives.
    - Textures must be sharp and realistic.
    - No illustrations, no graphics, no Atty, no poster elements.
    - Only real-world objects photographed realistically.

    Technical:
    - Output a cohesive 1024×1024 photorealistic image.
    - Respond ONLY with an image.
    """

    # --- OpenAI Image Call ---
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        n=1,
        size="1024x1024"
    )

    # Decode → PIL
    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Output path
    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"

    # Instagram-safe baseline JPEG
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
