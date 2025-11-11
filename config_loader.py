"""
Config Loader
Loads and validates environment variables for ATRA.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
SHEET_ID = os.getenv("SHEET_ID")


def validate_env():
    """Alert if any required environment variables are missing."""
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": OPENAI_API_KEY,
            "CLOUDINARY_URL": CLOUDINARY_URL,
            "GOOGLE_SHEETS_CREDENTIALS_PATH": GOOGLE_SHEETS_CREDENTIALS_PATH,
            "SHEET_ID": SHEET_ID,
        }.items()
        if not value
    ]
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
    else:
        print("✅ All environment variables loaded successfully.")

validate_env()

