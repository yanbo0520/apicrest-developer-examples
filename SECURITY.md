# Security policy

These scripts make potentially billable API requests only when a developer explicitly passes `--run` and supplies a private `APICREST_API_KEY` environment variable. Do not commit or post credentials, content containing personal data, or full request/response logs. Avoid storing source and generated images in public repositories unless you have permission.

For vulnerabilities concerning API Crest's hosted service, use the platform's official support/contact channel found on [apicrest.com](https://apicrest.com/) and avoid publishing exploit details or credentials. This project does not claim a special security contact email or formal bug bounty program.

There is no documented generic idempotency key for the shown billable POSTs. For lost connections, record any task ID, reconcile status/cost where documented, and do **not** blindly resubmit.