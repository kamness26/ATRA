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
    """Uploads an image to Cloudinary and returns an Instagram-safe direct binary URL."""
    print(f"☁️ Uploading asset from: {image_path}")

    try:
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(image_path, folder="atra_outputs")
        original_url = response.get("secure_url")
        print(f"☁️ Uploaded successfully: {original_url}")

        # Convert to Instagram-compatible direct JPEG binary URL
        # - fl_attachment forces binary delivery
        # - f_jpg forces JPEG conversion
        # - .jpg extension improves IG compatibility
        direct_url = (
            original_url
            .replace("/upload/", "/upload/fl_attachment,f_jpg/")
            .rsplit(".", 1)[0] + ".jpg"
        )

        print(f"☁️ Direct binary URL for IG: {direct_url}")

        return direct_url

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

