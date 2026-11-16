# Boston 311 Data Explorer

An interactive **Streamlit dashboard** for exploring Boston 311 service requests, alongside a beginner-friendly Python command-line data project.

## Online dashboard

The dashboard is prepared for deployment to [Streamlit Community Cloud](https://share.streamlit.io/). A live app URL will be added after deployment.

**How to use:** Download a CSV export from the [City of Boston 311 open-data portal](https://data.boston.gov/dataset/311-service-requests), open the dashboard, and upload the CSV in the sidebar. The dashboard does not automatically download current data.

The large 2026 CSV is intentionally excluded from GitHub. If you have the file locally at `data/boston_311_2026.csv`, the dashboard loads it automatically unless another CSV is uploaded.

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
4. Deploy, then upload a CSV from the sidebar.
5. Copy the live app URL into this README and your GitHub repository description.

**Note:** The free hosting service has resource limits. Very large CSV uploads may require a smaller export or a hosted data pipeline.

## Data and attribution

`data/sample_requests.csv` contains **fictional practice records**, not official City of Boston requests. The dashboard only displays real Boston 311 data when the user supplies a corresponding official CSV export. This project is not affiliated with the City of Boston.

## AI assistance

The starter project and dashboard improvements were developed with AI assistance. The project is a learning portfolio; the author should review and understand the code, run tests, and validate results before describing the implementation independently.
