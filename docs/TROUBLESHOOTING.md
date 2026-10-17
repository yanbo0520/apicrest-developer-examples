# Troubleshooting API integrations

Practical checks for developers following the [API Crest examples](../README.md). The repository is **API Crest-affiliated**. The examples are based on [public API documentation](https://apicrest.com/apidoc?theme=light), with **offline-only checks**; paid model behavior and channel availability have not been independently verified here.

This guide prioritizes **getting an integration working**. It is not a pricing comparison, a performance claim, or an availability guarantee.

## 1. Identify which workflow failed

| Your goal | Example | Documented endpoint | First thing to inspect |
| --- | --- | --- | --- |
| Chat / text messages | [Python](../examples/python/chat_messages.py) · [Node.js](../examples/node/chat_messages.mjs) | `POST /v1/messages` | Auth, chosen model, `messages` and `max_tokens` |
| Edit an uploaded image | [Python](../examples/python/image_edit.py) · [Node.js](../examples/node/image_edit.mjs) | `POST /v1/images/edits` | Multipart upload field `image[]`, accepted file format, response type |
| Run an asynchronous media task | [Python](../examples/python/media_async.py) · [Node.js](../examples/node/media_async.mjs) | `POST /v1/media/generate` and `GET /v1/media/status` | Store the exact `task_id` from submission; inspect `state` and `is_final` |

**Do not use the example model names as a permanent model catalog.** Verify the current model/channel combination in the [live docs](https://apicrest.com/apidoc?theme=light) and your account.

## 2. Run safe checks before any model request

```bash
# Clone the source:
git clone https://github.com/yanbo0520/apicrest-developer-examples.git
cd apicrest-developer-examples

# Offline Python checks (zero paid calls):
python -m compileall -q examples/python tests
python -m unittest discover -s tests -v

# Offline Node.js checks (Node.js 20+):
node --check examples/node/common.mjs
node --check examples/node/chat_messages.mjs
node --check examples/node/image_edit.mjs
node --check examples/node/media_async.mjs
node --test tests/test_node_contracts.mjs
```

The sample scripts deliberately require `--run` before making a network request. Passing the flag can result in charges; offline test success does **not** prove that live model requests will succeed.

## 3. Check HTTP errors without revealing your credentials

| Symptom | What to check | Safe next step |
| --- | --- | --- |
| 400 or validation error | Route, documented field names, supported model, JSON vs multipart format | Compare the sanitized request shape against live docs |
| 401 or 403 | Private key in the environment, key authorization, account/channel access | Check account configuration; never paste a key or full Authorization header into an issue |
| 404 | Base URL, exact endpoint path, model/channel name | Copy routes from the current provider documentation |
| 413 or rejected upload | Image count, file size, file format, channel-specific limits | Validate file size and format locally before reattempting |
| 429 | Whether a documented rate limit or capacity restriction applies | Review any documented backoff guidance and `Retry-After`; do not assume when a new billable POST is safe |
| 5xx, timeout or disconnection | Whether a side-effecting request already reached the server | **Stop automatic submission retries**; retain task ID, investigate task/account state |
| Parsed response missing text/image/status fields | Whether you used the correct protocol and expected response schema | Inspect a **sanitized** response *shape*, not secret/private contents |

These are general HTTP troubleshooting categories, **not** claims that API Crest returns every status under each scenario.

## 4. Don't confuse accepted submissions with completed media jobs

For asynchronous media tasks:

1. Save the `task_id` returned by `POST /v1/media/generate` immediately.
2. Poll `GET /v1/media/status?task_id=...` at a moderate interval.
3. Treat documented `state=success` and `is_final=true` as successful completion, and documented `state=failed` with `is_final=true` as a completed failure.
4. For `pending`/`running`, continue only up to a client-defined deadline. If status fields are missing or unfamiliar, pause and check docs rather than submitting a duplicate job.
5. For ambiguous synchronous image-edit requests, retain any `X-Task-Id` or `error.task_id`; the public documentation describes `GET /v1/skills/task-status?task_id=...` to inspect settlement.

**A timeout is not proof of cancellation.** This matters for any asynchronous or side-effecting API, not just AI generation.

## 5. Troubleshooting output images

When a media endpoint responds successfully but the application cannot display the output:

- Check whether the documented response contains base64 image bytes or a URL before applying a decoder.
- Validate base64 encoding and output file type locally. Don't assume JSON, an image link, and raw binary are interchangeable.
- For edited product images, inspect labels, logos, quantities and packaging before commercial use. Model-generated details can differ from the source.

## 6. Ask an actionable technical question

If you're blocked, use the [Integration question issue template](https://github.com/yanbo0520/apicrest-developer-examples/issues/new/choose).

A good issue contains a workflow name, the *sanitized* request shape (no key/header), HTTP status or task state, expected vs observed behavior, and the documentation URL. Never include API keys, bearer tokens, invoices, identifiable customer records, private prompts, or copyrighted media you cannot share.

**Start here:** [API Crest site](https://apicrest.com/?utm_source=github&utm_medium=referral&utm_campaign=developer_examples) · [API docs](https://apicrest.com/apidoc?theme=light) · [Developer examples](../README.md).
