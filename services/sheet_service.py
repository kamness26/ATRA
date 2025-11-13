"""
Sheet Service
Handles appending prompt + image data to Google Sheets.
"""

import os
import datetime
import gspread
from google.oauth2.service_account import Credentials

def update_sheet(prompt: str, image_url: str) -> None:
    """Append a row [timestamp, prompt, image_url] to the target Google Sheet."""
    creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
    sheet_id = os.getenv("SHEET_ID")

    if not creds_path or not sheet_id:
        print("⚠️ Missing Sheets credentials or sheet ID.")
        return

    try:
        # Authorize the client
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)

        # Open the sheet and append
        sheet = client.open_by_key(sheet_id).sheet1
        timestamp = datetime.datetime.now().isoformat()
        sheet.append_row([timestamp, prompt, image_url])
        print(f"📒 Added new row at {timestamp}")

    except Exception as e:
        print(f"❌ Failed to update Google Sheet: {e}")

