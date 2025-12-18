# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of main.py.

"""
ATRA Automation Orchestrator
main.py v2.0 – Joanie Modes + Sora Video Integration (TikTok Phase 1)

Pipeline:
prompt → image → optional video → upload → sheet → Make.com (IG, FB, TikTok)
"""

from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime

# Load environment
load_dotenv(dotenv_path=".env", override=True)
print("🔍 ENV check – CLOUDINARY_URL loaded:", bool(os.getenv("CLOUDINARY_URL")))

# Service imports
from services.post_service import send_to_make_webhook
from services.prompt_service import generate_prompt
from services.image_service import generate_image
from services.video_service import generate_video  # NEW
from services.upload_service import upload_asset
from services.sheet_service import update_sheet
from services.caption_service import (
    generate_instagram_caption,
    generate_facebook_caption,
)

# Joanie personality modes
PERSONALITY_MODES = {
    "corporate_burnout": "😵‍💼",
    "adhd_spiral": "🌀",
    "delusional_romantic": "💘",
    "existentially_exhausted": "🫠",
    "sunday_scaries": "😨",
}

STATE_FILE = "state/joanie_history.json"


# ---------------------------------------------------------
# Phase 2: Mood Persistence Engine
# ---------------------------------------------------------
def _load_history():
    """Load last 5 modes from state file."""
    if not os.path.exists("state"):
        os.makedirs("state")

    if not os.path.isfile(STATE_FILE):
        return []

    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("recent_modes", [])
    except:
        return []


def _save_history(history):
    """Save the last 5 modes."""
    with open(STATE_FILE, "w") as f:
        json.dump({"recent_modes": history[-5:]}, f)


def choose_joanie_mode():
    """Weighted mood selection with Sunday override."""
    history = _load_history()
    today = datetime.now().strftime("%A")

    # Sunday override
    if today == "Sunday":
        if not history or history[-1] != "sunday_scaries":
            _save_history(history + ["sunday_scaries"])
            return "sunday_scaries"

    last = history[-1] if history else None

    weights = {m: 1.0 for m in PERSONALITY_MODES}

    # No immediate repeat
    if last in weights:
        weights[last] = 0.0

    # Recency down-weighting
    for i, rm in enumerate(reversed(history)):
        if rm in weights and weights[rm] > 0:
            weights[rm] *= (0.7 - 0.1 * i)

    # Rarity boost
    for m in PERSONALITY_MODES:
        if m not in history:
            weights[m] *= 1.6

    pool = [(m, w) for m, w in weights.items() if w > 0]
    modes, wts = zip(*pool)
    chosen = random.choices(modes, weights=wts, k=1)[0]

    _save_history(history + [chosen])
    return chosen


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------
def run_once() -> None:
    print("🚀 ATRA main.py v2.0 – starting run with Sora video support")

    # 0. Choose emotional mode
    mode = choose_joanie_mode()
    emoji = PERSONALITY_MODES[mode]
    print(f"🎭 Joanie Mode → {mode} {emoji}")

    # 1. Generate journaling prompt
    prompt = generate_prompt(mode)
    print(f"🧠 Prompt: {prompt}")

    # 2. Generate base image (always)
    image_path = generate_image(prompt, mode)
    print(f"🎨 Image generated: {image_path}")

    image_url = upload_asset(image_path)
    print(f"☁️ Image uploaded: {image_url}")

    # 3. Attempt Sora video generation
    #    If video fails, we still post image normally
    video_url = None
    media_type = "image"

    try:
        print("🎥 Attempting Sora 2 video generation…")
        # Reconstruct day-items logic by calling image_service helper
        from services.image_service import _get_day_items
        day_items = _get_day_items()

        video_url = generate_video(prompt, mode, day_items)
        media_type = "video"
        print(f"🎬 Video generated + uploaded: {video_url}")

    except Exception as exc:
        print(f"⚠️ Sora video generation failed, falling back to image only. Reason: {exc}")

    # 4. Log to Google Sheet (store both if available)
    update_sheet(prompt, video_url or image_url)
    print("📒 Sheet updated")

    # 5. Captions for IG + FB
    ig_caption = generate_instagram_caption(prompt, mode)
    fb_caption = generate_facebook_caption(prompt, mode)

    print("📝 IG Caption:", ig_caption)
    print("📝 FB Caption:", fb_caption)

    # 6. Send to Make.com for posting to IG + FB + TikTok
    WEBHOOK_URL = "https://hook.us2.make.com/cx9uy79z1rar2h907adqw8mhbunppnt7"

    print("📨 Sending media to Make.com…")
    posted = send_to_make_webhook(
        ig_caption=ig_caption,
        fb_caption=fb_caption,
        media_url=video_url or image_url,
        media_type=media_type,       # NEW → image or video
        webhook_url=WEBHOOK_URL,
    )

    if posted:
        print("✅ Social post sent successfully.")
    else:
        print("⚠️ Something went wrong sending to Make.com.")

    print("🎉 ATRA run complete.")


if __name__ == "__main__":
    run_once()
