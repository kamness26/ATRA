import os
from typing import Any, Dict, Optional, Tuple

import requests

API_BASE = "https://open.tiktokapis.com"
DEFAULT_PRIVACY_LEVEL = "SELF_ONLY"
PRIVACY_LEVELS = {
    "SELF_ONLY",
    "PUBLIC_TO_EVERYONE",
    "MUTUAL_FOLLOW_FRIENDS",
    "FOLLOWER_OF_CREATOR",
}


class TikTokPoster:
    def __init__(self, access_token: Optional[str] = None, api_base: str = API_BASE) -> None:
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("TIKTOK_ACCESS_TOKEN env var is required for TikTok posting.")
        self.api_base = api_base.rstrip("/")

    def init_post(self, video_size: int, caption: str, privacy_level: str = DEFAULT_PRIVACY_LEVEL) -> Tuple[str, str]:
        privacy = self._normalize_privacy(privacy_level)
        url = f"{self.api_base}/v2/post/publish/video/init/"
        payload = {
            "post_info": {
                "title": caption,
                "privacy_level": privacy,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1,
            },
        }
        response = requests.post(url, json=payload, headers=self._json_headers(), timeout=30)
        data = self._parse_tiktok_response(response)
        publish_id = data.get("publish_id")
        upload_url = data.get("upload_url")
        if not publish_id or not upload_url:
            raise RuntimeError("TikTok init response missing publish_id or upload_url.")
        return publish_id, upload_url

    def upload_video(self, upload_url: str, video_bytes: bytes, video_size: int) -> None:
        headers = {
            "Content-Type": "video/mp4",
            "Content-Length": str(video_size),
            "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
        }
        response = requests.put(upload_url, data=video_bytes, headers=headers, timeout=120)
        if response.status_code not in (200, 201, 204):
            raise RuntimeError(f"Video upload failed ({response.status_code}): {response.text}")

    def fetch_status(self, publish_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/v2/post/publish/status/fetch/"
        response = requests.post(
            url,
            json={"publish_id": publish_id},
            headers=self._json_headers(),
            timeout=15,
        )
        data = self._parse_tiktok_response(response)
        return {
            "status": data.get("status"),
            "fail_reason": data.get("fail_reason"),
            "publicly_available_post_id": data.get("publicly_available_post_id")
            or data.get("publicaly_available_post_id"),
        }

    def _json_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        }

    def _parse_tiktok_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code != 200:
            raise RuntimeError(f"TikTok API request failed ({response.status_code}): {response.text}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(f"TikTok API returned non-JSON body ({response.status_code}).") from exc

        error = payload.get("error") or {}
        code = error.get("code")
        if code and code != "ok":
            message = error.get("message") or "TikTok API error"
            log_id = error.get("log_id")
            suffix = f" (log_id={log_id})" if log_id else ""
            raise RuntimeError(f"TikTok API error: {message}{suffix}")

        data = payload.get("data")
        if data is None:
            raise RuntimeError("TikTok API response missing data field.")
        return data

    def _normalize_privacy(self, privacy_level: str) -> str:
        privacy = (privacy_level or DEFAULT_PRIVACY_LEVEL).strip().upper()
        if privacy not in PRIVACY_LEVELS:
            raise ValueError(f"Unsupported privacy level '{privacy}'. Allowed: {', '.join(sorted(PRIVACY_LEVELS))}.")
        return privacy
