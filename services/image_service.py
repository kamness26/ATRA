
"""
Image Service – ATRA v1.9 (Joanie Edition)
Fixes: Switch from poster-style to Joanie’s flash-photo aesthetic, PNG → JPEG conversion.
"""

import os
import base64
import random
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str) -> str:
    print(f"🎨 Generating brand image for prompt: {prompt}")

    mode = random.choice(["core", "campaign"])
    print(f"🖤 Visual mode: {mode.upper()}")

    # Joanie's palette still varies by mode
    palette = (
        "Color mood: harsh black & white with high contrast flash."
        if mode == "core" else
        "Color mood: muted beige, mustard yellow accents, strong flash aesthetic."
    )

    # === NEW JOANIE VISUAL PROMPT ===
    visual_prompt = f"""
    Create a chaotic, flash-photography Gen Z/Millennial image inspired by “Joanie” —
    a functional-chaotic corporate girlie who survives on iced coffee, overthinking,
    ADHD brain dumps, romantic delusion, and funny self-awareness.

    AESTHETIC (strict):
    - Hard flash photography in low-light (phone-flash energy).
    - Realistic, candid, messy, unpolished.
    - High contrast, strong shadows, sharp flash reflections.
    - Must feel like a “life spill”: Joanie dumped her tote bag and this is the scene.

    PROPS (allowed, choose any):
    - Iced coffee cup, messy receipts, AirPods/headphones tangled,
      lip gloss, subway card, a pen, corporate keycard, sticky notes,
      hydro flask, mascara, tote bag, half-finished martini,
      scribbled notebook doodles.

    JOURNAL INTEGRATION (strict):
    Include ONE visible journal page or prompt from the set below:
    - “My ADHD Is the Captain Now!”
    - “My Flags Identify As GREEN”
    - “Doodle Time!”
    - “Delusion: Not Just A River In Egypt”
    - “Treat Every Room Like An Escape Room”
    - “Mercury Was Far From Retro-GREAT”
    Do NOT show more than one page. Keep it candid, not graphic-designed.

    TONE:
    - Organized chaos meets feminine unhinged energy.
    - Should feel humorous, self-aware, and accidentally aesthetic.
    - Real-world, physical objects — no illustrations, no poster layouts.

    WHAT TO AVOID:
    - Poster-style graphics.
    - Perfectly neat or centered compositions.
    - Inspirational typography.
    - Cartoon characters, emoji faces, mascots.
    - Clean corporate minimalism.
    - Anything too polished.

    {palette}
    Output: a single finished 1024x1024 flash-photographic image.
    """

    # Call OpenAI image generation
    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        n=1,
        size="1024x1024"
    )

    # Extract base64 → bytes
    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    # Bytes → PIL Image → RGB for IG compatibility
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Save as JPEG (IG safe)
    path = "output/generated_image.jpg"
    pil_image.save(path, format="JPEG", quality=92)

    print(f"✅ Generated: {path}")
    return path
