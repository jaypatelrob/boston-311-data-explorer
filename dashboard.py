from pathlib import Path
from urllib.request import urlopen

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Boston 311 Data Explorer", page_icon="🏙️", layout="wide")
st.title("🏙️ Boston 311 Data Explorer")
st.caption("Explore Boston 311 service requests with interactive filters and charts.")

LOCAL_DATA = Path(__file__).parent / "data" / "boston_311_2026.csv"
REMOTE_DATA_URL = "https://data.boston.gov/dataset/8048697b-ad64-4bfc-b090-ee00169f2323/resource/1a0b420d-99f1-4887-9851-990b2a5a6e17/download/tmprq19sfgh.csv"
COLUMNS = ["case_enquiry_id", "open_dt", "case_status", "type", "neighborhood"]

@st.cache_data(show_spinner="Reading service requests...")
def load_data(source):
    df = pd.read_csv(source, usecols=COLUMNS, low_memory=False)
    df["open_dt"] = pd.to_datetime(df["open_dt"], errors="coerce")
    for col in ["neighborhood", "type", "case_status"]:
        df[col] = df[col].fillna("Unknown").astype(str)
    return df

@st.cache_data(ttl=86400, show_spinner="Downloading official Boston 311 data (first load may take a minute)...")
def load_public_data():
    with urlopen(REMOTE_DATA_URL, timeout=120) as response:
        return load_data(response)

st.sidebar.header("Data source")
uploaded = st.sidebar.file_uploader("Upload Boston 311 CSV", type=["csv"], help="Use a CSV exported from Boston's 311 open-data portal.")
if uploaded is not None:
    source = uploaded
    st.info("Showing data from your uploaded CSV.")
elif LOCAL_DATA.exists():
    source = LOCAL_DATA
    st.info("Showing the locally available 2026 Boston 311 dataset.")
else:
    source = None

try:
    if source is None:
        df = load_public_data()
        st.info("Showing automatically loaded City of Boston 2026 service requests. You can upload a different CSV in the sidebar.")
    else:
        df = load_data(source)
except (ValueError, pd.errors.ParserError, UnicodeError, OSError, TimeoutError) as exc:
    st.error("Unable to load the Boston 311 dataset. Try refreshing or uploading a CSV in the sidebar.")
    st.caption(str(exc))
    st.stop()

st.sidebar.header("Filters")
neighborhoods = ["All"] + sorted(df["neighborhood"].unique().tolist())
statuses = ["All"] + sorted(df["case_status"].unique().tolist())
selected_neighborhood = st.sidebar.selectbox("Neighborhood", neighborhoods)
selected_status = st.sidebar.selectbox("Request Status", statuses)

filtered = df
if selected_neighborhood != "All":
    filtered = filtered[filtered["neighborhood"] == selected_neighborhood]
if selected_status != "All":
    filtered = filtered[filtered["case_status"] == selected_status]

open_count = filtered["case_status"].str.casefold().eq("open").sum()
closed_count = filtered["case_status"].str.casefold().eq("closed").sum()
c1, c2, c3 = st.columns(3)
c1.metric("Total Requests", f"{len(filtered):,}")
c2.metric("Open Requests", f"{open_count:,}")
c3.metric("Closed Requests", f"{closed_count:,}")

st.divider()
st.subheader("Most Common Service Requests")
st.bar_chart(filtered["type"].value_counts().head(15))
st.subheader("Requests by Neighborhood")
st.bar_chart(filtered["neighborhood"].value_counts().head(15))
st.subheader("Monthly Request Trends")
monthly = filtered.dropna(subset=["open_dt"]).set_index("open_dt").resample("MS").size()
st.line_chart(monthly)
st.subheader("Service Request Records")
st.dataframe(filtered.head(1000), width="stretch")
st.caption("Source: City of Boston 311 public data when an official export is supplied. Counts reflect the loaded file and selected filters.")
