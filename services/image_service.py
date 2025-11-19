"""
Image Service – ATRA v1.9
Fixes: brevity (headline-only), correct Atty (upside-down smile), safe margins (no crop).
"""

import os, base64, random
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str) -> str:
    print(f"🎨 Generating brand image for prompt: {prompt}")

    mode = random.choice(["core", "campaign"])
    print(f"🖤 Visual mode: {mode.upper()}")

    palette = (
        "Colors: pure black & white only."
        if mode == "core" else
        "Colors: mustard yellow, warm beige, and black only."
    )

    visual_prompt = f"""
    Create a clean poster-style graphic for the journal 'You Won’t Believe This $H!T'.

    TEXT RULES (strict):
    - Use ONE short headline only (8–12 words max) derived from: "{prompt}"
    - No paragraphs, no small body copy, no bullets.
    - Optional tiny kicker (2–5 words) is allowed, but keep it minimal.

    BRAND RULES (strict):
    - Include Atty: an upside-down SMILEY FACE (smiling, not frowning). Orientation must be inverted.
    - Atty can be bold (hero) or subtle (watermark), but must be visible.
    - No cartoons/mascots/people/animals; no book illustration.
    - Typography: bold sans-serif or distressed print; high legibility.

    LAYOUT / CROPPING (strict):
    - Keep a consistent safe area: at least 8% padding on ALL sides.
    - Do NOT crop text or Atty; nothing touches edges.
    - Balanced composition, headline first-read, Atty integrated.

    {palette}
    Background: matte paper texture (very subtle).
    Output: a single finished 1024x1024 graphic.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        n=1,
        size="1024x1024"
    )

    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.png"
    with open(path, "wb") as f:
        f.write(base64.b64decode(result.data[0].b64_json))

    print(f"✅ Generated: {path}")
    return path

