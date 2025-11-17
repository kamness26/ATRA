import requests
from datetime import datetime

def post_to_instagram_webhook(caption: str, image_url: str, webhook_url: str):
    """
    Sends a payload to the Make.com webhook to trigger an Instagram post.
    """
    payload = {
        "caption": caption,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"📣 Successfully sent post payload to Make.com webhook ({resp.status_code})")
        return True
    except Exception as e:
        print(f"❌ Failed to send Instagram post payload: {str(e)}")
        return False

