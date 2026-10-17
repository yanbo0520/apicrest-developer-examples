# API Crest Developer Examples — Python & Node.js AI API Integration

Build AI features with documented [API Crest](https://apicrest.com/) API request examples. This repository shows how to integrate chat, product-image editing, and asynchronous media jobs in Python or Node.js 20+.

**[Explore API Crest](https://apicrest.com/?utm_source=github&utm_medium=referral&utm_campaign=developer_examples)** · **[API documentation](https://apicrest.com/apidoc?theme=light)** · **[Python quick start](#quick-start)** · **[Node.js quick start](#quick-start)** · **[Ask a technical question](https://github.com/yanbo0520/apicrest-developer-examples/issues/new/choose)**

## Choose your integration

| Building… | Python example | Node.js example | Documented protocol |
| --- | --- | --- | --- |
| An AI chat feature | [Messages API](examples/python/chat_messages.py) | [Messages API](examples/node/chat_messages.mjs) | `POST /v1/messages` |
| Product photo editing | [Multipart image edits](examples/python/image_edit.py) | [Multipart image edits](examples/node/image_edit.mjs) | `POST /v1/images/edits` |
| AI image/media jobs that take time | [Submit + poll](examples/python/media_async.py) | [Submit + poll](examples/node/media_async.mjs) | `POST /v1/media/generate` + `GET /v1/media/status` |

### From documentation to your first authorized request

1. **[Visit API Crest](https://apicrest.com/?utm_source=github&utm_medium=referral&utm_campaign=developer_examples)** and check the current account and API-key onboarding process.
2. **[Read the live docs](https://apicrest.com/apidoc?theme=light)** for compatible model IDs, request fields, supported channels, and current pricing and availability.
3. **Clone this repository and run the [offline checks](#safe-offline-checks)**. These do not require an API key or make paid network calls.
4. **Choose one example**, load your own private `APICREST_API_KEY`, and deliberately pass `--run` only when you have reviewed any potential charges.
5. **Persist task IDs** for async jobs. If a billable submission times out, don't blindly retry it.

For a longer worked example, read [Build AI API Examples That Cannot Accidentally Run a Billable Request](https://apicrest.hashnode.dev/build-ai-api-examples-that-cannot-accidentally-run-a-billable-request). For sensitive problems, read [SECURITY.md](SECURITY.md); for a general docs mismatch, [ask a sanitized integration question](https://github.com/yanbo0520/apicrest-developer-examples/issues/new/choose).

**Scope:** API Crest-affiliated examples based on [public documentation reviewed October 16, 2026](https://apicrest.com/apidoc?theme=light). Offline syntax/contract checks passed, but no paid API calls, availability tests, performance benchmarks, or price comparisons were performed. Model availability and real behavior depend on the live service and your account. The UTM campaign link does not imply website-side tracking is installed.

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

See [integration safety notes](docs/INTEGRATION_NOTES.md) for billing, webhooks, size limitations, and security caveats, and [maintainer instructions](docs/PUBLISHING.md).

For outreach, use the [channel attribution plan](docs/OUTREACH_TRACKING.md) rather than assuming clicks, signups, or purchases are tracked automatically.

## Safe offline checks

No API key is required for these tests. CI deliberately does **not** send traffic to API Crest.

```bash
python -m compileall -q examples/python tests
python -m unittest discover -s tests -v
node --check examples/node/chat_messages.mjs
node --check examples/node/image_edit.mjs
node --check examples/node/media_async.mjs
node --test tests/test_node_contracts.mjs
```

## Questions, security, and attribution

Reference: [API Crest API docs](https://apicrest.com/apidoc?theme=light) · [Main site](https://apicrest.com/) · [Technical tutorials on DEV](https://dev.to/_d32a5a2f243220ade32f48).

Open issues for **reproducible, non-sensitive** problems and refer to [SECURITY.md](SECURITY.md) for private vulnerability reporting guidance. Never paste keys, bearer headers, paid usage logs, or customer data into issues.

This repository is licensed under the [MIT License](LICENSE). It provides examples **as-is**, without uptime, price, feature, or performance guarantees.