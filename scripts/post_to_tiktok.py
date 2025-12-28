import argparse
import os
import sys
import time

from dotenv import load_dotenv

from services.tiktok import DEFAULT_PRIVACY_LEVEL, PRIVACY_LEVELS, TikTokPoster


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post a single MP4 to TikTok via Direct Post.")
    parser.add_argument("--video", required=True, help="Path to the MP4 file to upload.")
    parser.add_argument("--caption", required=True, help="Caption/title for the TikTok post.")
    parser.add_argument(
        "--privacy",
        default=DEFAULT_PRIVACY_LEVEL,
        choices=sorted(PRIVACY_LEVELS),
        help="TikTok privacy level. Defaults to SELF_ONLY.",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        help="Poll status up to 10 times with 3s intervals until completion or failure.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    video_path = os.path.abspath(args.video)
    if not os.path.isfile(video_path):
        print(f"Video not found: {video_path}")
        sys.exit(1)

    with open(video_path, "rb") as file_handle:
        video_bytes = file_handle.read()
    video_size = len(video_bytes)

    print(f"Preparing TikTok upload for {video_path} ({video_size} bytes)")
    poster = TikTokPoster()

    print("Initializing Direct Post upload session...")
    publish_id, upload_url = poster.init_post(
        video_size=video_size,
        caption=args.caption,
        privacy_level=args.privacy,
    )
    print(f"Publish ID: {publish_id}")

    print("Uploading video...")
    poster.upload_video(upload_url=upload_url, video_bytes=video_bytes, video_size=video_size)
    print("Upload request completed.")

    def print_status(step: str, info: dict) -> None:
        status = info.get("status")
        fail_reason = info.get("fail_reason")
        public_id = info.get("publicly_available_post_id")
        extra = []
        if fail_reason:
            extra.append(f"fail_reason={fail_reason}")
        if public_id:
            extra.append(f"public_post_id={public_id}")
        suffix = f" ({'; '.join(extra)})" if extra else ""
        print(f"{step}: {status}{suffix}")

    print("Fetching status...")
    status_info = poster.fetch_status(publish_id)
    print_status("Status", status_info)

    if args.poll:
        for attempt in range(1, 11):
            if status_info.get("status") in ("PUBLISH_COMPLETE", "FAILED"):
                break
            time.sleep(3)
            status_info = poster.fetch_status(publish_id)
            print_status(f"Poll {attempt}", status_info)

    print("Done.")


if __name__ == "__main__":
    main()
