# Boston 311 Data Explorer

A beginner-friendly **Python command-line project** for summarizing 311-style service requests by category. This project is a learning portfolio for programming, data analysis, and software testing.

> **Data note:** The included `data/sample_requests.csv` is entirely **fictional practice data**, not real Boston 311 case records. The project is not affiliated with the City of Boston.

## What works in version 0.1

- Loads service requests from a CSV file using Python's built-in `csv` module.
- Counts requests in each category.
- Prints total requests and category counts in descending order.
- Handles blank categories and gives a useful error if the CSV has no `category` header.
- Includes four automated unit tests.

## Quick start (macOS)

1. Install Python 3 if you don't already have it. Check using `python3 --version` in Terminal.
2. Download or clone this project and open the project folder in Terminal.
3. Run:

   ```bash
   python3 main.py
   ```

   Expected output using the fictional sample data:

   ```text
   311 Service Request Summary
   ===========================
   Total requests: 12

   Requests by category:
     Street Cleaning: 4
     Trash Collection: 4
     Pothole: 3
     Street Lighting: 1
   ```

4. Run the tests:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

This first version uses only Python's standard library; **no packages to install**.

### Analyze a different CSV

Run `python3 main.py path/to/file.csv`. Your CSV must have a header called `category`. Official datasets sometimes use different column names, so you'll need to inspect the data and adapt the program before importing them.

## File map

```text
boston-311-data-explorer/
├── README.md                 # Project explanation and instructions
├── main.py                   # CSV reader and category summary
├── data/
│   └── sample_requests.csv  # Fictional records for practice
├── tests/
│   └── test_main.py          # Automated tests
└── .gitignore                # Files Git should not track
```

## Learning roadmap

- [x] Version 0.1: CSV loading, basic counting, tests.
- [ ] Version 0.2: Add filtering by neighborhood and open/closed status.
- [ ] Version 0.3: Explore **real** data from the [City of Boston 311 open-data portal](https://data.boston.gov/dataset/311-service-requests); document the dataset's actual fields and attribution.
- [ ] Version 0.4: Save and query records in SQLite.
- [ ] Version 0.5: Create charts and a simple dashboard.

## Skills demonstrated (currently)

Python basics, CSV input, dictionaries, `collections.Counter`, command-line interfaces, and automated testing with `unittest`.

## About

An independent learning project developed for an undergraduate engineering student's software/data portfolio. Built incrementally so each feature can be explained and demonstrated in an interview.

## Development assistance

The initial starter code, sample data, tests, and documentation were generated with ChatGPT assistance. This repository is being used for hands-on learning and incremental development.
