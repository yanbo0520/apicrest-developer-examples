"""Purely offline checks using illustrative numbers, not actual provider prices."""

import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "examples" / "python"))
from cost_per_accepted_output import format_report, parse_rows, summarize


class OfflineCostTests(unittest.TestCase):
    def test_counts_charged_failures_and_manual_acceptance(self):
        summary = summarize([
            ("A", "test", Decimal("0.02"), True),
            ("A", "test", Decimal("0.02"), False),
            ("A", "test", Decimal("0"), False),
        ])
        a = summary[("A", "test")]
        self.assertEqual(a["attempts"], 3)
        self.assertEqual(a["accepted"], 1)
        self.assertEqual(a["charged_usd"], Decimal("0.04"))
        self.assertIn("0.0400", format_report(summary))

    def test_zero_accepted_outputs_never_divides_by_zero(self):
        summary = summarize([("A", "test", Decimal("0.01"), False)])
        self.assertIn("N/A (0 accepted)", format_report(summary))

    def test_rejects_bad_or_negative_cost(self):
        for charge in ("bad", "-0.01", "NaN", "Infinity"):
            with self.subTest(charge=charge):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "attempts.csv"
                    path.write_text(
                        "provider,model,charged_usd,accepted\nA,m," + charge + ",true\n",
                        encoding="utf-8",
                    )
                    with self.assertRaises(ValueError):
                        parse_rows(path)

    def test_reads_illustrative_csv(self):
        filename = Path(__file__).parents[1] / "examples" / "data" / "illustrative_image_attempts.csv"
        rows = parse_rows(filename)
        self.assertEqual(len(rows), 6)
        sums = summarize(rows)
        self.assertEqual(sums[("Example-A", "synthetic-model-A")]["accepted"], 2)
        self.assertEqual(sums[("Example-B", "synthetic-model-B")]["charged_usd"], Decimal("0.12"))


if __name__ == "__main__":
    unittest.main()
