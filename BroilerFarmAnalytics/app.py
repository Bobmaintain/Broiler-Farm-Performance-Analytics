from pathlib import Path

import pandas as pd
import streamlit as st

from src.db import initialize_database, replace_records, fetch_flock_records, list_flocks
from src.metrics import add_performance_metrics, validate_records

ROOT = Path(__file__).parent
SAMPLE_FILE = ROOT / "data" / "sample_daily_records.csv"
DB_FILE = ROOT / "data" / "farm_analytics.db"

st.set_page_config(page_title="Broiler Farm Analytics", page_icon="🐔", layout="wide")
st.title("🐔 Broiler Farm Performance Analytics")
st.caption("A portfolio-ready demonstration of Python, SQL and agricultural data analytics.")

initialize_database(DB_FILE)

with st.sidebar:
    st.header("Data source")
    uploaded_file = st.file_uploader("Upload daily farm records (CSV)", type=["csv"])
    initial_chick_weight = st.number_input(
        "Initial chick weight (kg)", min_value=0.001, max_value=0.2,
        value=0.04, step=0.005, format="%.3f"
    )
    st.caption("The sample dataset is synthetic. Replace it with authorised farm data for real analysis.")

if uploaded_file is not None:
    try:
        incoming = pd.read_csv(uploaded_file)
        errors = validate_records(incoming)
        if errors:
            st.error("The uploaded file has data-quality issues:")
            for error in errors:
                st.write(f"- {error}")
            st.stop()
        replace_records(incoming, DB_FILE)
        st.success(f"Imported {len(incoming):,} records into the local SQLite database.")
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()
else:
    if not DB_FILE.exists() or not list_flocks(DB_FILE):
        sample = pd.read_csv(SAMPLE_FILE)
        replace_records(sample, DB_FILE)

flocks = list_flocks(DB_FILE)
if not flocks:
    st.warning("No flock records found. Upload a valid CSV file.")
    st.stop()

selected_flock = st.sidebar.selectbox("Select flock", flocks)
records = fetch_flock_records(selected_flock, DB_FILE)

if records.empty:
    st.info("No records available for this flock.")
    st.stop()

records["date"] = pd.to_datetime(records["date"])
records = records.sort_values("date")
metrics = add_performance_metrics(records, initial_chick_weight)
latest = metrics.iloc[-1]

st.subheader(f"Flock: {selected_flock}")
st.caption(f"Reporting period: {metrics['date'].min():%d %b %Y} – {metrics['date'].max():%d %b %Y}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Birds currently alive", f"{int(latest['live_birds']):,}")
c2.metric("Cumulative mortality", f"{int(latest['cumulative_mortality']):,}")
c3.metric("Average live weight", f"{latest['avg_weight_kg']:.2f} kg")
if pd.notna(latest["fcr"]):
    c4.metric("Estimated cumulative FCR", f"{latest['fcr']:.2f}")
else:
    c4.metric("Estimated cumulative FCR", "Not available")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Average bird weight")
    st.line_chart(metrics.set_index("date")["avg_weight_kg"])

with right:
    st.subheader("Daily feed consumption")
    st.bar_chart(metrics.set_index("date")["feed_kg"])

left, right = st.columns(2)
with left:
    st.subheader("Cumulative mortality")
    st.line_chart(metrics.set_index("date")["cumulative_mortality"])

with right:
    st.subheader("Estimated cumulative FCR")
    fcr_data = metrics.set_index("date")["fcr"].dropna()
    if not fcr_data.empty:
        st.line_chart(fcr_data)
    else:
        st.info("FCR cannot be calculated until liveweight gain is positive.")

st.subheader("Cost and production indicators")
cost1, cost2, cost3 = st.columns(3)
cost1.metric("Cumulative feed cost", f"{metrics['cumulative_feed_cost_kwd'].iloc[-1]:,.3f} KWD")
cost2.metric("Cumulative other cost", f"{metrics['cumulative_other_cost_kwd'].iloc[-1]:,.3f} KWD")
cost3.metric("Total recorded cost", f"{metrics['cumulative_total_cost_kwd'].iloc[-1]:,.3f} KWD")

st.subheader("Daily records")
display_cols = [
    "date", "birds_placed", "live_birds", "feed_kg", "avg_weight_kg",
    "mortality_count", "feed_cost_kwd", "other_cost_kwd", "fcr"
]
st.dataframe(metrics[display_cols], use_container_width=True, hide_index=True)

csv_output = metrics.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download analysed flock data (CSV)",
    data=csv_output,
    file_name=f"{selected_flock.lower().replace(' ', '_')}_analysis.csv",
    mime="text/csv",
)

with st.expander("Data dictionary and calculation notes"):
    st.markdown("""
    - **Live birds:** current number of live birds reported for that date.
    - **Cumulative mortality:** sum of daily mortality records.
    - **Estimated cumulative FCR:** cumulative feed consumed divided by estimated liveweight gain.
    - **Estimated liveweight gain:** current flock live biomass minus starting chick biomass.
    - **Costs:** cumulative feed and other costs recorded in KWD.

    FCR is an estimate based on the supplied daily snapshots. For commercial reporting,
    reconcile placements, transfers, culls, sales, feed wastage and weighing procedures.
    """)
