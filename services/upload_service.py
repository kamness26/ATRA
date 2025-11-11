"""
Upload Service
Handles uploading generated assets to Cloudinary.
"""

import os
import cloudinary
import cloudinary.uploader

# Initialize Cloudinary using your environment variable (CLOUDINARY_URL)
cloudinary.config(cloudinary_url=os.getenv("CLOUDINARY_URL"))

def upload_asset(image_path: str) -> str:
    """Uploads an image to Cloudinary and returns the hosted URL."""
    print(f"☁️ Uploading asset from: {image_path}")

    try:
        response = cloudinary.uploader.upload(image_path, folder="atra_outputs")
        secure_url = response.get("secure_url")
        print(f"☁️ Uploaded successfully: {secure_url}")
        return secure_url
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

