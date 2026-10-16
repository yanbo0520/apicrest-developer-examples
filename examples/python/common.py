"""Non-network helpers shared by the API Crest example scripts."""

import argparse
import os

BASE_URL = "https://api.vv666.ai"


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--run", action="store_true", help="Opt in to a potentially billable API call")
    return p


def require_execution(run: bool, environ=None) -> str:
    """Return a key only after explicit consent; do not print it."""
    if not run:
        raise SystemExit("Dry by default: supply --run only after checking API pricing and permissions.")
    env = os.environ if environ is None else environ
    key = env.get("APICREST_API_KEY", "").strip()
    if not key or key in {"YOUR_API_KEY", "YOUR_REAL_API_KEY", "REPLACE_WITH_YOUR_OWN_KEY"}:
        raise SystemExit("Set a private APICREST_API_KEY environment variable first.")
    return key


def error_task_id(body):
    if not isinstance(body, dict):
        return None
    obj = body.get("error")
    return obj.get("task_id") if isinstance(obj, dict) else None


def extract_text(body):
    """Flatten Anthropic-style text blocks without guessing non-text content."""
    blocks = body.get("content", []) if isinstance(body, dict) else []
    return "\n".join(b["text"] for b in blocks if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str))


def classify_media_job(body):
    """Return 'pending', 'success', 'failed' or 'unknown' from a status response."""
    if not isinstance(body, dict):
        return "unknown"
    state = body.get("state")
    if state == "success" and body.get("is_final") is True:
        return "success"
    if state == "failed" and body.get("is_final") is True:
        return "failed"
    if state in {"pending", "running"} and body.get("is_final") is not True:
        return "pending"
    return "unknown"
