"""A beginner-friendly command-line explorer for 311 service requests.

The included CSV contains *fictional sample records*, not official Boston 311 data.
"""

import argparse
import csv
from collections import Counter
from pathlib import Path


DEFAULT_CSV = Path(__file__).parent / "data" / "sample_requests.csv"


def load_requests(csv_path):
    """Read request rows from a CSV file into a list of dictionaries."""
    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "category" not in reader.fieldnames:
            raise ValueError("CSV must have a 'category' column.")
        return list(reader)


def count_by_category(requests):
    """Count the number of requests belonging to each category."""
    counts = Counter()
    for request in requests:
        category = (request.get("category") or "").strip()
        counts[category or "Uncategorized"] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Summarize 311 service requests from a CSV file."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to a CSV file (default: fictional sample data)",
    )
    args = parser.parse_args()

    try:
        requests = load_requests(args.csv_file)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not read CSV: {error}\n")

    counts = count_by_category(requests)
    print("311 Service Request Summary")
    print("=" * 27)
    print(f"Total requests: {len(requests)}")
    print("\nRequests by category:")
    for category, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
