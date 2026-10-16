"""Offline contract-shape tests only — zero network access or paid API calls."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "examples" / "python"))
from common import (classify_media_job, error_task_id, extract_text, require_execution)


class ContractTests(unittest.TestCase):
    def test_explicit_opt_in(self):
        with self.assertRaises(SystemExit):
            require_execution(False, {"APICREST_API_KEY": "not-a-real-key"})

    def test_missing_key_rejected(self):
        with self.assertRaises(SystemExit):
            require_execution(True, {})
        with self.assertRaises(SystemExit):
            require_execution(True, {"APICREST_API_KEY": "YOUR_API_KEY"})

    def test_key_reads_without_printing(self):
        self.assertEqual(require_execution(True, {"APICREST_API_KEY": "synthetic-example-not-real"}), "synthetic-example-not-real")

    def test_extract_text_ignores_nontext(self):
        body = {"content": [{"type": "text", "text": "hello"}, {"type": "tool_use", "id": "t1"}, {"type": "text", "text": "world"}]}
        self.assertEqual(extract_text(body), "hello\nworld")

    def test_task_id_from_error(self):
        self.assertEqual(error_task_id({"error": {"task_id": "job_synthetic"}}), "job_synthetic")
        self.assertIsNone(error_task_id({"error": "bad request"}))

    def test_media_terminal_states(self):
        self.assertEqual(classify_media_job({"state": "success", "is_final": True}), "success")
        self.assertEqual(classify_media_job({"state": "failed", "is_final": True}), "failed")
        self.assertEqual(classify_media_job({"state": "running", "is_final": False}), "pending")
        self.assertEqual(classify_media_job({"state": "success", "is_final": False}), "unknown")
        self.assertEqual(classify_media_job({"state": "new-state", "is_final": False}), "unknown")


if __name__ == "__main__":
    unittest.main()
