# Developer outreach attribution plan

**Status:** This is a tracking *plan*, not evidence that attribution is live. GitHub, DEV and Hashnode exposure cannot be connected to registrations or revenue until API Crest records campaign metadata and downstream account events.

## Reusable links

Use distinct `utm_source` values for each publishing channel. The link format is a standard URL query string; whether the website currently records it is **not verified**.

| Channel | Example campaign URL |
| --- | --- |
| GitHub | https://apicrest.com/?utm_source=github&utm_medium=referral&utm_campaign=developer_examples |
| DEV Community | https://apicrest.com/?utm_source=devto&utm_medium=technical_article&utm_campaign=developer_examples |
| Hashnode | https://apicrest.com/?utm_source=hashnode&utm_medium=technical_article&utm_campaign=developer_examples |

Keep documentation reference links such as [the public API docs](https://apicrest.com/apidoc?theme=light) intact. Don't append tracking strings to API endpoints, billing requests, or authentication links. Avoid placing any personal information or secrets in UTM fields.

## Events needed for a credible funnel

1. **Landing visit:** Record campaign source, timestamp, visited route, and anonymous session identifier *only when permitted by the site's privacy and consent configuration*. Exclude API keys, bearer headers, full query strings containing sensitive fields and private prompts.
2. **Account creation:** Carry source attribution into the registration event if the session can lawfully be linked.
3. **First successful API call:** Count an actual completed, authorized invocation, not simply a copied example.
4. **First settled payment:** Count a confirmed paid transaction, not balance page views or attempted top-ups.

Use one consistent definition per event and deduplicate appropriately. Prefer aggregate reporting where possible and follow relevant privacy/consent requirements.

## Weekly report template

| Channel | Clicks / visits | Registrations | First successful calls | Paying users |
| --- | --- | --- | --- | --- |
| github | not connected | not connected | not connected | not connected |
| devto | not connected | not connected | not connected | not connected |
| hashnode | not connected | not connected | not connected | not connected |

**Do not put zeros in the table for unavailable measurements.** Missing tracking is `not connected`, not evidence that no one visited or converted.

## Publication safeguards

- No fabricated traffic, leads, tests or revenue.
- One high-quality DEV post at a time; avoid duplicated copy and unsolicited messages.
- Disclose API Crest affiliation in community posts.
- Use [API Crest docs](https://apicrest.com/apidoc?theme=light) to verify endpoint/model details before publication.
- Never collect keys from developers or expose account/usage data in public reports.
