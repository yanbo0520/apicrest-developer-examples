# The AI API Timeout Problem: How to Avoid Duplicate Image and Video Jobs

**An integration guide for developers building asynchronous AI applications in Python and Node.js.**

You submit an image or video generation request. The network connection drops after 30 seconds. Your application never receives the response.

Should it automatically submit the same prompt again?

**Usually, not until you know whether the first job was created.** A timeout describes what happened to the *client's wait for a response*. It does not prove the server canceled the work.

This distinction matters when the operation creates an asynchronous task, changes external state, or can be billed.

## The ambiguity after a timeout

Consider three possible sequences:

1. The request never reached the server. No job exists.
2. The server accepted the request and created a job, but the response carrying its ID was lost.
3. The server is still working, even though your client stopped waiting.

From the client's perspective, all three can look like a timeout.

If you automatically repeat `POST /generate`, the second request might create a *new* job rather than continuing the first one. A client-side retry is not inherently an exactly-once guarantee.

### A practical rule

**Treat an uncertain creation request as an unknown outcome, not as a confirmed failure.** When supported, use an idempotency mechanism defined by the provider. If none is documented, reconcile the original request before submitting a second job.

## Separate job creation from job observation

A robust client maintains a clear difference between the two operations:

| Operation | Purpose | Typical handling |
| --- | --- | --- |
| Create a task (POST) | Ask the service to start work | Submit deliberately; avoid blind retries on ambiguous failures |
| Query task state (GET) | Find out what happened to an existing task | Retry responsibly if transiently unavailable, subject to documented limits |
| Retrieve final output | Consume a completed task | Validate the output and its permissions before use |

For the [documented API Crest asynchronous media workflow](https://apicrest.com/apidoc?theme=light), the example integration submits to `POST /v1/media/generate` and polls `GET /v1/media/status?task_id=...`.

The [Python example](https://github.com/yanbo0520/apicrest-developer-examples/blob/main/examples/python/media_async.py) and [Node.js example](https://github.com/yanbo0520/apicrest-developer-examples/blob/main/examples/node/media_async.mjs) demonstrate this separation.

These are documentation-based examples, not proof that any particular production model/channel is currently available.

## Save the task ID as soon as you receive it

After a successful submission, persist the returned task ID with the application request that initiated it.

The documentation-based examples use `task_id`. They inspect the reported status using `state` and `is_final`.

A conservative state classifier might look like this:

```python
def classify_media_job(job):
    if not isinstance(job, dict):
        return "unknown"

    state = job.get("state")
    is_final = job.get("is_final")

    if state == "success" and is_final is True:
        return "success"
    if state == "failed" and is_final is True:
        return "failed"
    if state in {"pending", "running"} and is_final is not True:
        return "pending"
    return "unknown"
```

Why explicitly handle `unknown`? Because a missing field, new state, or unexpected shape should not silently be interpreted as completion. Check the current API specification before building assumptions into production code.

When the status is pending, poll at a moderate interval. When the task is final, stop polling and handle the result. If the status endpoint becomes unavailable, retain the task ID so the user can resume investigation later.

## Polling deadline versus job cancellation

Suppose your client polls for 10 minutes and then stops.

That is a **client-side deadline**. Unless the API documents and confirms a cancellation action, the job may still be running remotely. Don't tell the end user that the provider canceled it merely because your application stopped polling.

Likewise, do not submit the same work again automatically just because the polling deadline expired.

If the provider documents callbacks, use authenticated webhooks where appropriate. Make your callback processing tolerant of repeated delivery.

## What if the submission response never arrives?

This is the most difficult case: you may have no task ID.

A safe recovery sequence is:

1. Preserve any request correlation information that the provider explicitly supports.
2. Check documented account activity, task history, or reconciliation mechanisms.
3. Look for any task identifier surfaced in an error response or response header.
4. Avoid blind duplicate submissions while the original outcome is still unknown.
5. Request clarification from the provider if a supported recovery mechanism is not documented.

The API Crest [integration notes](https://github.com/yanbo0520/apicrest-developer-examples/blob/main/docs/INTEGRATION_NOTES.md) also describe a separate image-editing flow where a response may expose an `X-Task-Id` header or `error.task_id`; its documented reconciliation route is `GET /v1/skills/task-status?task_id=...`. That flow should not be confused with async media generation.

Do **not** assume an `Idempotency-Key` header works unless your provider documents it. An unsupported header does not create exactly-once behavior by magic.

## How to test without issuing paid requests

Before making any authorized live calls, validate your request construction, status parser, and state transitions locally.

Our [API Crest developer examples](https://github.com/yanbo0520/apicrest-developer-examples) include offline tests for common failure and unknown-state cases. Those tests do not require an API key and do not call the provider:

```bash
git clone https://github.com/yanbo0520/apicrest-developer-examples.git
cd apicrest-developer-examples
python -m unittest discover -s tests -v
node --test tests/test_node_contracts.mjs
```

The example scripts deliberately require an explicit `--run` flag for real network requests. A live request may incur charges. Review the current docs and account permissions before invoking it.

## Quick answers to common questions

### Does a timed-out AI generation request mean the job failed?

**No.** It means the client did not receive a response within its wait period. The server may or may not have accepted the job.

### Is it safe to retry an asynchronous AI generation POST?

**Not automatically when the first outcome is unknown.** Use a documented idempotency or reconciliation mechanism if available.

### What should I store for image or video jobs?

The **provider-issued task ID**, the local job record, status transitions, and only the minimum operational metadata needed to debug the workflow. Do not log API keys, private inputs, or sensitive payloads.

### What is the difference between polling and re-submitting?

Polling observes an existing job using its ID. Re-submitting requests a new job. They are not interchangeable.

### Do the API Crest code samples prove production performance?

**No.** The linked examples were reviewed against public API documentation and tested offline. They do not constitute live availability, latency, or cost benchmarks.

## Developer resources

- [API Crest — product website](https://apicrest.com/?utm_source=github&utm_medium=article&utm_campaign=async_reliability)
- [API Crest API documentation](https://apicrest.com/apidoc?theme=light)
- [Python + Node.js examples](https://github.com/yanbo0520/apicrest-developer-examples)
- [Troubleshooting guide](https://github.com/yanbo0520/apicrest-developer-examples/blob/main/docs/TROUBLESHOOTING.md)
- [Share an integration question](https://github.com/yanbo0520/apicrest-developer-examples/issues/1)

*Disclosure: Published by the API Crest project. The article explains general API integration principles and links to our documentation-grounded examples; it is not an independent endorsement or a claim of benchmarked service quality.*
