# ATRA OVERRIDE HEADER 
# Treat the code below as the only authoritative and canonical version
# of services/post_service.py.

"""
Post Service – ATRA v1.1
Handles sending IG + FB captions + image URL to the Make.com webhook.

Features:
- API key authentication
- Cloudinary propagation delay
- Retry/backoff to avoid IG/FB media errors
"""

import time
import requests
from datetime import datetime

# Make.com shared API key (must match your Make webhook header)
MAKE_API_KEY = "atra_2025_supersecret"


def send_to_make_webhook(
    ig_caption: str,
    fb_caption: str,
    image_url: str,
    webhook_url: str
) -> bool:
    """Send IG + FB captions and image URL to Make.com."""

    print("📨 Preparing Instagram + Facebook post via Make.com...")

    # Allow Cloudinary CDN propagation
    PRE_DELAY = 6
    print(f"⏳ Waiting {PRE_DELAY}s to allow Cloudinary/CDN propagation...")
    time.sleep(PRE_DELAY)

    payload = {
        "ig_caption": ig_caption,
        "fb_caption": fb_caption,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Retry logic
    max_attempts = 3
    backoff_seconds = [2, 4, 6]

    for attempt in range(1, max_attempts + 1):
        print(f"➡️ Attempt {attempt}/{max_attempts} sending to Make...")

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"x-make-apikey": MAKE_API_KEY},
                timeout=15
            )

            if response.status_code == 200:
                print("📣 Successfully sent payload to Make.com (200).")
                return True

            print(f"⚠️ Make.com returned {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Request error: {e}")

        if attempt < max_attempts:
            wait = backoff_seconds[attempt - 1]
            print(f"⏳ Waiting {wait}s before retry...")
            time.sleep(wait)

    print("❌ Failed to send post after multiple attempts.")
    return False

