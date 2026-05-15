import streamlit as st
import plotly.express as px
import io, json

from src.data_loader  import load_file
from src.data_cleaner import clean_data
from src.kpi_engine   import compute_kpis
from src.ai_agent     import run_analysis

st.set_page_config(page_title="AI Business Analyst Agent", page_icon="📊", layout="wide")
st.title("📊 AI Business Analyst Agent")
st.caption("Upload a sales CSV or Excel file to get instant AI-powered insights.")

with st.sidebar:
    st.header("Options")
    show_raw  = st.checkbox("Show raw data", value=False)
    show_kpis = st.checkbox("Show KPI numbers", value=False)

uploaded_file = st.file_uploader("Upload your file", type=["csv","xlsx","xls"])

def show_results(df, kpis, insights, show_raw, show_kpis):
    st.header("Executive Summary")
    st.info(insights.get("summary","No summary."))

    st.header("Key Numbers")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Revenue",      f"${kpis.get('total_revenue',0):,.0f}")
    c2.metric("Avg Transaction",    f"${kpis.get('avg_transaction',0):,.2f}")
    c3.metric("Median Transaction", f"${kpis.get('median_transaction',0):,.2f}")
    c4.metric("Total Records",      f"{kpis.get('total_rows',0):,}")

    st.header("AI Analysis")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Insights")
        for x in insights.get("insights",[]): st.success(x)
    with col2:
        st.subheader("Risks")
        for x in insights.get("risks",[]): st.warning(x)
    with col3:
        st.subheader("Recommendations")
        for x in insights.get("recommendations",[]): st.info(x)

    st.header("Charts")
    ch1,ch2 = st.columns(2)
    with ch1:
        if "revenue_by_region" in kpis:
            fig = px.bar(x=list(kpis["revenue_by_region"].keys()),
                         y=list(kpis["revenue_by_region"].values()),
                         title="Revenue by Region",
                         color=list(kpis["revenue_by_region"].keys()))
            st.plotly_chart(fig, use_container_width=True)
    with ch2:
        if "revenue_by_product" in kpis:
            fig2 = px.pie(names=list(kpis["revenue_by_product"].keys()),
                          values=list(kpis["revenue_by_product"].values()),
                          title="Revenue by Product")
            st.plotly_chart(fig2, use_container_width=True)

    if "monthly_trend" in kpis:
        fig3 = px.line(x=list(kpis["monthly_trend"].keys()),
                       y=list(kpis["monthly_trend"].values()),
                       title="Monthly Revenue Trend", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    d1,d2 = st.columns(2)
    with d1:
        buf = io.BytesIO()
        df.to_excel(buf, index=False)
        st.download_button("Download Cleaned Data (Excel)", buf.getvalue(),
                           "cleaned_data.xlsx","application/vnd.ms-excel")
    with d2:
        st.download_button("Download AI Report (JSON)", json.dumps(insights,indent=2),
                           "ai_insights.json","application/json")

    if show_raw:
        st.subheader("Raw Data"); st.dataframe(df, use_container_width=True)
    if show_kpis:
        st.subheader("All KPIs"); st.json(kpis)

if uploaded_file:
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.get("last_file") != file_key:
        st.session_state["last_file"] = file_key
        st.session_state["result"]    = None
        with st.status("Working on it...", expanded=True) as status:
            st.write("Reading your file...")
            df = load_file(uploaded_file)
            if df is not None:
                st.write("Cleaning the data...")
                clean_df, report = clean_data(df)
                st.write("Calculating KPIs...")
                kpis = compute_kpis(clean_df)
                st.write("Asking Claude AI for insights (10-15 seconds)...")
                insights = run_analysis(kpis, report)
                st.session_state["result"] = {"df":clean_df,"kpis":kpis,"insights":insights}
                status.update(label="Done!", state="complete")
    res = st.session_state.get("result")
    if res:
        if "error" in res["insights"]:
            st.error(f"AI error: {res['insights']['error']}")
        else:
            show_results(res["df"],res["kpis"],res["insights"],show_raw,show_kpis)
else:
    st.info("Upload a file above to begin. You can use data\\sample_sales.csv to test.")