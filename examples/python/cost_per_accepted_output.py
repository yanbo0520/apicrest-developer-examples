"""Offline cost-per-accepted-output analysis from your OWN recorded usage.

Never calls an API and does not import project API credentials.
Input CSV columns: provider,model,charged_usd,accepted
'accepted' is the user's own quality judgment (true/false), not merely HTTP success.
See illustrative input under examples/data/. This is not a pricing benchmark.
"""

import argparse
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUMNS = {"provider", "model", "charged_usd", "accepted"}
TRUE = {"true", "yes", "1"}
FALSE = {"false", "no", "0"}


def parse_rows(path):
    """Return validated (provider, model, charged_usd, accepted) records."""
    rows = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not COLUMNS.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must contain provider,model,charged_usd,accepted columns")
        for line, row in enumerate(reader, start=2):
            provider, model = (row.get("provider") or "").strip(), (row.get("model") or "").strip()
            status = (row.get("accepted") or "").strip().lower()
            if not provider or not model or status not in TRUE | FALSE:
                raise ValueError(f"Line {line}: require nonempty provider/model and accepted=true|false")
            try:
                charge = Decimal((row.get("charged_usd") or "").strip())
            except InvalidOperation as exc:
                raise ValueError(f"Line {line}: charged_usd is not a decimal") from exc
            if not charge.is_finite() or charge < 0:
                raise ValueError(f"Line {line}: charged_usd must be finite and >= 0")
            rows.append((provider, model, charge, status in TRUE))
    if not rows:
        raise ValueError("CSV contains no attempts")
    return rows


def summarize(rows):
    """Aggregate observed charges and manually accepted outputs by provider/model."""
    buckets = defaultdict(lambda: {"attempts": 0, "accepted": 0, "charged_usd": Decimal("0")})
    for provider, model, charge, accepted in rows:
        bucket = buckets[(provider, model)]
        bucket["attempts"] += 1
        bucket["accepted"] += int(accepted)
        bucket["charged_usd"] += charge
    return dict(sorted(buckets.items()))


def format_report(summary):
    lines = [
        "| Provider | Model | Attempts | Accepted | Recorded charge (USD) | USD per accepted output |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for (provider, model), data in summary.items():
        count = data["accepted"]
        cost = data["charged_usd"]
        per_accepted = f"{cost / count:.4f}" if count else "N/A (0 accepted)"
        lines.append(
            f"| {provider.replace('|', '/')} | {model.replace('|', '/')} | "
            f"{data['attempts']} | {count} | {cost:.4f} | {per_accepted} |"
        )
    lines.append("")
    lines.append("Reported charges are INPUT DATA, not verified invoices, live prices, or benchmark results.")
    lines.append("Accepted counts require independent human evaluation; small samples are not representative.")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Analyze recorded image/API attempts OFFLINE; no API calls.")
    p.add_argument("csv_path", type=Path, help="Your sanitized CSV with provider,model,charged_usd,accepted")
    args = p.parse_args()
    try:
        print(format_report(summarize(parse_rows(args.csv_path))))
    except (OSError, ValueError) as err:
        p.error(str(err))


if __name__ == "__main__":
    main()
