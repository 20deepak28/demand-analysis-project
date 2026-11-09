
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import json

warnings.filterwarnings("ignore")


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RetailIQ | Retail Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
DATA_DIR = DASHBOARD_DIR / "data"

SUMMARY_PATH = DATA_DIR / "product_summary.parquet"

FORECAST_PATHS = [
    DATA_DIR / "future_forecasts.parquet",
    PROJECT_DIR / "Data/processed/full_dataset/"
    / "future_forecasts_corrected_v2/future_forecasts.parquet"
]

CATEGORY_PATHS = [
    DATA_DIR / "category_error_summary.csv",
    PROJECT_DIR / "Data/processed/full_dataset/"
    / "day13_analysis/category_error_summary.csv"
]

STORE_PATHS = [
    DATA_DIR / "store_error_summary.csv",
    PROJECT_DIR / "Data/processed/full_dataset/"
    / "day13_analysis/store_error_summary.csv"
]

MODEL_PATH = PROJECT_DIR / "models/model_comparison.json"

HISTORY_START = "2016-04-25"
HISTORY_DAYS = 28

FORECAST_START = "2016-05-23"
FORECAST_END = "2016-06-19"


# ============================================================
# 2. VISUAL DESIGN
# ============================================================

st.markdown("""
<style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1550px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #101c32;
    }

    [data-testid="stSidebar"] * {
        color: #edf3ff;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #c5d0e0;
    }

    [data-testid="stSidebar"] hr {
        border-color: #34435b;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e8edf4;
        padding: 19px 20px;
        border-radius: 13px;
        box-shadow: 0 3px 12px rgba(20, 35, 60, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #66748a;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #14213d;
        font-weight: 800;
    }

    .hero {
        background: linear-gradient(115deg, #101c32 0%, #1e3a60 65%, #285681 100%);
        border-radius: 18px;
        padding: 30px 34px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(16, 28, 50, 0.12);
    }

    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #a9c6e8;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        line-height: 1.25;
    }

    .hero-subtitle {
        color: #d2dfef;
        font-size: 14px;
        margin-top: 10px;
        margin-bottom: 0;
    }

    .page-heading {
        color: #14213d;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .page-description {
        color: #738096;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .section-heading {
        color: #172b49;
        font-size: 17px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 10px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e8edf4;
        border-radius: 13px;
        padding: 18px 20px;
        margin: 8px 0 16px 0;
    }

    .info-card-title {
        color: #172b49;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .info-card-text {
        color: #69788e;
        font-size: 13px;
        line-height: 1.6;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        background: #fff2db;
        color: #9a5b00;
    }

    .footer {
        text-align: center;
        color: #8793a6;
        font-size: 12px;
        padding: 22px 0 8px 0;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e7edf4;
        border-radius: 10px;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

COLORS = {
    "navy": "#14213d",
    "blue": "#3478b9",
    "cyan": "#43a5c6",
    "green": "#24966b",
    "yellow": "#e5a52e",
    "orange": "#e67e35",
    "red": "#d94b55",
    "purple": "#8064b5",
    "gray": "#8190a5"
}

RISK_COLORS = {
    "Low": COLORS["green"],
    "Medium": COLORS["yellow"],
    "High": COLORS["orange"],
    "Critical": COLORS["red"]
}


def first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    return None


def numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )
    return df


def section_title(title, description=None):
    st.markdown(
        f'<div class="page-heading">{title}</div>',
        unsafe_allow_html=True
    )

    if description:
        st.markdown(
            f'<div class="page-description">{description}</div>',
            unsafe_allow_html=True
        )


def chart_layout(fig, height=390):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=15, r=15, t=55, b=20),
        font=dict(
            family="DM Sans, sans-serif",
            color="#40516a"
        ),
        title_font=dict(
            size=16,
            color="#172b49"
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        ),
        legend_title_text=""
    )
    return fig


def dataframe_download(df, filename, label="Download CSV"):
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=False
    )


def format_number(value, decimals=0):
    if pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}"


# ============================================================
# 4. DATA LOADING
# ============================================================

@st.cache_data(show_spinner="Loading product intelligence...")
def load_product_summary():

    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(
            f"Product summary not found: {SUMMARY_PATH}"
        )

    df = pd.read_parquet(SUMMARY_PATH)

    required = [
        "id",
        "forecast_total",
        "average_daily_demand",
        "peak_daily_demand"
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required product summary columns: {missing}"
        )

    df["id"] = df["id"].astype(str)

    if "category" not in df.columns:
        df["category"] = (
            df["id"].str.split("_").str[0]
        )

    if "store_id" not in df.columns:
        df["store_id"] = (
            df["id"].str.extract(
                r"((?:CA|TX|WI)_\d+)"
            )[0]
        )

    numeric_columns = [
        "forecast_total",
        "average_daily_demand",
        "peak_daily_demand",
        "inventory_risk_score",
        "avg_daily_demand",
        "demand_std",
        "safety_stock",
        "reorder_point",
        "mae",
        "rmse",
        "wape"
    ]

    return numeric(df, numeric_columns)


@st.cache_data(show_spinner="Loading daily demand forecasts...")
def load_forecast_data():

    path = first_existing(FORECAST_PATHS)

    if path is None:
        return None

    df = pd.read_parquet(path)

    required = [
        "id",
        "date",
        "predicted_sales"
    ]

    if not all(col in df.columns for col in required):
        return None

    df["id"] = df["id"].astype(str)
    df["date"] = pd.to_datetime(df["date"])

    df["predicted_sales"] = pd.to_numeric(
        df["predicted_sales"],
        errors="coerce"
    ).clip(lower=0)

    if "category" not in df.columns:
        df["category"] = (
            df["id"].str.split("_").str[0]
        )

    if "store_id" not in df.columns:
        df["store_id"] = (
            df["id"].str.extract(
                r"((?:CA|TX|WI)_\d+)"
            )[0]
        )

    return df.dropna(
        subset=["date", "predicted_sales"]
    )


@st.cache_data(show_spinner="Preparing historical sales...")
def load_historical_data():

    # Prefer an already prepared historical dataset.
    prepared_path = DATA_DIR / "historical_last_28_days.parquet"

    if prepared_path.exists():

        hist = pd.read_parquet(prepared_path)

        if {"id", "date", "actual_sales"}.issubset(hist.columns):
            hist["date"] = pd.to_datetime(hist["date"])
            return hist

    # Otherwise read only the last 28 daily columns
    # from the original M5 evaluation dataset.
    raw_dir = PROJECT_DIR / "Data" / "raw"

    candidates = list(
        raw_dir.rglob("sales_train_evaluation.csv")
    )

    if not candidates:
        candidates = list(
            raw_dir.rglob("sales_train_validation.csv")
        )

    if not candidates:
        return None

    source = candidates[0]

    daily_columns = [
        f"d_{i}" for i in range(1914, 1942)
    ]

    usecols = ["id"] + daily_columns

    raw = pd.read_csv(
        source,
        usecols=usecols,
        dtype={"id": "string"}
    )

    hist = raw.melt(
        id_vars=["id"],
        value_vars=daily_columns,
        var_name="day",
        value_name="actual_sales"
    )

    day_number = (
        hist["day"].str.replace("d_", "", regex=False)
        .astype(int)
    )

    hist["date"] = (
        pd.Timestamp("2011-01-29")
        + pd.to_timedelta(day_number - 1, unit="D")
    )

    hist["actual_sales"] = pd.to_numeric(
        hist["actual_sales"],
        errors="coerce"
    )

    hist = hist[
        ["id", "date", "actual_sales"]
    ]

    return hist


@st.cache_data
def load_model_metrics():

    if MODEL_PATH.exists():

        with open(MODEL_PATH, "r") as file:
            return json.load(file)

    return {
        "lightgbm": {
            "mae": 0.930733,
            "rmse": 2.006124,
            "wape": 71.662936
        },
        "lstm_epoch_2": {
            "mae": 0.889473,
            "rmse": 2.137365,
            "wape": 68.49
        },
        "lstm_epoch_5": {
            "mae": 0.887903,
            "rmse": 2.149717,
            "wape": 68.37
        }
    }


@st.cache_data
def load_analysis(paths):

    path = first_existing(paths)

    if path is None:
        return None

    return pd.read_csv(path)


# ============================================================
# 5. LOAD APPLICATION DATA
# ============================================================

try:

    products = load_product_summary()

    forecast_data = load_forecast_data()

    historical_data = load_historical_data()

    model_metrics = load_model_metrics()

    category_analysis = load_analysis(
        CATEGORY_PATHS
    )

    store_analysis = load_analysis(
        STORE_PATHS
    )

except Exception as error:

    st.error(
        f"Dashboard data loading failed: {error}"
    )

    st.stop()


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div style="padding:10px 0 20px 0;">
        <div style="font-size:25px;font-weight:800;color:white;">
            ◈ RetailIQ
        </div>
        <div style="font-size:11px;color:#9eafc7;letter-spacing:1px;">
            RETAIL INTELLIGENCE PLATFORM
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

pages = [
    "Executive Overview",
    "Demand Forecasting",
    "Historical vs Forecast",
    "Model Performance",
    "Store & Category Analysis",
    "Inventory Optimization",
    "High-Risk Products"
]

page = st.sidebar.radio(
    "NAVIGATION",
    pages,
    label_visibility="visible"
)

st.sidebar.divider()

st.sidebar.markdown(
    "**FILTER DATA**"
)

categories = sorted(
    products["category"].dropna().unique().tolist()
)

stores = sorted(
    products["store_id"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)

selected_stores = st.sidebar.multiselect(
    "Store",
    stores,
    default=stores
)

product_search = st.sidebar.text_input(
    "Search Product",
    placeholder="Search product ID..."
)

# Apply global filters.

filtered_products = products[
    products["category"].isin(selected_categories)
    & products["store_id"].isin(selected_stores)
].copy()

if product_search:
    filtered_products = filtered_products[
        filtered_products["id"].str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

if filtered_products.empty:

    st.warning(
        "No products match the selected filters. "
        "Please change your filters."
    )

    st.stop()

filtered_ids = filtered_products["id"].unique()

if forecast_data is not None:

    filtered_forecast = forecast_data[
        forecast_data["id"].isin(filtered_ids)
    ].copy()

else:

    filtered_forecast = None


# ============================================================
# ============================================================
# 7. COMMON HEADER
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-eyebrow">RETAIL DEMAND &amp; INVENTORY INTELLIGENCE</div>'
    '<div class="hero-title">Smarter Demand. Better Inventory Decisions.</div>'
    '<div class="hero-subtitle">A data-driven view of retail demand, model performance, product trends and inventory risk.</div>'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Displaying {len(filtered_products):,} product-store combinations "
    f"across {filtered_products['store_id'].nunique()} stores."
)

st.divider()


# 8. EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    section_title(
        "Executive Overview",
        "A consolidated view of predicted demand, product performance "
        "and inventory risk."
    )

    total_products = len(filtered_products)

    total_demand = filtered_products[
        "forecast_total"
    ].sum()

    average_daily = filtered_products[
        "average_daily_demand"
    ].mean()

    high_critical = (
        filtered_products["risk_level"]
        .isin(["High", "Critical"])
        .sum()
        if "risk_level" in filtered_products.columns
        else 0
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Product-Store Combinations",
        f"{total_products:,}"
    )

    b.metric(
        "28-Day Forecast Demand",
        f"{total_demand:,.0f} units"
    )

    c.metric(
        "Average Daily Demand",
        f"{average_daily:,.2f} units"
    )

    d.metric(
        "High / Critical Risk",
        f"{high_critical:,}"
    )

    st.markdown(
        '<div class="section-heading">Demand Overview</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1.35, 1]
    )

    with left:

        category_demand = (
            filtered_products.groupby("category")[
                "forecast_total"
            ]
            .sum()
            .reset_index()
            .sort_values("forecast_total", ascending=False)
        )

        fig = px.bar(
            category_demand,
            x="category",
            y="forecast_total",
            color="category",
            text_auto=".2s",
            title="Forecast Demand by Product Category",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Category",
            yaxis_title="Forecast Units"
        )

        st.plotly_chart(
            chart_layout(fig, 370),
            use_container_width=True
        )

    with right:

        if "risk_level" in filtered_products.columns:

            risk_counts = (
                filtered_products["risk_level"]
                .value_counts()
                .reindex(
                    ["Low", "Medium", "High", "Critical"],
                    fill_value=0
                )
                .rename_axis("Risk Level")
                .reset_index(name="Products")
            )

            fig = px.pie(
                risk_counts,
                names="Risk Level",
                values="Products",
                hole=0.62,
                color="Risk Level",
                color_discrete_map=RISK_COLORS,
                title="Inventory Risk Distribution"
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                chart_layout(fig, 370),
                use_container_width=True
            )

    st.markdown(
        '<div class="section-heading">Top Products by Forecast Demand</div>',
        unsafe_allow_html=True
    )

    top_products = filtered_products.nlargest(
        10, "forecast_total"
    ).sort_values("forecast_total")

    fig = px.bar(
        top_products,
        x="forecast_total",
        y="id",
        orientation="h",
        color="category",
        hover_data=[
            "store_id",
            "average_daily_demand",
            "peak_daily_demand"
        ],
        title="Top 10 Product-Store Combinations"
    )

    fig.update_layout(
        xaxis_title="28-Day Forecast Units",
        yaxis_title="",
        legend_title="Category"
    )

    st.plotly_chart(
        chart_layout(fig, 430),
        use_container_width=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Business Interpretation</div>
            <div class="info-card-text">
                Use forecast demand to identify high-volume products
                and compare inventory risk across product-store
                combinations. Risk scores represent a project-defined
                prioritization measure, not the probability of a stockout.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 9. DEMAND FORECASTING
# ============================================================

elif page == "Demand Forecasting":

    section_title(
        "Demand Forecasting",
        "Explore daily demand estimates across the product portfolio."
    )

    if filtered_forecast is None:

        st.error("The forecast dataset could not be found.")
        st.stop()

    total_units = filtered_forecast[
        "predicted_sales"
    ].sum()

    forecast_days = filtered_forecast[
        "date"
    ].nunique()

    product_count = filtered_forecast[
        "id"
    ].nunique()

    a, b, c = st.columns(3)

    a.metric(
        "Forecast Demand",
        f"{total_units:,.0f} units"
    )

    b.metric(
        "Forecast Period",
        f"{forecast_days} days"
    )

    c.metric(
        "Products Covered",
        f"{product_count:,}"
    )

    st.markdown(
        '<span class="status-pill">EXPERIMENTAL HISTORICAL FORECAST</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Daily Demand Trend</div>',
        unsafe_allow_html=True
    )

    daily = (
        filtered_forecast.groupby("date")[
            "predicted_sales"
        ]
        .sum()
        .reset_index()
    )

    fig = px.area(
        daily,
        x="date",
        y="predicted_sales",
        markers=True,
        title="Total Predicted Daily Demand"
    )

    fig.update_traces(
        line_color=COLORS["blue"],
        fillcolor="rgba(52,120,185,0.14)"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Predicted Units"
    )

    st.plotly_chart(
        chart_layout(fig, 420),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Demand by Category</div>',
        unsafe_allow_html=True
    )

    category_daily = (
        filtered_forecast.groupby(
            ["date", "category"]
        )["predicted_sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        category_daily,
        x="date",
        y="predicted_sales",
        color="category",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Predicted Units"
    )

    st.plotly_chart(
        chart_layout(fig, 380),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Product Forecast Details</div>',
        unsafe_allow_html=True
    )

    table = filtered_products[
        [
            "id",
            "category",
            "store_id",
            "forecast_total",
            "average_daily_demand",
            "peak_daily_demand"
        ]
    ].sort_values(
        "forecast_total",
        ascending=False
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    dataframe_download(
        table,
        "product_forecast_summary.csv"
    )


# ============================================================
# 10. HISTORICAL VS FORECAST
# ============================================================

elif page == "Historical vs Forecast":

    section_title(
        "Historical vs Forecast",
        "Compare observed historical sales with model-generated "
        "demand estimates for the same product-store combination."
    )

    st.info(
        "Historical period: April 25 – May 22, 2016 | "
        "Forecast period: May 23 – June 19, 2016. "
        "This is a historical M5 benchmark exercise, not a live forecast."
    )

    product_options = sorted(
        filtered_products["id"].unique().tolist()
    )

    if not product_options:
        st.warning("No products available.")
        st.stop()

    selected_product = st.selectbox(
        "Choose a Product-Store Combination",
        product_options
    )

    historical_product = None
    forecast_product = None

    if historical_data is not None:

        historical_product = historical_data[
            historical_data["id"] == selected_product
        ].copy()

        historical_product = historical_product.sort_values(
            "date"
        )

    if filtered_forecast is not None:

        forecast_product = filtered_forecast[
            filtered_forecast["id"] == selected_product
        ].copy()

        forecast_product = forecast_product.sort_values(
            "date"
        )

    if forecast_product is None or forecast_product.empty:

        st.warning("Forecast data is unavailable for this product.")
        st.stop()

    fig = go.Figure()

    actual_available = (
        historical_product is not None
        and not historical_product.empty
    )

    if actual_available:

        fig.add_trace(
            go.Scatter(
                x=historical_product["date"],
                y=historical_product["actual_sales"],
                name="Actual Sales",
                mode="lines",
                line=dict(
                    color=COLORS["navy"],
                    width=2.8
                ),
                fill="tozeroy",
                fillcolor="rgba(20,33,61,0.06)"
            )
        )

    fig.add_trace(
        go.Scatter(
            x=forecast_product["date"],
            y=forecast_product["predicted_sales"],
            name="Forecast Demand",
            mode="lines",
            line=dict(
                color=COLORS["blue"],
                width=3,
                dash="dash"
            )
        )
    )

    # Forecast boundary — use a shape instead of add_vline
    # to avoid Plotly Timestamp arithmetic errors.
    forecast_boundary = pd.Timestamp(FORECAST_START)

    fig.add_shape(
        type="line",
        x0=forecast_boundary.isoformat(),
        x1=forecast_boundary.isoformat(),
        y0=0,
        y1=1,
        yref="paper",
        line=dict(
            color="#95a2b5",
            width=2,
            dash="dot"
        )
    )

    fig.add_annotation(
        x=forecast_boundary.isoformat(),
        y=1,
        yref="paper",
        text="Forecast begins",
        showarrow=False,
        yshift=12,
        font=dict(color="#64748b", size=11)
    )

    fig.update_layout(
        title=f"Demand History and Forecast — {selected_product}",
        xaxis_title="Date",
        yaxis_title="Units",
        hovermode="x unified"
    )

    st.plotly_chart(
        chart_layout(fig, 470),
        use_container_width=True
    )

    if actual_available:

        actual_total = historical_product[
            "actual_sales"
        ].sum()

        predicted_total = forecast_product[
            "predicted_sales"
        ].sum()

        actual_avg = historical_product[
            "actual_sales"
        ].mean()

        predicted_avg = forecast_product[
            "predicted_sales"
        ].mean()

        a, b, c, d = st.columns(4)

        a.metric(
            "Historical 28-Day Sales",
            f"{actual_total:,.0f}"
        )

        b.metric(
            "Forecast 28-Day Demand",
            f"{predicted_total:,.2f}"
        )

        c.metric(
            "Historical Daily Average",
            f"{actual_avg:,.2f}"
        )

        d.metric(
            "Forecast Daily Average",
            f"{predicted_avg:,.2f}"
        )

        change = (
            (predicted_total - actual_total) / actual_total * 100
            if actual_total != 0 else np.nan
        )

        if pd.notna(change):

            st.caption(
                f"Forecast change against the preceding 28-day "
                f"actual period: {change:+.2f}%. "
                "This is a comparison of adjacent periods, "
                "not a forecast accuracy metric."
            )

    else:

        st.warning(
            "Historical sales data is unavailable. "
            "The chart is showing the forecast only."
        )

    st.markdown(
        '<div class="section-heading">Detailed Demand Records</div>',
        unsafe_allow_html=True
    )

    if actual_available:

        actual_table = historical_product[
            ["date", "actual_sales"]
        ].rename(
            columns={"actual_sales": "sales"}
        )

        actual_table["series"] = "Actual"

    else:

        actual_table = pd.DataFrame(
            columns=["date", "sales", "series"]
        )

    future_table = forecast_product[
        ["date", "predicted_sales"]
    ].rename(
        columns={"predicted_sales": "sales"}
    )

    future_table["series"] = "Forecast"

    comparison_table = pd.concat(
        [actual_table, future_table],
        ignore_index=True
    )

    st.dataframe(
        comparison_table,
        use_container_width=True,
        hide_index=True
    )

    dataframe_download(
        comparison_table,
        "historical_vs_forecast.csv"
    )


# ============================================================
# 11. MODEL PERFORMANCE
# ============================================================

elif page == "Model Performance":

    section_title(
        "Model Performance",
        "Compare the validation performance of the machine learning "
        "models developed for retail demand prediction."
    )

    model_rows = []

    model_labels = {
        "lightgbm": "LightGBM",
        "lstm_epoch_2": "LSTM — Epoch 2",
        "lstm_epoch_5": "LSTM — Epoch 5"
    }

    for key, label in model_labels.items():

        values = model_metrics.get(key, {})

        if values:

            model_rows.append({
                "Model": label,
                "MAE": values.get("mae", np.nan),
                "RMSE": values.get("rmse", np.nan),
                "WAPE (%)": values.get("wape", np.nan)
            })

    performance = pd.DataFrame(model_rows)

    if performance.empty:
        st.warning("Model performance metrics are unavailable.")
        st.stop()

    best_mae = performance.loc[
        performance["MAE"].idxmin()
    ]

    best_rmse = performance.loc[
        performance["RMSE"].idxmin()
    ]

    best_wape = performance.loc[
        performance["WAPE (%)"].idxmin()
    ]

    a, b, c = st.columns(3)

    a.metric(
        "Best MAE",
        f"{best_mae['MAE']:.4f}",
        best_mae["Model"]
    )

    b.metric(
        "Best RMSE",
        f"{best_rmse['RMSE']:.4f}",
        best_rmse["Model"]
    )

    c.metric(
        "Best WAPE",
        f"{best_wape['WAPE (%)']:.2f}%",
        best_wape["Model"]
    )

    st.markdown(
        '<div class="section-heading">Validation Metric Comparison</div>',
        unsafe_allow_html=True
    )

    metric_choice = st.selectbox(
        "Select Metric",
        ["MAE", "RMSE", "WAPE (%)"]
    )

    fig = px.bar(
        performance,
        x="Model",
        y=metric_choice,
        color="Model",
        text_auto=".4f",
        title=f"Model Comparison — {metric_choice}"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Model",
        yaxis_title=metric_choice
    )

    st.plotly_chart(
        chart_layout(fig, 390),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Model Scorecard</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        performance.round(4),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">How to interpret these results</div>
            <div class="info-card-text">
                MAE measures average absolute prediction error.
                RMSE penalizes larger errors more heavily.
                WAPE expresses aggregate absolute error relative
                to actual demand. Lower values indicate better
                performance for each metric.
                <br><br>
                A model may perform better on one metric and worse
                on another, so model selection should consider the
                business objective.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 12. STORE & CATEGORY ANALYSIS
# ============================================================

elif page == "Store & Category Analysis":

    section_title(
        "Store & Category Analysis",
        "Understand how forecast demand and validation performance "
        "vary across stores and product categories."
    )

    left, right = st.columns(2)

    with left:

        store_demand = (
            filtered_products.groupby("store_id")[
                "forecast_total"
            ]
            .sum()
            .reset_index()
            .sort_values("forecast_total", ascending=False)
        )

        fig = px.bar(
            store_demand,
            x="store_id",
            y="forecast_total",
            color="store_id",
            title="Forecast Demand by Store"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Store",
            yaxis_title="Forecast Units"
        )

        st.plotly_chart(
            chart_layout(fig, 380),
            use_container_width=True
        )

    with right:

        category_demand = (
            filtered_products.groupby("category")[
                "forecast_total"
            ]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            category_demand,
            names="category",
            values="forecast_total",
            hole=0.58,
            title="Category Demand Share"
        )

        st.plotly_chart(
            chart_layout(fig, 380),
            use_container_width=True
        )

    st.markdown(
        '<div class="section-heading">Store Validation Performance</div>',
        unsafe_allow_html=True
    )

    if store_analysis is not None:

        st.dataframe(
            store_analysis,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Store validation metrics are unavailable."
        )

    st.markdown(
        '<div class="section-heading">Category Validation Performance</div>',
        unsafe_allow_html=True
    )

    if category_analysis is not None:

        st.dataframe(
            category_analysis,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Category validation metrics are unavailable."
        )


# ============================================================
# 13. INVENTORY OPTIMIZATION
# ============================================================

elif page == "Inventory Optimization":

    section_title(
        "Inventory Optimization",
        "Review demand-based safety stock and reorder thresholds "
        "for product-store combinations."
    )

    st.info(
        "Illustrative planning assumptions: 7-day lead time and "
        "95% service level. These calculations are threshold "
        "recommendations, not live inventory positions or purchase orders."
    )

    inventory_view = filtered_products.dropna(
        subset=["safety_stock", "reorder_point"]
    ).copy()

    if inventory_view.empty:

        st.warning(
            "Inventory recommendation fields are unavailable."
        )
        st.stop()

    a, b, c = st.columns(3)

    a.metric(
        "Products Analyzed",
        f"{len(inventory_view):,}"
    )

    b.metric(
        "Average Safety Stock",
        f"{inventory_view['safety_stock'].mean():,.2f}"
    )

    c.metric(
        "Average Reorder Point",
        f"{inventory_view['reorder_point'].mean():,.2f}"
    )

    st.markdown(
        '<div class="section-heading">Inventory Threshold Comparison</div>',
        unsafe_allow_html=True
    )

    sample = inventory_view.nlargest(
        15, "forecast_total"
    ).sort_values("reorder_point")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Safety Stock",
            x=sample["safety_stock"],
            y=sample["id"],
            orientation="h",
            marker_color=COLORS["cyan"]
        )
    )

    fig.add_trace(
        go.Bar(
            name="Reorder Point",
            x=sample["reorder_point"],
            y=sample["id"],
            orientation="h",
            marker_color=COLORS["blue"]
        )
    )

    fig.update_layout(
        barmode="group",
        xaxis_title="Units",
        yaxis_title="Product",
        height=570
    )

    st.plotly_chart(
        chart_layout(fig, 570),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Inventory Recommendations</div>',
        unsafe_allow_html=True
    )

    inventory_columns = [
        "id",
        "category",
        "store_id",
        "avg_daily_demand",
        "demand_std",
        "safety_stock",
        "reorder_point"
    ]

    inventory_columns = [
        col for col in inventory_columns
        if col in inventory_view.columns
    ]

    inventory_table = inventory_view[
        inventory_columns
    ].sort_values(
        "reorder_point",
        ascending=False
    )

    st.dataframe(
        inventory_table,
        use_container_width=True,
        hide_index=True
    )

    dataframe_download(
        inventory_table,
        "inventory_recommendations.csv"
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Methodology and limitations</div>
            <div class="info-card-text">
                Safety stock and reorder points are calculated from
                historical demand variability and assumed replenishment
                lead time. The M5 dataset does not provide actual
                on-hand inventory or supplier lead times.
                Therefore, these outputs should be interpreted as
                illustrative planning thresholds.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 14. HIGH-RISK PRODUCTS
# ============================================================

elif page == "High-Risk Products":

    section_title(
        "High-Risk Products",
        "Prioritize products with elevated project-defined inventory "
        "risk scores for further investigation."
    )

    if "risk_level" not in filtered_products.columns:

        st.warning("Risk classifications are unavailable.")
        st.stop()

    risk_levels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    risk_filter = st.multiselect(
        "Risk Classification",
        risk_levels,
        default=["Critical", "High"]
    )

    risk_df = filtered_products[
        filtered_products["risk_level"].isin(risk_filter)
    ].copy()

    a, b, c = st.columns(3)

    a.metric(
        "Products in Selected Risk Bands",
        f"{len(risk_df):,}"
    )

    b.metric(
        "Average Risk Score",
        format_number(
            risk_df["inventory_risk_score"].mean(),
            2
        )
    )

    c.metric(
        "Highest Risk Score",
        format_number(
            risk_df["inventory_risk_score"].max(),
            2
        )
    )

    st.markdown(
        '<div class="section-heading">Risk Score Distribution</div>',
        unsafe_allow_html=True
    )

    risk_distribution = (
        filtered_products.groupby("risk_level")
        .size()
        .reindex(risk_levels, fill_value=0)
        .rename_axis("Risk Level")
        .reset_index(name="Products")
    )

    fig = px.bar(
        risk_distribution,
        x="Risk Level",
        y="Products",
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
        text="Products"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Risk Classification",
        yaxis_title="Number of Products"
    )

    st.plotly_chart(
        chart_layout(fig, 350),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Prioritized Product List</div>',
        unsafe_allow_html=True
    )

    display_columns = [
        "id",
        "category",
        "store_id",
        "inventory_risk_score",
        "risk_level",
        "forecast_total",
        "mae",
        "wape",
        "safety_stock",
        "reorder_point"
    ]

    display_columns = [
        col for col in display_columns
        if col in risk_df.columns
    ]

    risk_table = risk_df[
        display_columns
    ].sort_values(
        "inventory_risk_score",
        ascending=False
    )

    st.dataframe(
        risk_table,
        use_container_width=True,
        hide_index=True
    )

    dataframe_download(
        risk_table,
        "high_risk_products.csv",
        "Download Risk Analysis"
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Risk Score Interpretation</div>
            <div class="info-card-text">
                The risk score is a project-defined prioritization
                measure combining forecast error ranking and
                safety-stock ranking. It is not a statistically
                calibrated probability of stockout or product failure.
                Higher scores indicate products that may deserve
                closer review.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <strong>RetailIQ</strong>
        <br>
        Retail Demand Forecasting & Inventory Intelligence
        <br><br>
        Built with Python · Pandas · LightGBM · PyTorch ·
        Streamlit · Plotly
        <br>
        Historical M5 benchmark | May 2016 – June 2016
    </div>
    """,
    unsafe_allow_html=True
)
