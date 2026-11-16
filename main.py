"""Command-line summary of 311-style CSV records.

The bundled dataset is fictional; supply an official CSV to analyze real records.
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

DEFAULT_CSV = Path(__file__).parent / "data" / "sample_requests.csv"


def load_requests(csv_path):
    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "category" not in reader.fieldnames:
            raise ValueError("CSV must have a 'category' column.")
        return list(reader)


def filter_requests(requests, neighborhood=None, status=None):
    """Filter rows case-insensitively; require columns for requested filters."""
    filtered = list(requests)
    available_columns = set(filtered[0]) if filtered else set()
    for column, value in (("neighborhood", neighborhood), ("status", status)):
        if value is None:
            continue
        if filtered and column not in available_columns:
            raise ValueError(f"CSV must have a '{column}' column for --{column}.")
        filtered = [
            row for row in filtered
            if (row.get(column) or "").strip().casefold() == value.strip().casefold()
        ]
    return filtered


def count_by_category(requests):
    counts = Counter()
    for request in requests:
        category = (request.get("category") or "").strip()
        counts[category or "Uncategorized"] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Summarize 311 service requests.")
    parser.add_argument("csv_file", nargs="?", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--neighborhood", help="Filter by neighborhood (exact match)")
    parser.add_argument("--status", help="Filter by status (exact match)")
    args = parser.parse_args()
    try:
        requests = load_requests(args.csv_file)
        requests = filter_requests(requests, args.neighborhood, args.status)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not analyze CSV: {error}\n")

    counts = count_by_category(requests)
    print("311 Service Request Summary")
    print("=" * 27)
    print(f"Total requests: {len(requests)}")
    print("\nRequests by category:")
    for category, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
