
"""
ATRA Automation Orchestrator
main.py v1.0

Coordinates all services: prompt → image → upload → sheet
"""

from dotenv import load_dotenv
import os

# Force-load the real .env file before importing anything else
load_dotenv(dotenv_path=".env", override=True)
print("🔍 ENV check – CLOUDINARY_URL loaded:", bool(os.getenv("CLOUDINARY_URL")))

from datetime import datetime
from services.prompt_service import generate_prompt
from services.image_service import generate_image
from services.upload_service import upload_asset
from services.sheet_service import update_sheet


def run_once() -> None:
    """Run the full ATRA pipeline once."""
    print("🚀 ATRA main.py v1.0 – starting run")
    started_at = datetime.utcnow().isoformat()

    prompt = generate_prompt()
    print(f"🧠 Prompt generated: {prompt}")

    image_path = generate_image(prompt)
    print(f"🎨 Image generated at: {image_path}")

    image_url = upload_asset(image_path)
    print(f"☁️ Uploaded image to: {image_url}")

    update_sheet(prompt, image_url)
    print(f"📒 Sheet updated successfully at {started_at}")
    print("✅ ATRA run complete.")


if __name__ == "__main__":
    run_once()

