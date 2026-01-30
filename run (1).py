import streamlit as st
import pandas as pd
import plotly.express as px
from utils import json_to_df

px.defaults.template = "plotly_white"
px.defaults.height = 420

st.set_page_config(page_title="Near Miss Dashboard", layout="wide")
st.title("🚧 Near Miss Data Analysis Dashboard")
st.write("Upload a Near Miss JSON file to explore safety trends and risk insights.")

uploaded_file = st.file_uploader("Upload Near Miss JSON", type=["json"])
if uploaded_file is None:
    st.info("Please upload a Near Miss JSON file.")
    st.stop()

@st.cache_data
def load_data(file):
    return json_to_df(file)

df = load_data(uploaded_file)

df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

def find_column(keywords):
    for col in df.columns:
        if any(k in col for k in keywords):
            return col
    return None

category_col = find_column(["primary_category", "category"])
sub_category_col = find_column(["sub"])
severity_col = find_column(["severity"])
region_col = find_column(["region", "location"])
unsafe_col = find_column(["unsafe"])

# ---------- Clean categorical columns ----------
for col in [category_col, region_col, unsafe_col]:
    if col:
        df[col] = (
            df[col]
            .replace([None, "", "nan", "NaN", "None", "null", "NaT"], pd.NA)
            .astype("string")
            .fillna("Unknown")
        )

# ---------- Clean severity ----------
if severity_col:
    df[severity_col] = (
        pd.to_numeric(df[severity_col], errors="coerce")
        .fillna(0)
        .astype(int)
    )

# ---------- Date handling (single source of truth) ----------
date_col = next((c for c in df.columns if "date" in c or "time" in c), None)

if date_col:
    df[date_col] = pd.to_numeric(df[date_col], errors="coerce")
    df["incident_datetime"] = pd.to_datetime(df[date_col], unit="ms", errors="coerce")
    df = df.dropna(subset=["incident_datetime"])

    df["year_month"] = df["incident_datetime"].dt.to_period("M").astype(str)
    df["incident_year"] = df["incident_datetime"].dt.year

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

if category_col:
    categories = sorted(df[category_col].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Category", categories, default=categories
    )
    df = df[df[category_col].isin(selected_categories)]

if region_col:
    regions = sorted(df[region_col].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Region", regions, default=regions
    )
    df = df[df[region_col].isin(selected_regions)]

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------- KPIs ----------
st.subheader("Key Safety Metrics")
m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Near Misses", len(df))
m2.metric("High Severity (3 & 4)", len(df[df[severity_col] >= 3]) if severity_col else "N/A")
m3.metric("Regions Impacted", df[region_col].nunique() if region_col else "N/A")
m4.metric("Categories Involved", df[category_col].nunique() if category_col else "N/A")

# ---------- Category & Severity ----------
st.subheader("Category & Severity Overview")
c1, c2 = st.columns(2)

if category_col:
    cat_df = df[category_col].value_counts().reset_index()
    cat_df.columns = ["Category", "Count"]
    c1.plotly_chart(
        px.bar(cat_df, x="Category", y="Count", title="Near Misses by Category"),
        use_container_width=True
    )

if severity_col:
    sev_df = df[severity_col].value_counts().reset_index()
    sev_df.columns = ["Severity Level", "Count"]
    c2.plotly_chart(
        px.pie(sev_df, names="Severity Level", values="Count",
               hole=0.45, title="Severity Level Distribution"),
        use_container_width=True
    )

# ---------- Monthly trend ----------
st.subheader("Monthly Near Miss Trend")

if "year_month" in df.columns:
    trend = (
        df.groupby("year_month")
        .size()
        .reset_index(name="Count")
        .sort_values("year_month")
    )

    st.plotly_chart(
        px.line(trend, x="year_month", y="Count",
                markers=True, title="Monthly Near Miss Trend"),
        use_container_width=True
    )
else:
    st.info("Monthly trend unavailable (no valid date data).")

# ---------- Region & Unsafe ----------
st.subheader("Regional & Behavioral Insights")
c1, c2 = st.columns(2)

if region_col:
    reg_df = df[region_col].value_counts().reset_index()
    reg_df.columns = ["Region", "Count"]
    c1.plotly_chart(
        px.bar(reg_df, x="Region", y="Count", title="Near Misses by Region"),
        use_container_width=True
    )

if unsafe_col:
    unsafe_df = df[unsafe_col].value_counts().reset_index()
    unsafe_df.columns = ["Type", "Count"]
    c2.plotly_chart(
        px.pie(unsafe_df, names="Type", values="Count",
               title="Unsafe Condition vs Unsafe Behavior"),
        use_container_width=True
    )

# ---------- Heatmap ----------
st.subheader("Risk Concentration Analysis")

if category_col and severity_col:
    heatmap = pd.crosstab(df[category_col], df[severity_col]).reset_index()
    heatmap = heatmap.melt(category_col, var_name="Severity", value_name="Count")

    st.plotly_chart(
        px.density_heatmap(
            heatmap,
            x="Severity",
            y=category_col,
            z="Count",
            title="Severity vs Category Heatmap",
            height=480
        ),
        use_container_width=True
    )

# ---------- High-risk ----------
st.subheader("High-Risk Areas")
c1, c2 = st.columns(2)

if sub_category_col:
    sub_df = df[sub_category_col].value_counts().head(10).reset_index()
    sub_df.columns = ["Sub Category", "Count"]
    c1.plotly_chart(
        px.bar(sub_df, x="Sub Category", y="Count",
               title="Top Near Miss Sub-Categories"),
        use_container_width=True
    )

if severity_col and region_col:
    high_df = df[df[severity_col] >= 3]
    reg_high = high_df[region_col].value_counts().reset_index()
    reg_high.columns = ["Region", "Count"]
    c2.plotly_chart(
        px.bar(reg_high, x="Region", y="Count",
               title="High Severity Near Misses by Region"),
        use_container_width=True
    )

# ---------- Year-wise (FIXED) ----------
st.subheader("Year-wise Near Miss Comparison")

if "incident_year" in df.columns:
    year_df = (
        df["incident_year"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    year_df.columns = ["Year", "Count"]

    st.plotly_chart(
        px.bar(year_df, x="Year", y="Count",
               title="Year-wise Near Miss Comparison"),
        use_container_width=True
    )

# ---------- Pareto ----------
if category_col:
    pareto = df[category_col].value_counts().reset_index()
    pareto.columns = ["Category", "Count"]
    pareto["Cumulative %"] = pareto["Count"].cumsum() / pareto["Count"].sum() * 100

    fig = px.bar(pareto, x="Category", y="Count",
                 title="Pareto Analysis (80/20 Rule)")
    fig.add_scatter(
        x=pareto["Category"],
        y=pareto["Cumulative %"],
        yaxis="y2",
        name="Cumulative %"
    )
    fig.update_layout(
        yaxis2=dict(overlaying="y", side="right", range=[0, 100])
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Near Miss Safety Dashboard • Clean UI • Correct Time Series • Final")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Made with ❤️ by <b>Vedansh Kadre</b>"
    "</p>",
    unsafe_allow_html=True
)
