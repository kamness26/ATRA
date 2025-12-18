# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Video Service – ATRA (Sora 2 TikTok Engine v2.0 – Official API Integration)

import os
from datetime import datetime
from openai import OpenAI

from services.video_upload_service import upload_video_to_cloudinary

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Default model for TikTok videos
VIDEO_MODEL = os.getenv("ATRA_VIDEO_MODEL", "sora-2")

OUTPUT_DIR = "output_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _construct_video_prompt(mode: str, day_items: str) -> str:
    """
    Build Joanie-mode micro-story vignette prompt for Sora 2.
    Keeps tone realistic, funny, light, and object-driven.
    """
    return f"""
    Create a 6 second vertical TikTok-style looping video (1080×1920) showing
    a realistic top-down desk vignette that humorously expresses the emotional mode.

    STYLE:
    - Realistic everyday desk setup, cinematic lighting, textured shadows
    - Light, funny, self-aware Joanie-style tone
    - No humans visible; express emotion through objects + lighting
    - Subtle looping motion (soft camera drift, object micro-motion)
    - Aesthetic messy chaos, but believable
    - No surreal effects, no magical animation, no text overlays

    JOURNAL:
    A blank matte-black paperback notebook sits naturally in the scene.
    (Final branded cover will be applied in post-processing.)

    MODE-SPECIFIC MOVEMENT GUIDANCE:
    - corporate_burnout → lamp flicker, papers lifting slightly, slow drift
    - adhd_spiral → pens rolling gently, receipts fluttering
    - delusional_romantic → soft glow shimmer, floating petal
    - existentially_exhausted → slow push-in, candle flicker, drifting dust
    - sunday_scaries → iced coffee sweating, remote vibrating lightly

    Day clutter: {day_items}
    Mode: {mode}
    """


def generate_video(prompt: str, mode: str, day_items: str) -> str:
    """
    Generate a Sora 2 video using official create-poll-download flow.
    Save locally, upload to Cloudinary, return the public URL.
    """
    sora_prompt = _construct_video_prompt(mode, day_items)

    print(f"🎥 Starting Sora 2 job for mode '{mode}'...")

    # Create + automatically poll for completion
    video_job = client.videos.create_and_poll(
        model=VIDEO_MODEL,
        prompt=sora_prompt,
        size="1080x1920",
        seconds=6,
    )

    if video_job.status != "completed":
        raise RuntimeError(
            f"Sora video generation failed (status={video_job.status}). Error: {getattr(video_job, 'error', None)}"
        )

    print("✨ Sora 2 job completed successfully.")

    # Download MP4 content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_path = os.path.join(OUTPUT_DIR, f"atra_video_{timestamp}.mp4")

    print("⬇️  Downloading Sora video content...")
    video_content = client.videos.download_content(video_job.id, variant="video")
    video_content.write_to_file(local_path)

    print(f"🎬 Video saved locally: {local_path}")
    print("☁️ Uploading video to Cloudinary...")

    # Upload video to Cloudinary
    cloudinary_url = upload_video_to_cloudinary(local_path)

    print(f"✅ Cloudinary Video URL: {cloudinary_url}")
    return cloudinary_url

