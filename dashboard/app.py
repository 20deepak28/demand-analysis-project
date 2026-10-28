import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Retail Demand Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "processed" / "feature_engineered_sample.parquet"
POLICY_PATH = BASE_DIR / "reports" / "day8_inventory_simulation_results.csv"
EVALUATION_PATH = BASE_DIR / "reports" / "day8_inventory_evaluation.csv"

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def load_inventory():
    if POLICY_PATH.exists():
        return pd.read_csv(POLICY_PATH)
    return pd.DataFrame()

@st.cache_data
def load_evaluation():
    if EVALUATION_PATH.exists():
        return pd.read_csv(EVALUATION_PATH)
    return pd.DataFrame()

# ---------------- HEADER ----------------
st.title("📊 Retail Demand Intelligence")
st.caption(
    "Demand analysis • Sales trends • Inventory optimization"
)

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

df = load_data()
inventory = load_inventory()
evaluation = load_evaluation()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Dashboard Filters")

# ---------------- DATE FILTER ----------------

min_date = df["date"].min().date()
max_date = df["date"].max().date()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Date Range")

date_mode = st.sidebar.selectbox(
    "Select period",
    [
        "All Time",
        "Last 30 Days",
        "Last 90 Days",
        "Last 6 Months",
        "Custom Range"
    ],
    index=0
)

if date_mode == "All Time":
    start_date, end_date = min_date, max_date

elif date_mode == "Last 30 Days":
    start_date = max(min_date, max_date - pd.Timedelta(days=30))
    end_date = max_date

elif date_mode == "Last 90 Days":
    start_date = max(min_date, max_date - pd.Timedelta(days=90))
    end_date = max_date

elif date_mode == "Last 6 Months":
    start_date = max(min_date, max_date - pd.DateOffset(months=6).date())
    end_date = max_date

else:
    st.sidebar.caption("Choose your preferred dates")

    date_columns = st.sidebar.columns(2)

    start_date = date_columns[0].date_input(
        "From",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="custom_start_date"
    )

    end_date = date_columns[1].date_input(
        "To",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="custom_end_date"
    )

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

date_range = (start_date, end_date)
categories = sorted(df["cat_id"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

stores = sorted(df["store_id"].dropna().unique())
selected_stores = st.sidebar.multiselect(
    "Store",
    stores,
    default=stores
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        filtered_df["date"].between(
            pd.Timestamp(start_date),
            pd.Timestamp(end_date)
        )
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["cat_id"].isin(selected_categories)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_stores:
    filtered_df = filtered_df[
        filtered_df["store_id"].isin(selected_stores)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if filtered_df.empty:
    st.warning("No data matches your selected filters.")
    st.stop()

# ---------------- KPI CARDS ----------------
total_sales = filtered_df["sales"].sum()
active_days = (filtered_df["sales"] > 0).sum()
product_count = filtered_df["item_id"].nunique()
store_count = filtered_df["store_id"].nunique()
average_daily_sales = filtered_df["sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📦 Total Units Sold", f"{total_sales:,.0f}")
col2.metric("🛒 Products", f"{product_count:,}")
col3.metric("🏬 Stores", f"{store_count:,}")
col4.metric("📈 Average Units / Row", f"{average_daily_sales:.2f}")

st.divider()

# ---------------- SALES TREND ----------------
# ---------------- SALES TREND ----------------
st.subheader("📈 Sales Trend")

daily_sales = (
    filtered_df.groupby("date", as_index=False)["sales"]
    .sum()
    .sort_values("date")
)

fig_sales = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Daily Sales",
    template="plotly_white"
)

fig_sales.update_traces(
    line=dict(width=1.5),
    connectgaps=True
)

fig_sales.update_layout(
    xaxis_title="Date",
    yaxis_title="Units Sold",
    hovermode="x unified",
    height=420
)

st.plotly_chart(
    fig_sales,
    use_container_width=True,
    key="daily_sales_trend"
)

# ---------------- CATEGORY ANALYSIS ----------------
left, right = st.columns(2)

with left:
    st.subheader("🏷️ Sales by Category")

    category_sales = (
        filtered_df.groupby("cat_id", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="cat_id",
        y="sales",
        title="Total Units Sold by Category",
        template="plotly_white"
    )

    st.plotly_chart(fig_category, use_container_width=True)

with right:
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("item_id", as_index=False)["sales"]
        .sum()
        .nlargest(10, "sales")
        .sort_values("sales")
    )

    fig_products = px.bar(
        top_products,
        x="sales",
        y="item_id",
        orientation="h",
        title="Best-Selling Products",
        template="plotly_white"
    )

    st.plotly_chart(fig_products, use_container_width=True)

# ---------------- STORE ANALYSIS ----------------
st.subheader("🏬 Sales by Store")

store_sales = (
    filtered_df.groupby("store_id", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

fig_store = px.bar(
    store_sales,
    x="store_id",
    y="sales",
    title="Store Performance",
    template="plotly_white"
)

st.plotly_chart(fig_store, use_container_width=True)

# ---------------- INVENTORY PERFORMANCE ----------------
st.divider()
st.header("📦 Inventory Optimization")

if not inventory.empty:
    required_columns = {
        "id",
        "total_demand",
        "fulfilled_demand",
        "unmet_demand",
        "fill_rate_pct",
        "average_inventory",
        "total_orders"
    }

    if required_columns.issubset(inventory.columns):
        total_demand = inventory["total_demand"].sum()
        fulfilled = inventory["fulfilled_demand"].sum()
        unmet = inventory["unmet_demand"].sum()

        overall_fill_rate = (
            fulfilled / total_demand * 100
            if total_demand > 0 else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Demand", f"{total_demand:,.0f}")
        c2.metric("Fulfilled", f"{fulfilled:,.0f}")
        c3.metric("Unmet Demand", f"{unmet:,.0f}")
        c4.metric("Overall Fill Rate", f"{overall_fill_rate:.2f}%")

        inventory_chart = inventory.nlargest(15, "unmet_demand")

        fig_stockout = px.bar(
            inventory_chart.sort_values("unmet_demand"),
            x="unmet_demand",
            y="id",
            orientation="h",
            title="15 Products with Highest Unmet Demand",
            labels={
                "unmet_demand": "Unmet Demand (Units)",
                "id": "Item-Store Combination"
            },
            template="plotly_white"
        )

        st.plotly_chart(fig_stockout, use_container_width=True)

        st.caption(
            "Inventory metrics are from the historical simulation, "
            "not live inventory data."
        )
    else:
        st.warning("The inventory results file has an unexpected structure.")
else:
    st.info("Inventory simulation results are not available yet.")

# ---------------- DATA TABLE ----------------
with st.expander("🔎 Explore Filtered Sales Data"):
    st.dataframe(
        filtered_df.head(1000),
        use_container_width=True
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Retail Demand Intelligence | Built with Python, Pandas, "
    "Streamlit and Plotly"
)
