import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import io, json

from src.data_loader  import load_file
from src.data_cleaner import clean_data
from src.kpi_engine   import compute_kpis
from src.ai_agent     import run_analysis

st.set_page_config(
    page_title="Business Analyst Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    background: #F5F5F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #111111 !important;
}

[data-testid="stHeader"]     { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }
#MainMenu, footer, .stDeployButton { visibility: hidden; }

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1300px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F0F0EB; }
::-webkit-scrollbar-thumb { background: #CCCCCC; border-radius: 3px; }

[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #888888 !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
    color: #666666 !important;
    font-size: 0.85rem !important;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2rem 0;
    border-bottom: 2px solid #111111;
    margin-bottom: 2.5rem;
}
.topbar-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #111111;
    letter-spacing: -0.02em;
}
.topbar-meta {
    font-size: 0.72rem;
    color: #999999;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.page-title { margin-bottom: 3rem; }
.page-title h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    color: #111111;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 0.75rem;
}
.page-title p {
    font-size: 0.95rem;
    font-weight: 300;
    color: #777777;
    line-height: 1.65;
    max-width: 480px;
}

.section-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #AAAAAA;
    margin-bottom: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8E8E2;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #DDDDDD;
    border: 1px solid #DDDDDD;
    margin-bottom: 2.5rem;
    border-radius: 3px;
    overflow: hidden;
}
.metric-cell {
    background: #FFFFFF;
    padding: 1.6rem 1.4rem;
}
.metric-cell-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #BBBBBB;
    margin-bottom: 0.55rem;
}
.metric-cell-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #111111;
    line-height: 1;
    letter-spacing: -0.02em;
}

.summary-block {
    background: #111111;
    border-radius: 3px;
    padding: 1.8rem 2rem;
    margin-bottom: 2.5rem;
}
.summary-block p {
    font-size: 0.97rem;
    font-weight: 300;
    color: #CCCCCC;
    line-height: 1.85;
}

.analysis-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #DDDDDD;
    border: 1px solid #DDDDDD;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.analysis-col { background: #FFFFFF; padding: 1.4rem 1.3rem; }
.analysis-col-head {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #111111;
    margin-bottom: 1rem;
    padding-bottom: 0.55rem;
    border-bottom: 2px solid #111111;
}
.analysis-item {
    font-size: 0.86rem;
    font-weight: 400;
    color: #444444;
    line-height: 1.65;
    padding: 0.6rem 0;
    border-bottom: 1px solid #F0F0EB;
}
.analysis-item:last-child { border-bottom: none; }

.chart-panel {
    background: #FFFFFF;
    border: 1px solid #E8E8E2;
    border-radius: 3px;
    padding: 1rem 0.8rem 0.3rem;
    margin-bottom: 1px;
}

[data-testid="stDownloadButton"] button {
    background: #111111 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 3px !important;
    padding: 0.65rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #333333 !important;
}

[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 3px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #777777 !important;
}
[data-testid="stFileUploader"] label {
    font-weight: 600 !important;
    color: #111111 !important;
    font-size: 0.88rem !important;
}

[data-testid="stStatusWidget"] {
    background: #FFFFFF !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 3px !important;
}
[data-testid="stStatusWidget"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #555555 !important;
    font-size: 0.86rem !important;
}

.upload-screen {
    background: #FFFFFF;
    border: 1px solid #E8E8E2;
    border-radius: 3px;
    padding: 2.5rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.upload-screen h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #111111;
    margin-bottom: 0.4rem;
    font-weight: 400;
}
.upload-screen p {
    font-size: 0.84rem;
    color: #999999;
    font-weight: 300;
    line-height: 1.6;
}

.feature-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #DDDDDD;
    border: 1px solid #DDDDDD;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 1.5rem;
}
.feature-cell { background: #FAFAF7; padding: 1.4rem 1.3rem; }
.feature-cell-title {
    font-family: 'DM Serif Display', serif;
    font-size: 0.95rem;
    color: #111111;
    margin-bottom: 0.45rem;
    font-weight: 400;
}
.feature-cell-desc {
    font-size: 0.8rem;
    color: #999999;
    font-weight: 300;
    line-height: 1.65;
}

.page-footer {
    margin-top: 3.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid #DDDDDD;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.page-footer-left {
    font-size: 0.75rem;
    color: #BBBBBB;
    font-weight: 400;
}
.page-footer-right {
    font-size: 0.72rem;
    font-weight: 600;
    color: #111111;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.8rem 0 0.5rem">
        <div style="font-family:'DM Serif Display',serif;font-size:1.1rem;
                    color:#FFFFFF;letter-spacing:-0.01em;margin-bottom:0.2rem">
            Business Analyst
        </div>
        <div style="font-size:0.68rem;color:#444444;letter-spacing:0.14em;
                    text-transform:uppercase;font-weight:500">
            Intelligence Agent
        </div>
    </div>
    <div style="height:1px;background:#222222;margin:1.4rem 0"></div>
    <div style="font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;
                color:#444444;font-weight:600;margin-bottom:0.7rem">
        Display
    </div>
    """, unsafe_allow_html=True)

    show_raw  = st.checkbox("Raw data table",     value=False)
    show_kpis = st.checkbox("Full KPI breakdown", value=False)

    st.markdown("""
    <div style="height:1px;background:#222222;margin:1.4rem 0"></div>
    <div style="font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;
                color:#444444;font-weight:600;margin-bottom:0.7rem">
        Process
    </div>
    <div style="font-size:0.8rem;color:#555555;line-height:2.2;font-weight:300">
        01 &mdash; Upload file<br>
        02 &mdash; Auto clean data<br>
        03 &mdash; Compute KPIs<br>
        04 &mdash; AI generates report
    </div>
    <div style="height:1px;background:#222222;margin:1.4rem 0"></div>
    <div style="font-size:0.75rem;color:#333333;line-height:1.9;font-weight:300">
        Python &middot; pandas<br>
        Claude AI &middot; Streamlit
    </div>
    """, unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-brand">Business Analyst Agent</div>
    <div class="topbar-meta">Manikanta's Project Work</div>
</div>
""", unsafe_allow_html=True)

# ── PAGE TITLE ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">
    <h1>Sales Intelligence<br>Dashboard</h1>
    <p>Upload a CSV or Excel file. The agent cleans your data,
       computes key business metrics, and returns an executive analysis.</p>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOADER ─────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload file — CSV or Excel",
    type=["csv", "xlsx", "xls"],
    label_visibility="visible"
)

# ── CHART LAYOUT HELPER ───────────────────────────────────────────────────────
def clean_layout(title=""):
    return dict(
        title=dict(
            text=title,
            font=dict(family="DM Serif Display, serif",
                      size=13, color="#111111"),
            x=0, xanchor="left",
            pad=dict(l=4, b=10)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif",
                  color="#AAAAAA", size=11),
        margin=dict(l=10, r=10, t=46, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#AAAAAA", size=11)
        )
    )

# ── RESULTS ───────────────────────────────────────────────────────────────────
def show_results(df, kpis, insights, show_raw, show_kpis):

    # SUMMARY
    st.markdown('<div class="section-label">Executive Summary</div>',
                unsafe_allow_html=True)
    summary = insights.get("summary", "No summary generated.")
    st.markdown(
        f'<div class="summary-block"><p>{summary}</p></div>',
        unsafe_allow_html=True
    )

    # METRICS
    st.markdown('<div class="section-label">Key Metrics</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-cell">
            <div class="metric-cell-label">Total Revenue</div>
            <div class="metric-cell-value">${kpis.get('total_revenue', 0):,.0f}</div>
        </div>
        <div class="metric-cell">
            <div class="metric-cell-label">Avg Transaction</div>
            <div class="metric-cell-value">${kpis.get('avg_transaction', 0):,.0f}</div>
        </div>
        <div class="metric-cell">
            <div class="metric-cell-label">Median Transaction</div>
            <div class="metric-cell-value">${kpis.get('median_transaction', 0):,.0f}</div>
        </div>
        <div class="metric-cell">
            <div class="metric-cell-label">Total Records</div>
            <div class="metric-cell-value">{kpis.get('total_rows', 0):,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ANALYSIS
    st.markdown('<div class="section-label">Analysis</div>',
                unsafe_allow_html=True)

    ins_html  = "".join(
        f'<div class="analysis-item">{x}</div>'
        for x in insights.get("insights", [])
    )
    risk_html = "".join(
        f'<div class="analysis-item">{x}</div>'
        for x in insights.get("risks", [])
    )
    rec_html  = "".join(
        f'<div class="analysis-item">{x}</div>'
        for x in insights.get("recommendations", [])
    )

    st.markdown(f"""
    <div class="analysis-grid">
        <div class="analysis-col">
            <div class="analysis-col-head">Insights</div>
            {ins_html}
        </div>
        <div class="analysis-col">
            <div class="analysis-col-head">Risks</div>
            {risk_html}
        </div>
        <div class="analysis-col">
            <div class="analysis-col-head">Recommendations</div>
            {rec_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CHARTS
    st.markdown('<div class="section-label">Visual Analytics</div>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="small")

    with col_a:
        if "revenue_by_region" in kpis:
            regions = list(kpis["revenue_by_region"].keys())
            values  = list(kpis["revenue_by_region"].values())
            fig = go.Figure(go.Bar(
                x=regions,
                y=values,
                marker_color="#111111",
                marker_line_width=0,
                text=[f"${v:,.0f}" for v in values],
                textposition="outside",
                textfont=dict(size=10, color="#AAAAAA",
                              family="DM Sans, sans-serif")
            ))
            fig.update_layout(
                **clean_layout("Revenue by Region"),
                xaxis=dict(showgrid=False, showline=False,
                           tickfont=dict(color="#AAAAAA")),
                yaxis=dict(showgrid=True, gridcolor="#F0F0EB",
                           showline=False, zeroline=False,
                           tickfont=dict(color="#CCCCCC"),
                           tickprefix="$", tickformat=",.0f")
            )
            st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        if "revenue_by_product" in kpis:
            fig2 = go.Figure(go.Pie(
                labels=list(kpis["revenue_by_product"].keys()),
                values=list(kpis["revenue_by_product"].values()),
                hole=0.55,
                marker=dict(
                    colors=["#111111","#444444","#777777","#AAAAAA"],
                    line=dict(color="#F5F5F0", width=2)
                ),
                textfont=dict(color="#FFFFFF",
                              family="DM Sans, sans-serif", size=11),
                hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>"
            ))
            fig2.update_layout(
                **clean_layout("Revenue by Product"),
                annotations=[dict(
                    text="Revenue",
                    x=0.5, y=0.5,
                    font=dict(size=11, color="#AAAAAA",
                              family="DM Sans, sans-serif"),
                    showarrow=False
                )]
            )
            st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if "monthly_trend" in kpis:
        months = list(kpis["monthly_trend"].keys())
        vals   = list(kpis["monthly_trend"].values())
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=months, y=vals,
            mode="lines+markers",
            line=dict(color="#111111", width=2, shape="spline"),
            marker=dict(size=5, color="#111111",
                        line=dict(color="#FFFFFF", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(17,17,17,0.04)",
            hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>"
        ))
        fig3.update_layout(
            **clean_layout("Monthly Revenue Trend"),
            xaxis=dict(showgrid=False, showline=False,
                       tickangle=-30,
                       tickfont=dict(color="#CCCCCC", size=10)),
            yaxis=dict(showgrid=True, gridcolor="#F0F0EB",
                       showline=False, zeroline=False,
                       tickfont=dict(color="#CCCCCC"),
                       tickprefix="$", tickformat=",.0f"),
            showlegend=False
        )
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if "revenue_by_customer_type" in kpis:
        ct_labels = list(kpis["revenue_by_customer_type"].keys())
        ct_vals   = list(kpis["revenue_by_customer_type"].values())
        fig4 = go.Figure(go.Bar(
            x=ct_vals, y=ct_labels,
            orientation="h",
            marker_color=["#111111","#888888"],
            marker_line_width=0,
            text=[f"${v:,.0f}" for v in ct_vals],
            textposition="outside",
            textfont=dict(size=10, color="#AAAAAA",
                          family="DM Sans, sans-serif")
        ))
        fig4.update_layout(
            **clean_layout("New vs Repeat Customers"),
            xaxis=dict(showgrid=True, gridcolor="#F0F0EB",
                       showline=False, zeroline=False,
                       tickfont=dict(color="#CCCCCC"),
                       tickprefix="$", tickformat=",.0f"),
            yaxis=dict(showgrid=False, showline=False,
                       tickfont=dict(color="#444444", size=12))
        )
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # EXPORT
    st.markdown(
        '<div class="section-label" style="margin-top:1.5rem">Export</div>',
        unsafe_allow_html=True
    )
    d1, d2 = st.columns(2, gap="small")
    with d1:
        buf = io.BytesIO()
        df.to_excel(buf, index=False)
        st.download_button(
            "Download Cleaned Data — Excel",
            data=buf.getvalue(),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    with d2:
        st.download_button(
            "Download AI Report — JSON",
            data=json.dumps(insights, indent=2),
            file_name="ai_insights.json",
            mime="application/json",
            use_container_width=True
        )

    if show_raw:
        st.markdown(
            '<div class="section-label" style="margin-top:2rem">Raw Data</div>',
            unsafe_allow_html=True
        )
        st.dataframe(df, use_container_width=True)

    if show_kpis:
        st.markdown(
            '<div class="section-label" style="margin-top:2rem">KPI Breakdown</div>',
            unsafe_allow_html=True
        )
        st.json(kpis)

    st.markdown("""
    <div class="page-footer">
        <div class="page-footer-left">
            AI Business Analyst Agent &mdash;
            Python &middot; pandas &middot; Claude AI &middot; Streamlit
        </div>
        <div class="page-footer-right">Manikanta's Project Work</div>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN LOGIC ────────────────────────────────────────────────────────────────
if uploaded_file:
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.get("last_file") != file_key:
        st.session_state["last_file"] = file_key
        st.session_state["result"]    = None

        with st.status("Running analysis...", expanded=True) as status:
            st.write("Reading file...")
            df = load_file(uploaded_file)
            if df is not None:
                st.write("Cleaning data...")
                clean_df, report = clean_data(df)
                st.write("Computing KPIs...")
                kpis = compute_kpis(clean_df)
                st.write("Generating AI insights...")
                insights = run_analysis(kpis, report)
                st.session_state["result"] = {
                    "df": clean_df, "kpis": kpis, "insights": insights
                }
                status.update(label="Analysis complete.", state="complete")

    res = st.session_state.get("result")
    if res:
        if "error" in res["insights"]:
            st.error(f"Error: {res['insights']['error']}")
        else:
            show_results(
                res["df"], res["kpis"], res["insights"],
                show_raw, show_kpis
            )

else:
    st.markdown("""
    <div class="upload-screen">
        <h3>Upload Your Sales Data</h3>
        <p>
            Supported formats: CSV &nbsp;&middot;&nbsp;
            Excel .xlsx &nbsp;&middot;&nbsp; Excel .xls<br>
            Use <em>data/sample_sales.csv</em> to run a demo.
        </p>
    </div>

    <div class="feature-row">
        <div class="feature-cell">
            <div class="feature-cell-title">Data Cleaning</div>
            <div class="feature-cell-desc">
                Duplicate rows removed. Missing values filled with column median.
                Date columns parsed automatically.
            </div>
        </div>
        <div class="feature-cell">
            <div class="feature-cell-title">KPI Engine</div>
            <div class="feature-cell-desc">
                Revenue by region, monthly trend, product breakdown
                and customer type split — computed via pandas and SQL.
            </div>
        </div>
        <div class="feature-cell">
            <div class="feature-cell-title">AI Analysis</div>
            <div class="feature-cell-desc">
                Claude AI returns an executive summary, key insights,
                business risks and action recommendations.
            </div>
        </div>
    </div>

    <div class="page-footer">
        <div class="page-footer-left">
            AI Business Analyst Agent &mdash;
            Python &middot; pandas &middot; Claude AI &middot; Streamlit
        </div>
        <div class="page-footer-right">Manikanta's Project Work</div>
    </div>
    """, unsafe_allow_html=True)