# Boston 311 Data Explorer

A beginner-friendly **Python command-line data project** that summarizes 311-style service requests by category, with optional neighborhood and status filters.

> **Important:** The included `data/sample_requests.csv` contains **fictional practice records**, not official City of Boston requests. This is a learning project, not a City of Boston product.

## Features
- Load CSV data using Python's standard library.
- Count service requests by category, including missing categories.
- Filter records by neighborhood and/or status when the input CSV contains those columns.
- Run automated unit tests.
- Display helpful errors for missing required columns.

## Run locally
Requires Python 3. No third-party packages.

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

To analyze a CSV with a `category` column:

```bash
python3 main.py path/to/requests.csv
```

To filter a CSV that **also contains** `neighborhood` and `status` columns:

```bash
python3 main.py path/to/requests.csv --neighborhood Dorchester --status Open
```

Column names must be exactly `category`, `neighborhood`, and `status` as applicable. Filtering is case-insensitive, with exact text matching. The bundled fictional CSV may not contain optional filter columns. If your dataset uses different column names, rename them or adapt the loader.

## Project status
- [x] CSV category summaries
- [x] Optional neighborhood and status filtering (proposed v0.2)
- [x] Automated tests
- [ ] Import and document **real** data from the [Boston 311 open-data portal](https://data.boston.gov/dataset/311-service-requests)
- [ ] Visualizations and dashboard
- [ ] SQLite storage

## What this demonstrates
Basic Python programming, CSV parsing, functions, dictionaries, command-line interfaces, input validation, and unit testing. It does **not** yet demonstrate a deployed application, real-world dataset analysis, or advanced software engineering.

## AI assistance and attribution
The original starter project and these proposed enhancements were generated with AI assistance. The repository is intended as a learning project; understanding, validating, and extending the code is the next step. Do not describe generated features as independently implemented until you have worked through them yourself.
