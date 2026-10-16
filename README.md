# API Crest Developer Examples

Documentation-grounded, copy-ready starter scripts for developers integrating [API Crest](https://apicrest.com/). This repository is maintained as an **API Crest-affiliated developer resource**, not an independent benchmark or review.

> **Status (2026-10-16):** Routes, fields, model IDs, and caveats below were checked against the [public API documentation](https://apicrest.com/apidoc?theme=light). No paid API requests were run while preparing these examples. The programs have been checked offline for syntax and basic contract-handling only. Availability, pricing, performance, and generation quality are **not** asserted. Check the live docs and pricing before use.

## What's inside

| Use case | Python | Node.js 20+ | Documented route |
| --- | --- | --- | --- |
| Text response with Anthropic-style messages | [`chat_messages.py`](examples/python/chat_messages.py) | [`chat_messages.mjs`](examples/node/chat_messages.mjs) | `POST /v1/messages` |
| Edit an existing product image | [`image_edit.py`](examples/python/image_edit.py) | [`image_edit.mjs`](examples/node/image_edit.mjs) | `POST /v1/images/edits` |
| Submit and poll an async media task | [`media_async.py`](examples/python/media_async.py) | [`media_async.mjs`](examples/node/media_async.mjs) | `POST /v1/media/generate`, `GET /v1/media/status` |

All examples use the documented base URL `https://api.vv666.ai` and read your API key from **the environment** (never from checked-in source). Every example requires an explicit `--run` flag to prevent accidental billable requests.

## Quick start

**Python 3.10+**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export APICREST_API_KEY="YOUR_REAL_API_KEY"
python examples/python/chat_messages.py --run
python examples/python/image_edit.py --run --image ./product.png --out ./edited.png
python examples/python/media_async.py --run
```

In Windows PowerShell use `$env:APICREST_API_KEY = "YOUR_REAL_API_KEY"`, then run the same `python ...` commands. Always provide your **own authorized** `product.png` and inspect results for packaging/label errors before commercial use.

**Node.js 20+** (no third-party packages)

```bash
export APICREST_API_KEY="YOUR_REAL_API_KEY"
node examples/node/chat_messages.mjs --run
node examples/node/image_edit.mjs --run --image ./product.png --out ./edited-node.png
node examples/node/media_async.mjs --run
```

The scripts intentionally refuse to make API calls when `--run` is missing. **These example calls may incur charges.** We have not run them against the live service, so returned shapes and account/model availability should be tested by each developer in an authorized account with a small budget.

## Model IDs and contract assumptions

The public documentation currently lists `claude-haiku-5-5` for the Anthropic-style messages endpoint and `gpt-image-2.5` for the image examples. Override with `APICREST_CHAT_MODEL` or `APICREST_IMAGE_MODEL` only after reviewing the current model catalog.

- **Messages:** POST JSON `{ model, max_tokens, messages }`, with a documented API key authentication header. Samples use `Authorization: Bearer`.
- **Image edits:** multipart with `model`, `prompt`, repeated `image[]`, `size`, `quality`, `response_format=b64_json`. Synchronous request; a dropped connection **does not imply cancellation**. Save any `X-Task-Id` or `error.task_id` to reconcile the result/cost through `GET /v1/skills/task-status?task_id=...`.
- **Async media:** POST `{ model, prompt, params }`; save the returned `task_id` before polling `GET /v1/media/status?task_id=...`. Status fields documented include `state`, `is_final`, `result_url`, and `error`. These examples poll every 8 seconds with a 10-minute deadline.
- **No documented generic idempotency key:** Do not automatically retry a billable POST if the outcome is unknown. Poll or reconcile known task IDs first.

See [integration safety notes](docs/INTEGRATION_NOTES.md) for billing, webhooks, size limitations, and security caveats.

## Safe offline checks

No API key is required for these tests. CI deliberately does **not** send traffic to API Crest.

```bash
python -m compileall -q examples/python tests
python -m unittest discover -s tests -v
node --check examples/node/chat_messages.mjs
node --check examples/node/image_edit.mjs
node --check examples/node/media_async.mjs
```

## Questions, security, and attribution

Reference: [API Crest API docs](https://apicrest.com/apidoc?theme=light) · [Main site](https://apicrest.com/) · [Technical tutorials on DEV](https://dev.to/_d32a5a2f243220ade32f48).

Open issues for **reproducible, non-sensitive** problems and refer to [SECURITY.md](SECURITY.md) for private vulnerability reporting guidance. Never paste keys, bearer headers, paid usage logs, or customer data into issues.

This repository is licensed under the [MIT License](LICENSE). It provides examples **as-is**, without uptime, price, feature, or performance guarantees.