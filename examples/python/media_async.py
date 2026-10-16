"""Submit ONE async media job and poll; never auto-retry creation POST."""

import os
import time
import requests
from common import BASE_URL, classify_media_job, error_task_id, parser, require_execution


def main():
    args = parser("API Crest: submit one async media job and poll").parse_args()
    key = require_execution(args.run)
    auth = {"Authorization": f"Bearer {key}"}
    try:
        created = requests.post(
            f"{BASE_URL}/v1/media/generate",
            headers=auth,
            json={
                "model": os.getenv("APICREST_IMAGE_MODEL", "gpt-image-2.5"),
                "prompt": "A small robot watering a bonsai tree, studio lighting.",
                "params": {"aspect_ratio": "1:1", "quality": "auto"},
            },
            timeout=(10, 30),
        )
    except requests.RequestException:
        raise SystemExit("Submission result unknown. Reconcile account tasks; do not submit again blindly.")
    if not created.ok:
        try:
            task_id = error_task_id(created.json())
            if task_id:
                print("Error task ID:", task_id)
        except ValueError:
            pass
        raise SystemExit(f"Submit HTTP {created.status_code}. No automatic retry.")
    try:
        task_id = created.json()["task_id"]
        if not isinstance(task_id, str) or not task_id:
            raise ValueError()
    except (KeyError, ValueError, TypeError):
        raise SystemExit("No valid task_id found. Check account activity before creating a new job.")
    print("Save this task ID:", task_id)

    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        time.sleep(8)
        try:
            check = requests.get(
                f"{BASE_URL}/v1/media/status", headers=auth,
                params={"task_id": task_id}, timeout=(10, 30),
            )
            check.raise_for_status()
            status = check.json()
        except (requests.RequestException, ValueError):
            print("Status lookup failed; task ID retained. Check later rather than resubmitting.")
            return
        outcome = classify_media_job(status)
        if outcome == "success":
            print("Result URL:", status.get("result_url", "(none returned)"))
            return
        if outcome == "failed":
            print("Task failed; check task status and account settlement. ID:", task_id)
            return
        if outcome == "unknown":
            print("Unrecognized task status. Stop and inspect docs/account. ID:", task_id)
            return
        print("Task still pending:", task_id)
    print("Polling deadline reached; task may continue. Keep task ID:", task_id)


if __name__ == "__main__":
    main()
