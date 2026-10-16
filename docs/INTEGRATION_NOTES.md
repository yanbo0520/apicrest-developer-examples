# Integration safety notes

**Documentation check:** October 16, 2026. **Source:** [API Crest public API documentation](https://apicrest.com/apidoc?theme=light). These are documentation-based observations, not direct paid-endpoint verification.

## Billing and retries

- API calls **may be billable**. Review live model/channel pricing before any run; this repository contains no prices or savings claims.
- Public docs describe image edits as per-image billed; some Enhanced channels may cost more. Only account invoices/task settlement can establish actual charges.
- The synchronous images endpoint can continue processing and billing after the client times out. The docs describe an `X-Task-Id` response header and possible `error.task_id`; if you capture one, query `GET /v1/skills/task-status?task_id=...` rather than creating a duplicate POST.
- The asynchronous media route returns `task_id`; **persist it** and poll GET `/v1/media/status?task_id=...` at a moderate interval. Never spin in a tight loop.
- The docs describe `is_final`, `state` (`pending`, `running`, `success`, `failed`), `result_url`, and `error`. These examples handle final states conservatively; an undocumented or missing terminal state causes a failure rather than an endless loop.
- **Idempotency:** A generic `Idempotency-Key` contract was not confirmed. Do not assume a retry has exactly-once semantics.

## Image limits and format

- The image-editing docs describe `gpt-image-2.5`, multipart `image[]`, `response_format=b64_json`, optional `size` and `quality`.
- Reference images: up to 16 documented; individual channels may accept fewer.
- JSON inlined images: 10 MB per image decoded and 30 MB total per request documented; multipart guidance should be checked separately. Examples use a 10 MB local file cap as a conservative guard, not a platform-wide guarantee.
- The docs explicitly do **not** support `mask` or `n>1` in this integration.
- Logos, small text, labels, and product details can be altered; manually inspect any generated commercial asset.

## Secrets and transport

- Store tokens in a private environment or managed secrets vault. The sample `.env.example` contains **only placeholders**; the code does not automatically load `.env`.
- Use TLS and restrict access to task results. Log a task ID/status where safe, not secrets, complete request headers, sensitive prompts, or source images.
- `Authorization: Bearer` is documented; don't copy the literal placeholder values into real request headers.
- Timeouts and polling intervals in sample code are client choices. They are **not** service-level guarantees or benchmark measurements.

## Webhooks

- The media protocol documents optional `notify_url`. Verify authenticity of callbacks and make handlers idempotent if adopting webhooks; do not assume that a URL alone provides authenticity. Examples prefer polling to avoid implying a tested webhook verification method.

## Reproducibility and disclosure

Routes and model names were inspected in the [public docs](https://apicrest.com/apidoc?theme=light). Offline syntax/unit tests are not paid API integration tests. API Crest is the subject and affiliate of these examples; no outside endorsement or performance claim is implied.
