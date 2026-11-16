"""Tests for CSV parsing, category counts, and optional filters."""
import tempfile
import unittest
from pathlib import Path
from main import count_by_category, filter_requests, load_requests


class Test311Explorer(unittest.TestCase):
    def test_count_by_category(self):
        rows = [{"category": "Pothole"}, {"category": "Trash"}, {"category": "Pothole"}]
        self.assertEqual(count_by_category(rows)["Pothole"], 2)

    def test_missing_category(self):
        self.assertEqual(count_by_category([{"category": " "}, {}])["Uncategorized"], 2)

    def test_load_requests(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "requests.csv"
            path.write_text("case_id,category\n1,Pothole\n", encoding="utf-8")
            self.assertEqual(load_requests(path)[0]["category"], "Pothole")

    def test_reject_missing_category(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.csv"
            path.write_text("case_id,status\n1,Open\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_requests(path)

    def test_neighborhood_filter(self):
        rows = [
            {"category": "Trash", "neighborhood": "Dorchester", "status": "Open"},
            {"category": "Pothole", "neighborhood": "Roxbury", "status": "Closed"},
        ]
        self.assertEqual(len(filter_requests(rows, neighborhood="dorchester")), 1)
        self.assertEqual(len(filter_requests(rows, status="CLOSED")), 1)
        self.assertEqual(len(filter_requests(rows, neighborhood="Roxbury", status="Open")), 0)

    def test_missing_filter_column(self):
        with self.assertRaises(ValueError):
            filter_requests([{"category": "Trash"}], status="Open")


if __name__ == "__main__":
    unittest.main()
