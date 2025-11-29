# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the ONLY authoritative and canonical version of this file.
#
# Image Service – ATRA (Joanie Edition v3.0 – Cinematic Photorealism)
#
# NEW RULES (Dec 2025):
# - NO Atty
# - NO posters, NO typographic layouts
# - NO padding rules
# - NO graphic-design constraints
# - CINEMATIC PHOTO-REAL IMAGERY ONLY
# - Emotive, atmospheric, relatable, scroll-stopping
#
# Joanie visual themes (per mode):
# - corporate_burnout          → cold office light, fatigue realism
# - adhd_spiral                → colorful clutter, motion/energy
# - delusional_romantic        → warm dreamy haze, emotional softness
# - existentially_exhausted    → dim, cool, introspective isolation
# - sunday_scaries             → nighttime quiet anxiety, warm lamp glow
#
# Each image:
# - Photo-realistic (not illustration)
# - Cinematic lighting, shallow depth-of-field, A24 vibe
# - Joanie may appear fully, partially, or implied through framing
# - Never identical, always same archetype
# - 1024x1024 JPG output for IG compatibility

import os
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cinematic mode styles
JOANIE_MODES = {
    "corporate_burnout": """
        Cinematic photorealism. Cold office lighting. Soft blue-grey palette.
        Tired eyes, slumped posture, emotional realism.
        Subtle computer monitor glow, messy desk, shallow depth-of-field.
    """,
    "adhd_spiral": """
        Photorealistic lifestyle chaos. Colorful clutter, motion blur,
        lived-in apartment, intense natural window light.
        Slight surreal bloom around highlights. Emotional energy, realism.
    """,
    "delusional_romantic": """
        Warm cinematic golden-hour lighting. Soft haze, dreamy bloom,
        wistful expression, elegant close-ups.
        Romantic tones with emotional intimacy. A24-like visual softness.
    """,
    "existentially_exhausted": """
        Dim room. Cool, shadow-heavy palette. Moody introspective lighting.
        Emotional weight, quiet isolation, heavy negative space.
        Photorealistic realism with soft vignette.
    """,
    "sunday_scaries": """
        Nighttime interior. Warm lamp against cool ambient darkness.
        Emotional tension, quiet loneliness, gentle highlights.
        Realistic textures, cinematic close framing.
    """,
}

# Core Joanie archetype (flexible but recognizable)
JOANIE_ARCHETYPE = """
Young woman (mid-20s to early-30s), expressive face, messy hair, tired beauty,
realistic skin texture, soft features, modern clothing, emotionally present.
"""


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating cinematic Joanie image ({mode})")

    style_block = JOANIE_MODES.get(mode, JOANIE_MODES["existentially_exhausted"])

    full_prompt = f"""
    Create a cinematic, photo-realistic image inspired by this journaling prompt:

        "{prompt}"

    Requirements:
    - Use the Joanie archetype: {JOANIE_ARCHETYPE}
    - Emphasize the emotional tone of: {style_block}
    - NO text. NO typography. NO graphic elements. NO icons. NO posters.
    - Natural real-world setting (apartment, street, coffee shop, office, etc.)
    - A24-style film lighting and composition.
    - Soft bloom, shallow depth-of-field, emotional realism.
    - Color palette guided by the mode.
    - IG-friendly, scroll-stopping, authentic, human.
    - 1024x1024 output, photo-real.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=full_prompt.strip(),
        size="1024x1024"
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    pil_img = Image.open(BytesIO(image_bytes)).convert("RGB")

    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"output/joanie_cinematic_{mode}_{timestamp}.jpg"

    pil_img.save(path, format="JPEG", quality=92)

    print(f"✅ Saved cinematic Joanie image: {path}")
    return path
