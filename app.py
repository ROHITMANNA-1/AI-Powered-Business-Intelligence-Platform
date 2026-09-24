"""AI Analyst Streamlit entry point."""

import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from typing import Any

from src.ai_analyst import answer_question
from src.data_cleaning import clean_dataframe
from src.data_loader import load_dataframe
from src.data_profiling import profile_dataframe
from src.eda import grouped_summary, revenue_trend_figure
from src.insight_engine import generate_insights
from src.kpis import calculate_kpis
from src.report_generator import build_markdown_report, build_pdf_report
from src.schema import detect_schema

load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent


st.set_page_config(
    page_title="AI Analyst",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("AI Analyst")
st.caption("AI-powered descriptive and diagnostic business intelligence")

with st.sidebar:
    st.header("Project status")
    st.success("Application ready")
    st.write("Dataset: UCI Online Retail")
    st.write("License: CC BY 4.0")

starter_path = PROJECT_ROOT / "data" / "raw" / "uci-online-retail" / "Online Retail.xlsx"
use_starter = st.checkbox("Use downloaded UCI Online Retail dataset", value=starter_path.exists())
uploaded_file = st.file_uploader("Upload a CSV or Excel dataset", type=["csv", "xlsx", "xls"])
if uploaded_file is None and not use_starter:
    st.info("Upload a dataset to begin analysis. The starter UCI Online Retail file is supported.")
    st.markdown("**Supported analysis:** revenue, orders, customers, products, countries, and time trends.")
    st.markdown("**Unavailable unless supplied:** profit, category, shipping, delivery, and cost metrics.")
    st.stop()

try:
    source = starter_path if use_starter and uploaded_file is None else uploaded_file
    source_name = starter_path.name if uploaded_file is None else uploaded_file.name
    source_bytes = source.read_bytes() if isinstance(source, Path) else source.getvalue()
except Exception as error:
    st.error(f"Could not load the file: {error}")
    st.stop()

@st.cache_data(show_spinner="Preparing dataset...")
def prepare_dataset(source_bytes: bytes, source_name: str, remove_duplicates: bool, remove_cancelled: bool, fill_numeric_missing: bool):
    raw = load_dataframe(source_bytes, source_name)
    return clean_dataframe(
        raw,
        remove_duplicates=remove_duplicates,
        remove_cancelled=remove_cancelled,
        fill_numeric_missing=fill_numeric_missing,
    )


with st.sidebar:
    remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
    remove_cancelled = st.checkbox("Remove cancelled invoices", value=True)
    fill_numeric_missing = st.checkbox("Fill missing numeric values with median", value=False)

dataframe, cleaning_report = prepare_dataset(
    source_bytes,
    source_name,
    remove_duplicates,
    remove_cancelled,
    fill_numeric_missing,
)
profile = profile_dataframe(dataframe)
kpis = calculate_kpis(dataframe)

st.caption(f"Loaded {len(dataframe):,} cleaned rows from {source_name}")
detected_schema = detect_schema(list(dataframe.columns))
with st.expander("Detected dataset fields"):
    st.write("The analyst maps recognized headings to internal metrics and keeps other headings available for exploration.")
    st.json(detected_schema)
tabs = st.tabs(["Overview", "Data quality", "Explore", "AI analyst", "Insights", "Report"])

with tabs[0]:
    st.subheader("Key performance indicators")
    cards = [("Revenue", kpis["total_revenue"], "£{:,.2f}"), ("Orders", kpis["orders"], "{:,.0f}"), ("Average order value", kpis["average_order_value"], "£{:,.2f}"), ("Customers", kpis["customers"], "{:,.0f}")]
    columns = st.columns(len(cards))
    for column, (label, value, formatter) in zip(columns, cards):
        column.metric(label, "Unavailable" if value is None else formatter.format(value))
    st.caption("Revenue is Quantity multiplied by UnitPrice. Profit margin, discount, and delivery KPIs are unavailable in the selected source dataset.")

with tabs[1]:
    st.subheader("Data quality and cleaning summary")
    st.dataframe(profile["numeric_summary"], use_container_width=True, hide_index=True)
    st.write(f"Rows: {profile['rows']:,} | Columns: {profile['columns']:,} | Duplicate rows remaining: {profile['duplicate_rows']:,}")
    st.write("Issues detected:")
    for issue in profile["quality_issues"] or ["No configured quality issues detected."]:
        st.write(f"- {issue}")
    st.write("Cleaning changes:")
    st.write(f"- Duplicate rows removed: {cleaning_report.duplicate_rows_removed:,}")
    st.write(f"- Cancelled rows removed: {cleaning_report.cancelled_rows_removed:,}")
    st.write(f"- Missing numeric values filled: {cleaning_report.missing_values_filled:,}")
    st.download_button("Download cleaned CSV", dataframe.to_csv(index=False).encode("utf-8"), "cleaned_data.csv", "text/csv")

with tabs[2]:
    st.subheader("Exploratory analysis")
    if "revenue" in dataframe:
        st.plotly_chart(revenue_trend_figure(dataframe), use_container_width=True)
    dimension_options = [
        column for column in dataframe.select_dtypes(exclude="number").columns
        if column not in {"date", "invoice_date", "order_date"}
    ]
    dimension = st.selectbox("Compare revenue by", dimension_options or ["No categorical field available"])
    if dimension != "No categorical field available":
        st.dataframe(grouped_summary(dataframe, dimension), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Ask the AI analyst")
    question = st.text_input("Business question", placeholder="What was the total revenue?")
    if st.button("Analyze question", type="primary") and question:
        try:
            response = answer_question(question, dataframe)
            st.subheader("Answer")
            st.success(response["answer"])
            st.code(response["sql"], language="sql")
            st.dataframe(response["result"], use_container_width=True, hide_index=True)
        except Exception as error:
            st.warning(f"The analyst could not answer this question: {error}")

with tabs[4]:
    st.subheader("Automated business insights")
    for insight in generate_insights(dataframe):
        with st.expander(insight["title"], expanded=True):
            st.write(f"**Supporting metric:** {insight['supporting_metric']}")
            st.write(f"**Comparison:** {insight['comparison']}")
            st.write(f"**Interpretation:** {insight['interpretation']}")
            st.write(f"**Further investigation:** {insight['next_step']}")

with tabs[5]:
    st.subheader("Download analytical report")
    insights = generate_insights(dataframe)
    markdown = build_markdown_report(profile, kpis, insights)
    st.download_button("Download Markdown report", markdown, "ai_analyst_report.md", "text/markdown")
    st.download_button("Download PDF report", build_pdf_report(markdown), "ai_analyst_report.pdf", "application/pdf")
    st.markdown(markdown)
