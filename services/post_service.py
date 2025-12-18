# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version
# of services/post_service.py.

"""
Post Service – ATRA v2.0
Supports:
- Images (default)
- Videos (Sora integration)
- API key authentication
- Cloudinary propagation delay
- Retry/backoff
"""

import time
import requests
from datetime import datetime

# Make.com shared API key (must match your Make webhook header)
MAKE_API_KEY = "atra_2025_supersecret"


def send_to_make_webhook(
    ig_caption: str,
    fb_caption: str,
    media_url: str,
    media_type: str,
    webhook_url: str
) -> bool:
    """
    Sends payload to Make.com.

    media_type:
        "image" → IG photo, FB photo
        "video" → TikTok video + optional IG/FB video if configured
    """

    print("📨 Preparing post for Make.com (IG + FB + TikTok)…")

    # Allow Cloudinary CDN propagation
    PRE_DELAY = 12
    print(f"⏳ Waiting {PRE_DELAY}s to allow Cloudinary/CDN propagation…")
    time.sleep(PRE_DELAY)

    payload = {
        "ig_caption": ig_caption,
        "fb_caption": fb_caption,
        "media_url": media_url,
        "media_type": media_type,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Retry logic
    max_attempts = 3
    backoff_seconds = [2, 4, 6]

    for attempt in range(1, max_attempts + 1):
        print(f"➡️ Attempt {attempt}/{max_attempts} sending to Make…")

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"x-make-apikey": MAKE_API_KEY},
                timeout=20
            )

            if response.status_code == 200:
                print("📣 Successfully sent payload to Make.com (200).")
                return True

            print(f"⚠️ Make.com returned {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Request error: {e}")

        if attempt < max_attempts:
            wait = backoff_seconds[attempt - 1]
            print(f"⏳ Waiting {wait}s before retry…")
            time.sleep(wait)

    print("❌ Failed to send post after multiple attempts.")
    return False
