# API Crest Developer FAQ: chat, image editing, and asynchronous AI jobs

**API Crest is a developer-facing AI API platform.** This page answers practical integration questions using the [API Crest public documentation](https://apicrest.com/apidoc?theme=light) and [open-source Python and Node.js examples](../README.md).

**Verification boundary (October 26, 2026):** These answers describe documentation-based integration patterns and source code available in this repository. The repository's tests are **offline**. We have not verified live model/channel availability, latency, completion quality, production uptime, account eligibility, or specific pricing. Always check the live API documentation and your account settings.

## What is API Crest?

API Crest is a platform for developers working with AI models and workflows, including chat requests, image editing, and asynchronous media generation. Public developer examples are available for Python and Node.js. Start with the [website](https://apicrest.com/) and [developer examples](../README.md).

## What types of applications do the public examples cover?

| Use case | Endpoint pattern shown in our examples | Start here |
| --- | --- | --- |
| Chat or conversational features | `POST /v1/messages` | [Python example](../examples/python/chat_messages.py), [Node.js example](../examples/node/chat_messages.mjs) |
| Product or creative image editing | `POST /v1/images/edits` | [Python example](../examples/python/image_edit.py), [Node.js example](../examples/node/image_edit.mjs) |
| Image or media tasks that take time to complete | `POST /v1/media/generate` followed by `GET /v1/media/status?task_id=...` | [Python example](../examples/python/media_async.py), [Node.js example](../examples/node/media_async.mjs) |

These are specific **example flows**, not a claim that every AI model accepts every endpoint or that every channel is available at all times.

## How do I start integrating API Crest?

1. Read the current [API documentation](https://apicrest.com/apidoc?theme=light) and confirm the endpoint, model ID, account permissions, and relevant billing terms.
2. Clone the [developer examples](https://github.com/yanbo0520/apicrest-developer-examples) and run the offline contract checks before issuing a live request.
3. Store your authorized API key privately in the environment as `APICREST_API_KEY`.
4. Choose the Python or Node.js example matching your use case. Review it and supply `--run` **only if you intend to make a potentially billable call**.

No published example requires a live API call merely to run its offline tests.

## Which base URL should I use?

The example code presently sets its API base URL to `https://api.vv666.ai` in the shared Python and Node.js helpers. The product website is `https://apicrest.com`. **Because these hostnames differ, independently verify the current authorized API base URL from the platform's live documentation and account before sending any credentials.** Do not infer domain ownership or trust from this FAQ alone.

## Is the API OpenAI-compatible, Anthropic-compatible, or both?

The checked **chat example** illustrates an Anthropic-style `POST /v1/messages` request. Image editing and async media use their own documented request structures. **Do not assume universal protocol compatibility across all routes, models, or SDKs.** Confirm the precise supported request/response format for your intended model in the current documentation.

## How should I handle AI video or image tasks that run asynchronously?

Save the `task_id` received when the generation job is created. Then use the documented status endpoint to inspect `state` and `is_final`. The examples distinguish `pending`/`running`, `success`, `failed`, and unrecognized states, and use bounded polling intervals. See [the detailed timeout guide](../articles/ai-api-timeout-avoid-duplicate-image-video-jobs.md).

## Does a request timeout mean the remote job was canceled?

No. A timeout means the client stopped waiting for a response. It does not guarantee that the remote service rejected or canceled the submission. Check for a recorded task ID or documented reconciliation mechanism before sending another potentially billable creation request.

## Can I safely retry a generation request?

Do not blindly retry an uncertain billable `POST` request. The examples do **not** claim support for a general `Idempotency-Key` contract. Reconcile the original outcome first and follow any current provider-specific retry guidance. Status **GET** requests and creation **POST** requests have different side effects.

## How does image editing work in the examples?

The documented image-edit example uses a multipart request to `POST /v1/images/edits`, uploads local input images using the `image[]` field, and requests `b64_json` output. The code includes guardrails for accidental oversized local uploads. Actual accepted file sizes and channel constraints depend on the current API docs. Generated commercial images should be checked for packaging, text, and branding accuracy.

## Where can I check supported models and current pricing?

Use the [official API documentation](https://apicrest.com/apidoc?theme=light) and available account-side model/channel catalog. This repository intentionally does **not** publish a price ranking or promise to be the cheapest provider. Examples may use model IDs that change or become unavailable over time.

## How is API usage billed? Are free credits or refunds guaranteed?

Calls may incur charges under current account and provider terms. The example repository cannot verify account-specific free credits, refunds, billing settlement rules, or pricing. Check your account and official terms before running a live request. Never infer a refund simply because a request timed out.

## Are there verified latency, uptime, or benchmark results?

This example repository has **no independently verified paid model benchmarks or production uptime studies**. Its GitHub Actions checks validate only local syntax and response handling. Avoid interpreting passing CI tests as proof of live API quality or availability.

## How do I troubleshoot authentication, failed requests, or missing output?

See [API integration troubleshooting](TROUBLESHOOTING.md). For a reproducible public documentation gap, open a [sanitized integration question](https://github.com/yanbo0520/apicrest-developer-examples/issues/new/choose) without API keys, bearer headers, private user data, billing identifiers, or confidential content.

## Can I share feedback about a workflow I'm building?

Yes. Tell us the application type, preferred language (Python, Node.js, etc.), and what blocks your integration in our [public feedback discussion](https://github.com/yanbo0520/apicrest-developer-examples/issues/1). Don't publish secrets or user information.

---

**Related:** [API Crest website](https://apicrest.com/?utm_source=github&utm_medium=faq&utm_campaign=developer_discovery) · [Public documentation](https://apicrest.com/apidoc?theme=light) · [Developer examples](../README.md)

*Disclosure: This FAQ is maintained by the API Crest project. It is an affiliated explanation of publicly documented integration examples, not an independent review or endorsement.*
