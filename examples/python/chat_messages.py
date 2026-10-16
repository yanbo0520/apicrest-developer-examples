"""Minimal Anthropic-compatible chat request. --run may incur charges."""

import os
import requests
from common import BASE_URL, extract_text, parser, require_execution


def main():
    args = parser("API Crest: Anthropic-compatible messages example").parse_args()
    key = require_execution(args.run)
    model = os.getenv("APICREST_CHAT_MODEL", "claude-haiku-5-5")
    # Do not automatically retry POST: the request may already have been accepted.
    response = requests.post(
        f"{BASE_URL}/v1/messages",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": model,
            "max_tokens": 256,
            "messages": [{"role": "user", "content": "Explain idempotency in two sentences."}],
        },
        timeout=(10, 60),
    )
    response.raise_for_status()
    print(extract_text(response.json()))


if __name__ == "__main__":
    main()
