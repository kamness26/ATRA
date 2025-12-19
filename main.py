# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of main.py.

"""
ATRA Automation Orchestrator
main.py v1.3 – Joanie Personality Modes (Phase 2: Mood Persistence)

Coordinates all services:
prompt → image → upload → sheet → IG + FB (via Make.com)
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
from services.upload_service import upload_asset
from services.sheet_service import update_sheet
from services.caption_service import (
    generate_instagram_caption,
    generate_facebook_caption
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
# Phase 2: Mood Persistence Engine (Tier B)
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
    """Choose next Joanie mode using:
    - No repetition
    - Recency down-weighting
    - Rarity boosting
    - Sunday override
    """
    history = _load_history()
    today = datetime.now().strftime("%A")

    # --- 1. Sunday Scaries override ---
    if today == "Sunday":
        # But avoid repeating
        if len(history) == 0 or history[-1] != "sunday_scaries":
            _save_history(history + ["sunday_scaries"])
            return "sunday_scaries"

    last = history[-1] if history else None

    # --- 2. Base weights ---
    weights = {
        mode: 1.0 for mode in PERSONALITY_MODES.keys()
    }

    # --- 3. No immediate repetition ---
    if last in weights:
        weights[last] = 0.0

    # --- 4. Recency down-weighting ---
    # recent modes get suppressed slightly
    for i, recent_mode in enumerate(reversed(history)):
        if recent_mode in weights and weights[recent_mode] > 0:
            weights[recent_mode] *= (0.7 - 0.1 * i)  # gradually less

    # --- 5. Rarity boosting ---
    # modes not seen in 5 runs get boosted
    for mode in PERSONALITY_MODES:
        if mode not in history:
            weights[mode] *= 1.6

    # Normalize and pick
    pool = [(m, w) for m, w in weights.items() if w > 0]
    modes, wts = zip(*pool)
    chosen = random.choices(modes, weights=wts, k=1)[0]

    # Save
    _save_history(history + [chosen])

    return chosen


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------
def run_once() -> None:
    """Run the full ATRA pipeline once."""
    print("🚀 ATRA main.py v1.3 – starting run (Phase 2 enabled)")

    # 0. Choose Joanie personality mode (Phase 2 engine)
    mode = choose_joanie_mode()
    emoji = PERSONALITY_MODES[mode]
    print(f"🎭 Joanie Mode → {mode} {emoji}")

    # 1. Generate base journaling prompt
    prompt = generate_prompt(mode)
    print(f"🧠 Prompt generated: {prompt}")

    # 2. Generate image using brand rules
    image_path = generate_image(prompt, mode)
    print(f"🎨 Image generated at: {image_path}")

    # 3. Upload to Cloudinary
    image_url = upload_asset(image_path)
    print(f"☁️ Uploaded image to: {image_path}")

    # 4. Update Google Sheet log
    update_sheet(prompt, image_url)
    print("📒 Sheet updated successfully")

    # 5. Generate platform-specific captions
    ig_caption = generate_instagram_caption(prompt, mode)
    fb_caption = generate_facebook_caption(prompt, mode)

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
