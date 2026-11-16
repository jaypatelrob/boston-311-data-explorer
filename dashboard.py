from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Boston 311 Data Explorer", page_icon="🏙️", layout="wide")
st.title("🏙️ Boston 311 Data Explorer")
st.caption("Explore Boston 311 service requests with interactive filters and charts.")

LOCAL_DATA = Path(__file__).parent / "data" / "boston_311_2026.csv"
COLUMNS = ["case_enquiry_id", "open_dt", "case_status", "type", "neighborhood"]

@st.cache_data(show_spinner="Reading service requests...")
def load_data(source):
    df = pd.read_csv(source, usecols=COLUMNS, low_memory=False)
    df["open_dt"] = pd.to_datetime(df["open_dt"], errors="coerce")
    for col in ["neighborhood", "type", "case_status"]:
        df[col] = df[col].fillna("Unknown").astype(str)
    return df

st.sidebar.header("Data source")
uploaded = st.sidebar.file_uploader("Upload Boston 311 CSV", type=["csv"], help="Use a CSV exported from Boston's 311 open-data portal.")
if uploaded is not None:
    source = uploaded
    st.info("Showing data from your uploaded CSV.")
elif LOCAL_DATA.exists():
    source = LOCAL_DATA
    st.info("Showing the locally available 2026 Boston 311 dataset.")
else:
    st.info("To explore service requests, upload a Boston 311 CSV using the sidebar.")
    st.markdown("Get a dataset from the [City of Boston 311 open-data portal](https://data.boston.gov/dataset/311-service-requests).")
    st.caption("The public repository intentionally does not contain the large 2026 CSV.")
    st.stop()

try:
    df = load_data(source)
except (ValueError, pd.errors.ParserError, UnicodeError, OSError) as exc:
    st.error(f"Unable to read this CSV. It must contain: {', '.join(COLUMNS)}.")
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
