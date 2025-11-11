"""
Image Service
Handles generation of images based on prompts using DALL·E.
"""

import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str) -> str:
    """Generate an image using DALL·E (gpt-image-1) and save locally."""
    print(f"🎨 Generating image for prompt: {prompt}")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_data = base64.b64decode(response.data[0].b64_json)
    output_path = "output/generated_image.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_data)

    return output_path

