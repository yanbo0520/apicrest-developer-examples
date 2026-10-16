# Maintainer guide: publishing and reviewing examples

This repository belongs to the API Crest developer-examples project. Public source: [yanbo0520/apicrest-developer-examples](https://github.com/yanbo0520/apicrest-developer-examples).

## Update checklist

1. Compare model IDs, endpoint paths, parameters and billing caveats against [current API Crest docs](https://apicrest.com/apidoc?theme=light). Do not publish inferred capabilities as verified.
2. Keep examples safe by default; requests require explicit `--run` and an environment-provided credential.
3. Do not commit secrets, customer data, paid API logs, or copyrighted example images.
4. Run the **offline** checks described in [README](../README.md); the checks validate syntax and local contracts only, not the upstream service.
5. Do not add claims about price, availability, latency, success rates, or customer adoption without attributable evidence.
6. For security issues, follow [SECURITY.md](../SECURITY.md) and avoid exposing secrets in issue reports.
7. Review the diff, then publish a pull request with the documentation changes and tested commands.

## Outreach and citation

The repository is an API Crest-affiliated technical resource. When sharing it in public developer communities, disclose that relationship and answer a concrete developer need rather than spamming generic product announcements. Respect each community's rules and do not automate mass comments or direct messages.
