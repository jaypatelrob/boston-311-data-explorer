"""Simple tests for the first version of the 311 explorer."""

import tempfile
import unittest
from pathlib import Path

from main import count_by_category, load_requests


class Test311Explorer(unittest.TestCase):
    def test_count_by_category(self):
        rows = [
            {"category": "Pothole"},
            {"category": "Trash Collection"},
            {"category": "Pothole"},
        ]
        self.assertEqual(count_by_category(rows)["Pothole"], 2)
        self.assertEqual(count_by_category(rows)["Trash Collection"], 1)

    def test_missing_category_is_grouped(self):
        rows = [{"category": " "}, {}]
        self.assertEqual(count_by_category(rows)["Uncategorized"], 2)

    def test_load_requests(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "requests.csv"
            path.write_text("case_id,category\n1,Pothole\n", encoding="utf-8")
            rows = load_requests(path)
            self.assertEqual(rows[0]["category"], "Pothole")

    def test_rejects_csv_without_category_column(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.csv"
            path.write_text("case_id,status\n1,Open\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_requests(path)


if __name__ == "__main__":
    unittest.main()
