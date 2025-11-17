"""
Upload Service
Handles uploading generated assets to Cloudinary.
"""

import os
import cloudinary
import cloudinary.uploader

# Initialize Cloudinary using the CLOUDINARY_URL environment variable
cloudinary.config(cloudinary_url=os.getenv("CLOUDINARY_URL"))

def upload_asset(image_path: str) -> str:
    """Uploads an image to Cloudinary and returns the raw public URL."""
    print(f"☁️ Uploading asset from: {image_path}")

    try:
        # Upload to Cloudinary with no transformations
        response = cloudinary.uploader.upload(
            image_path,
            folder="atra_outputs",
            resource_type="image"
        )

        secure_url = response.get("secure_url")
        print(f"☁️ Uploaded successfully: {secure_url}")

        # IMPORTANT:
        # Do NOT modify this URL. Instagram requires the original, untransformed asset.
        return secure_url

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

