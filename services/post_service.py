"""
Post Service
Sends posts to Make.com Instagram webhook with:
- API key authentication
- Controlled pre-delay for Cloudinary propagation
- Retry/backoff logic to avoid IG Error 9007 (media not available)
"""

import time
import requests
from datetime import datetime

# ---------------------------
# CHANGE THIS TO YOUR REAL KEY
# ---------------------------
MAKE_API_KEY = "atra_2025_supersecret"
# (Matches the API key you set in Make.com)


def send_to_make_webhook(caption: str, image_url: str, webhook_url: str) -> bool:
    """Send post data to Make.com webhook with predictable timing
    and correct API key authentication.
    """

    payload = {
        "caption": caption,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat()
    }

    print("📨 Preparing Instagram post via Make.com...")

    # Instagram fix — allow Cloudinary image URL to fully propagate
    PRE_DELAY = 6
    print(f"⏳ Waiting {PRE_DELAY}s to allow Cloudinary/CDN propagation...")
    time.sleep(PRE_DELAY)

    # Retry settings
    max_attempts = 3
    backoff_seconds = [2, 4, 6]

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"➡️ Attempt {attempt}/{max_attempts} sending to Make...")

            response = requests.post(
                webhook_url,
                json=payload,
                headers={"x-make-apikey": MAKE_API_KEY},
                timeout=15
            )

            if response.status_code == 200:
                print("📣 Successfully sent post payload to Make.com (200).")
                return True

            print(f"⚠️ Make.com returned status {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Request error: {e}")

        # If not last attempt, wait before retry
        if attempt < max_attempts:
            wait = backoff_seconds[attempt - 1]
            print(f"⏳ Waiting {wait}s before retry...")
            time.sleep(wait)

    print("❌ Failed to send post after multiple attempts.")
    return False

