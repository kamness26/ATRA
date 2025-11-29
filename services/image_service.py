# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat this file as the ONLY canonical version of services/image_service.py.
#
# Image Service – ATRA (Joanie Photoreal Edition v3.0)
#
# PURPOSE:
#   Generate photorealistic Joanie-centered images that reflect her mood modes.
#   These are cinematic, lifestyle, photojournalistic, emotionally grounded images.
#
# RULES:
#   - NO posters
#   - NO headlines
#   - NO graphic design elements
#   - NO Atty
#   - NO text on the image
#   - NO illustrations, cartoons, or character drawings
#   - MUST be photorealistic and cinematic, 1024x1024
#
# Joanie is never shown as a face-forward portrait.
# She is represented through:
#   - environments
#   - objects
#   - hands
#   - over-the-shoulder shots
#   - POV shots
#   - silhouettes
#   - emotional spaces that imply her presence
#
# Mood → Photoreal direction


import os
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


MOOD_TO_PHOTOREAL_STYLE = {
    "corporate_burnout": """
        A lonely desk at night, cold office lighting,
        half-drunk coffee, laptop glow, shadows of paperwork,
        muted colors, slight blue cast, exhaustion in the air.
        Cinematic, moody, shallow depth of field.
    """,

    "adhd_spiral": """
        Chaotic desk energy: scattered notes, open tabs on screens,
        colorful pens, half-finished snacks, motion blur hints,
        vibrant micro-details, tactile close-up textures.
        Energetic but still aesthetically composed.
    """,

    "delusional_romantic": """
        Warm cinematic lighting, soft bokeh, a cozy bed or couch,
        journal open next to candles or soft fairy lights,
        dreamy golden undertones, hints of longing in the space.
        Slight haze or film softness.
    """,

    "existentially_exhausted": """
        Empty room, cool lighting, soft gray palette,
        a journal sitting open on a table with nothing written,
        wide negative space, slightly desaturated,
        atmospheric loneliness. Quiet, still, cinematic.
    """,

    "sunday_scaries": """
        Dim early-evening apartment scene, unwashed mug,
        cozy-yet-anxious Sunday atmosphere, TV glow, socks on couch,
        slightly darker shadows, warm-to-cool mixed lighting.
        Subtle tension without chaos.
    """,
}


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating photoreal Joanie image for mode={mode}")

    photoreal_style = MOOD_TO_PHOTOREAL_STYLE[mode]

    visual_prompt = f"""
    Create a **photorealistic cinematic 1024x1024 image**.

    NOT ALLOWED:
    - No posters
    - No text
    - No Atty
    - No illustrations, drawings, cartoons, or clip art
    - No people shown fully or face-forward
    - No visible characters looking at camera

    ALLOWED:
    - Over-the-shoulder shots
    - POV shots
    - Silhouettes
    - Hands
    - Environments that imply Joanie’s presence
    - Everyday emotional objects

    STYLE REQUIREMENTS:
    - Cinematic lighting
    - Real camera depth of field
    - Realistic textures
    - Filmic color grading
    - Rich shadows and highlights
    - Photojournalistic or lifestyle feel

    MOOD SPECIFIC:
    {photoreal_style}

    PROMPT INFLUENCE:
    The scene should subtly reflect this journaling theme:
    "{prompt}"

    Deliver ONLY a finished image.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        size="1024x1024",
        n=1
    )

    # Decode base64 → image
    image_b64 = result.data[0].b64_json
    img_bytes = base64.b64decode(image_b64)
    pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")

    # Save output
    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"
    pil_img.save(path, format="JPEG", quality=92)

    print(f"✅ Generated photoreal image: {path}")
    return path
