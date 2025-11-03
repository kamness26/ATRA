# 🚨 ATRA OVERRIDE HEADER 🚨
# Canonical ATRA Image Generation Module v1.1
# Handles Base64 image data returned by OpenAI and saves it locally.

import base64
import os
from openai import OpenAI
from atra.config import OPENAI_API_KEY
from atra.utils import log, divider

client = OpenAI(api_key=OPENAI_API_KEY)

OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "generated_image.png")

def generate_image(prompt_text: str):
    """
    Generates an image from a given prompt string using DALL·E 3.
    Decodes Base64 data and saves it locally.
    Returns the path to the saved image.
    """
    divider("ATRA – Generating Image")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt_text,
            size="1024x1024"
        )

        # Handle Base64 image data
        image_b64 = response.data[0].b64_json
        image_data = base64.b64decode(image_b64)

        with open(OUTPUT_PATH, "wb") as f:
            f.write(image_data)

        log(f"🎨 Image generated and saved at: {OUTPUT_PATH}")
        return OUTPUT_PATH

    except Exception as e:
        log(f"❌ Error generating image: {e}")
        return None

if __name__ == "__main__":
    test_prompt = "A surreal desk scene where chaos meets creativity."
    generate_image(test_prompt)
