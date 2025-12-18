# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Cloudinary Video Upload Service – ATRA (v1.0)

import os
import cloudinary
import cloudinary.uploader

# Initialize Cloudinary (same as image uploads)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

def upload_video_to_cloudinary(local_video_path: str) -> str:
    """
    Upload a video file (mp4) to Cloudinary and return the public URL.
    """
    try:
        result = cloudinary.uploader.upload(
            local_video_path,
            resource_type="video",
            folder="ATRA_videos",
            overwrite=True,
        )
        return result["secure_url"]
    except Exception as exc:
        raise RuntimeError(f"Cloudinary video upload failed: {exc}") from exc

