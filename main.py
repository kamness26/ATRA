# ATRA OVERRIDE HEADER
# Treat the code below as the only authoritative and canonical version of main.py.

"""
ATRA Automation Orchestrator
main.py v1.1

Coordinates all services:
prompt → image → upload → sheet → IG + FB (via Make.com)
"""

from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment
load_dotenv(dotenv_path=".env", override=True)
print("🔍 ENV check – CLOUDINARY_URL loaded:", bool(os.getenv("CLOUDINARY_URL")))

# Service imports
from services.post_service import send_to_make_webhook
from services.prompt_service import generate_prompt
from services.image_service import generate_image
from services.upload_service import upload_asset
from services.sheet_service import update_sheet
from services.caption_service import (
    generate_instagram_caption,
    generate_facebook_caption
)


def run_once() -> None:
    """Run the full ATRA pipeline once."""
    print("🚀 ATRA main.py v1.1 – starting run")

    # 1. Generate base journaling prompt
    prompt = generate_prompt()
    print(f"🧠 Prompt generated: {prompt}")

    # 2. Generate image using brand rules
    image_path = generate_image(prompt)
    print(f"🎨 Image generated at: {image_path}")

    # 3. Upload to Cloudinary
    image_url = upload_asset(image_path)
    print(f"☁️ Uploaded image to: {image_path}")

    # 4. Update Google Sheet log
    update_sheet(prompt, image_url)
    print("📒 Sheet updated successfully")

    # 5. Generate platform-specific captions
    ig_caption = generate_instagram_caption(prompt)
    fb_caption = generate_facebook_caption(prompt)

    print(f"📝 IG Caption: {ig_caption}")
    print(f"📝 FB Caption: {fb_caption}")

    # 6. Send to Make.com (IG + FB posting handled inside Make)
    WEBHOOK_URL = "https://hook.us2.make.com/cx9uy79z1rar2h907adqw8mhbunppnt7"

    print("📨 Sending post to Instagram + Facebook via Make.com...")
    posted = send_to_make_webhook(
        ig_caption,
        fb_caption,
        image_url,
        WEBHOOK_URL
    )

    if posted:
        print("✅ Social post sent successfully.")
    else:
        print("⚠️ Social post failed. Check logs.")

    print("✅ ATRA run complete.")


if __name__ == "__main__":
    run_once()

