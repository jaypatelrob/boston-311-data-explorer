
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Boston 311 Data Explorer",
    page_icon="🏙️",
    layout="wide",
)

st.title("🏙️ Boston 311 Data Explorer")
st.caption("Explore real Boston 311 service requests from 2026.")

DATA_PATH = Path(__file__).parent / "data" / "boston_311_2026.csv"

@st.cache_data
def load_data():
    columns = [
        "case_enquiry_id",
        "open_dt",
        "case_status",
        "type",
        "neighborhood",
    ]

    df = pd.read_csv(
        DATA_PATH,
        usecols=columns,
        low_memory=False,
    )

    df["open_dt"] = pd.to_datetime(df["open_dt"], errors="coerce")
    df["neighborhood"] = df["neighborhood"].fillna("Unknown")
    df["type"] = df["type"].fillna("Unknown")
    df["case_status"] = df["case_status"].fillna("Unknown")

    return df

if not DATA_PATH.exists():
    st.error("2026 Boston 311 CSV file not found.")
    st.stop()

with st.spinner("Loading Boston 311 data..."):
    df = load_data()

st.sidebar.header("Filters")

neighborhoods = ["All"] + sorted(df["neighborhood"].unique().tolist())
selected_neighborhood = st.sidebar.selectbox(
    "Neighborhood",
    neighborhoods,
)

statuses = ["All"] + sorted(df["case_status"].unique().tolist())
selected_status = st.sidebar.selectbox(
    "Request Status",
    statuses,
)

filtered = df.copy()

if selected_neighborhood != "All":
    filtered = filtered[
        filtered["neighborhood"] == selected_neighborhood
    ]

if selected_status != "All":
    filtered = filtered[
        filtered["case_status"] == selected_status
    ]

total_requests = len(filtered)
open_requests = filtered["case_status"].str.casefold().eq("open").sum()
closed_requests = filtered["case_status"].str.casefold().eq("closed").sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Requests", f"{total_requests:,}")
col2.metric("Open Requests", f"{open_requests:,}")
col3.metric("Closed Requests", f"{closed_requests:,}")

st.divider()

st.subheader("Most Common Service Requests")
category_counts = filtered["type"].value_counts().head(15)
st.bar_chart(category_counts)

st.subheader("Requests by Neighborhood")
neighborhood_counts = filtered["neighborhood"].value_counts().head(15)
st.bar_chart(neighborhood_counts)

st.subheader("Monthly Request Trends")
monthly = (
    filtered.dropna(subset=["open_dt"])
    .set_index("open_dt")
    .resample("MS")
    .size()
)
st.line_chart(monthly)

st.subheader("Service Request Records")
st.dataframe(filtered.head(1000), width="stretch")

st.caption(
    "Source: City of Boston 311 public data. "
    "2026 is an incomplete year and records may be updated."
)


