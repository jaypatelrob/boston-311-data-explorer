# Boston 311 Data Explorer

An interactive **Streamlit dashboard** for exploring Boston 311 service requests, alongside a beginner-friendly Python command-line data project.

## Online dashboard

**[Launch the live Boston 311 dashboard](https://boston-311-data-explorer.streamlit.app/)** — a public Streamlit app displaying a default sample of 20,000 service requests from the 2026 Boston 311 CSV.

**How to use:** Open the live app to explore the bundled 20,000-record sample immediately. You can also upload a compatible CSV exported from the [City of Boston 311 open-data portal](https://data.boston.gov/dataset/311-service-requests) to analyze a different or larger set of records. The default sample is a snapshot, not live or exhaustive citywide data.

The full 2026 CSV is intentionally excluded from GitHub. The smaller `data/sample_311.csv` is committed to the repo to make the deployed app usable without an upload. If you have the full file locally at `data/boston_311_2026.csv`, the dashboard loads it automatically unless another CSV is uploaded.

### Dashboard features
- Filter by neighborhood and case status.
- View total, open, and closed requests.
- Explore request types, neighborhood counts, and monthly trends.
- Inspect up to 1,000 filtered records.

The uploaded CSV must contain `case_enquiry_id`, `open_dt`, `case_status`, `type`, and `neighborhood`.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run dashboard.py
```

For the original command-line explorer and tests:

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

The command-line explorer expects a `category` column, and optionally `neighborhood` and `status` for filters. These column names differ from the official Boston 311 export used by the dashboard.

## Deploy to Streamlit Community Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub.
2. Create a new app from repository `jaypatelrob/boston-311-data-explorer`.
3. Select branch `main` and entrypoint `dashboard.py`.
4. Deploy. The bundled sample should appear automatically; use the sidebar to upload another CSV if desired.
5. The published app is at https://boston-311-data-explorer.streamlit.app/.

**Note:** The free hosting service has resource limits. Very large CSV uploads may require a smaller export or a hosted data pipeline.

## Data and attribution

`data/sample_requests.csv` contains **fictional practice records**, not official City of Boston requests. The dashboard's default 20,000-row sample is derived from a downloaded 2026 Boston 311 CSV export. It is not the full dataset, and its figures should not be presented as citywide totals. This project is not affiliated with the City of Boston.

## AI assistance

The starter project and dashboard improvements were developed with AI assistance. The project is a learning portfolio; the author should review and understand the code, run tests, and validate results before describing the implementation independently.
