"""Multipart image edit example. --run submits one potentially billable POST."""

import argparse
import base64
import binascii
import os
from pathlib import Path

import requests
from common import BASE_URL, error_task_id, parser, require_execution


def main():
    p = parser("API Crest: image edits to local PNG (one submission only)")
    p.add_argument("--image", type=Path, required=True, help="Local authorized PNG/JPEG file")
    p.add_argument("--out", type=Path, default=Path("edited.png"))
    args = p.parse_args()
    key = require_execution(args.run)
    if not args.image.is_file():
        p.error("Image not found.")
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(args.image.suffix.lower())
    if mime is None:
        p.error("This example accepts PNG or JPEG only.")
    if args.image.stat().st_size > 10 * 1024 * 1024:
        p.error("Example safety limit: local image must be <= 10 MiB. Review current docs.")

    # A long read timeout is important for this synchronous, billable call.
    with args.image.open("rb") as source:
        try:
            response = requests.post(
                f"{BASE_URL}/v1/images/edits",
                headers={"Authorization": f"Bearer {key}"},
                files={"image[]": (args.image.name, source, mime)},
                data={
                    "model": os.getenv("APICREST_IMAGE_MODEL", "gpt-image-2.5"),
                    "prompt": "Put the product on a clean wooden desk; preserve package details as closely as possible.",
                    "size": "1536x1024",
                    "quality": "high",
                    "response_format": "b64_json",
                },
                timeout=(10, 360),
            )
        except requests.Timeout:
            raise SystemExit("Timeout: task outcome UNKNOWN. Do not blindly re-submit a billable POST; reconcile account tasks.")
        except requests.RequestException:
            raise SystemExit("Network error: outcome may be UNKNOWN. Check account activity before retrying.")

    if response.headers.get("X-Task-Id"):
        print("Task ID for reconciliation:", response.headers["X-Task-Id"])
    if not response.ok:
        try:
            task_id = error_task_id(response.json())
            if task_id:
                print("Error task ID for status lookup:", task_id)
        except ValueError:
            pass
        raise SystemExit(f"API request returned HTTP {response.status_code}; no automatic retry.")

    body = response.json()
    try:
        encoded = body["data"][0]["b64_json"]
        result = base64.b64decode(encoded, validate=True)
    except (KeyError, IndexError, TypeError, ValueError, binascii.Error):
        raise SystemExit("Unexpected image response; inspect safe task-status data rather than re-submitting.")
    args.out.write_bytes(result)
    print("Saved edited image:", args.out)


if __name__ == "__main__":
    main()
