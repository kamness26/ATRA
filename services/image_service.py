# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v3.2)
#
# Major update:
# - Journal is ALWAYS CLOSED
# - MUST display the exact real cover shown here:
#   https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg
# - Model must SHOW this cover, not reinterpret or redesign it.
# - No substitutions like “The Five-Minute Journal.”
#
# Style: warm, cinematic flat-lay, lived-in chaos, not depressing.
# Output: 1024×1024 baseline sRGB JPEG (Instagram-safe).

import os
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------
# Joanie mood cues → influences surrounding props
# ---------------------------------------
MOOD_OBJECTS = {
    "corporate_burnout": """
        Include items like: work badge, cold coffee, receipts, dead highlighter,
        laptop corner, minimal jewelry. Lighting: warm desk glow.
    """,

    "adhd_spiral": """
        Include: tangled earbuds, multiple pens, scattered notes, keys drifting
        out of frame, lipstick askew. Lighting: energetic but warm.
    """,

    "delusional_romantic": """
        Include: soft lipstick, a tiny flower, romantic doodles,
        warm drink, gentle clutter. Lighting: dreamy warm highlights.
    """,

    "existentially_exhausted": """
        Include: water bottle, minimal clutter, clean pen,
        a single sticky note. Lighting: balanced, cinematic, NOT gloomy.
    """,

    "sunday_scaries": """
        Include: iced coffee, crumpled receipts, keys, tote bag corner,
        subtle work reminders. Lighting: warm directional, slight vignette.
    """,
}


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating flat-lay Joanie image ({mode}) for prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")

    # 🔒 LOCK IN THE REAL COVER — NO REINTERPRETATION
    real_cover_url = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"

    visual_prompt = f"""
    Create a photorealistic editorial flat-lay photograph shot from a perfect
    overhead perspective. Warm, cinematic, lived-in chaos — but never sad.

    THE JOURNAL (MANDATORY):
    - The journal must be CLOSED.
    - It must display THIS EXACT REAL COVER:
      {real_cover_url}
    - The model should reproduce the cover faithfully as if photographed.
    - Do NOT redesign, reinterpret, simplify, or replace it.
    - Absolutely forbid other journals (e.g., "The Five-Minute Journal").
      Only the real *You Won’t Believe This $H!T* cover is allowed.

    REQUIRED OBJECTS:
    - The closed journal centered in the scene.
    - A pen nearby.
    - Dark wooden desk surface.
    - Cinematic directional lighting with warm, defined shadows.

    SURROUNDING CHAOS (varies by Joanie mode):
    {mood_influence}

    ADDITIONAL RULES:
    - No posters, no illustrations, no graphic design.
    - 100% real-world camera realism.
    - Earthy muted tones only.
    - Drinks appear depending on the day-of-week logic (handled upstream).
    - The drink should appear naturally in the clutter, not as a focal point.

    Technical:
    - Produce a final 1024×1024 photorealistic image.
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
    pil_image = Image.open(BytesIO(image_bytes))

    # IG compatibility: enforce baseline RGB JPEG
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
