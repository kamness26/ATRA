# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v3.0)
#
# New direction:
# - No posters, no graphics, no Atty
# - 100% photorealistic editorial flat-lay photography
# - Warm, cinematic, directional lighting (not depressing)
# - Moody but cozy, relatable, lived-in chaos
# - Journal is ALWAYS present (open or closed)
# - Objects arranged like a real busy life: work badge, pen, lipstick, iced coffee,
#   keys, headphones, sticky notes, receipts, tote bag, water bottle, laptop corner, etc.
# - Joanie’s “modes” appear subtly through the chaos, NOT through darkness.
#
# Output: 1024×1024 JPEG, photorealistic overhead shot.

import os
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------
# Joanie mood cues → influences object choices & lighting
# ---------------------------------------
MOOD_OBJECTS = {
    "corporate_burnout": """
        Include items like: laptop corner, dead highlighter, cold coffee,
        work badge, half-used sticky notes, receipts, simple jewelry.
        Lighting: warm desk-lamp glow, not harsh, not sad.
    """,

    "adhd_spiral": """
        Include items like: tangled earbuds, scattered pens,
        half-open lipstick, multiple notes, keys slightly out of frame.
        Lighting: energetic pockets of brightness without chaos in shadows.
    """,

    "delusional_romantic": """
        Include items like: soft lipstick, a small flower, heart doodle,
        warm coffee, gentle note scribbles.
        Lighting: warm, dreamy highlights without softness in focus.
    """,

    "existentially_exhausted": """
        Include items like: water bottle, minimal clutter, clean pen,
        simple sticky note or blank page.
        Lighting: cooler but still warm enough to avoid sadness — balanced cinematic.
    """,

    "sunday_scaries": """
        Include items like: iced coffee, crumpled receipt, keys,
        tote bag corner, work badge peeking out.
        Lighting: warm directional light, slight vignette, NOT dark.
    """,
}


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating flat-lay Joanie image ({mode}) for prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")

    visual_prompt = f"""
    Create a photorealistic editorial flat-lay photograph shot from a perfect
    overhead perspective. The scene should feel warm, cinematic, and full
    of relatable, lived-in chaos — but NEVER depressing.

    REQUIRED ELEMENTS:
    - A journal at the center (open with handwriting inspired by: "{prompt}"
      OR closed showing a textured cover).
    - A pen resting naturally near or across the journal.
    - Everyday items arranged like they were just used:
      keys, earbuds, lipstick, sticky notes, receipts, iced coffee,
      water bottle, tote bag, laptop corner, camera, etc.
    - Dark wooden desk surface with rich grain and subtle texture.
    - Cinematic directional lighting casting defined but warm shadows.

    COLOR PALETTE:
    - Muted earth tones: deep browns, blacks, tan, olive, beige.
    - Metallic pen elements allowed.
    - Absolutely no neon or harsh color pops.

    STYLE:
    - High-contrast but warm.
    - Editorial magazine aesthetic.
    - Chaotic in a human, funny, relatable way — not sad.
    - No illustrations, no poster graphics, no drawn elements.
    - 100% real-world camera realism.
    - Depth preserved through shadows and object texture.

    MOOD INFLUENCE BASED ON JOANIE MODE:
    {mood_influence}

    Technical:
    - Output a finished, cohesive 1024×1024 photorealistic image.
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

    # Save
    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"
    pil_image.save(path, format="JPEG", quality=92)

    print(f"✅ Image generated at: {path}")
    return path
