import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Burger Town — Sales Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS for Premium Design
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global styles */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }
    
    /* Card Container */
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6c757d;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1a1d20;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    
    .kpi-subtext {
        font-size: 0.8rem;
        color: #28a745;
        font-weight: 500;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eaeaea;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading with Cache
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df["Order_Datetime"] = pd.to_datetime(df["Order_Datetime"])
    df["Revenue"] = df["Price"] * df["Quantity"]
    return df

with st.spinner("Loading dataset..."):
    df = load_data()

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/emoji/96/hamburger-emoji.png", width=64)
st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("---")

# 1. Outlet Filter
available_outlets = ["All"] + sorted(df["Outlet_Name"].dropna().unique().tolist())
selected_outlet = st.sidebar.selectbox("Select Outlet", available_outlets)

# 2. Order Type Filter
available_order_types = ["All"] + sorted(df["Order_Type"].dropna().unique().tolist())
selected_order_type = st.sidebar.selectbox("Select Order Type", available_order_types)

# 3. Date Range Filter
min_date = df["Order_Datetime"].min().date()
max_date = df["Order_Datetime"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date range selection
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: `data.xlsx` | 300,000 Transactions")

# ---------------------------------------------------------
# Data Filtering Logic
# ---------------------------------------------------------
filtered_df = df.copy()

# Date filter
filtered_df = filtered_df[
    (filtered_df["Order_Datetime"].dt.date >= start_date) & 
    (filtered_df["Order_Datetime"].dt.date <= end_date)
]

# Outlet filter
if selected_outlet != "All":
    filtered_df = filtered_df[filtered_df["Outlet_Name"] == selected_outlet]

# Order Type filter
if selected_order_type != "All":
    filtered_df = filtered_df[filtered_df["Order_Type"] == selected_order_type]

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <div>
            <h1 class="header-title">🍔 Burger Town — Sales Analytics Dashboard</h1>
            <div class="header-subtitle">Performance overview, revenue metrics, and sales trend analysis</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
    st.stop()

# ---------------------------------------------------------
# KPI Calculations
# ---------------------------------------------------------
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["BillNo"].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

# Top Outlet Calculation
outlet_rev = filtered_df.groupby("Outlet_Name")["Revenue"].sum()
if not outlet_rev.empty:
    top_outlet = outlet_rev.idxmax()
    top_outlet_revenue = outlet_rev.max()
else:
    top_outlet = "N/A"
    top_outlet_revenue = 0

# ---------------------------------------------------------
# KPI Cards Display
# ---------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">₹{total_revenue:,.2f}</div>
            <div class="kpi-subtext">Across filtered transactions</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-subtext">Unique completed bills</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Order Value</div>
            <div class="kpi-value">₹{avg_order_value:,.2f}</div>
            <div class="kpi-subtext">Revenue per unique bill</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Outlet</div>
            <div class="kpi-value">{top_outlet}</div>
            <div class="kpi-subtext">₹{top_outlet_revenue:,.2f} revenue</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visualizations Section
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns([1, 1])

# Chart 1: Bar Chart - Revenue by Outlet
with row1_col1:
    st.subheader("📊 Revenue by Outlet")
    rev_by_outlet = (
        filtered_df.groupby("Outlet_Name")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=True)
    )
    
    fig_outlet = px.bar(
        rev_by_outlet,
        x="Revenue",
        y="Outlet_Name",
        orientation="h",
        text_auto=".2s",
        color="Revenue",
        color_continuous_scale="Reds",
        labels={"Revenue": "Revenue (₹)", "Outlet_Name": "Outlet"}
    )
    fig_outlet.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="",
        coloraxis_showscale=False,
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="y unified"
    )
    fig_outlet.update_traces(
        texttemplate='₹%{x:,.0f}', 
        textposition='outside'
    )
    st.plotly_chart(fig_outlet, use_container_width=True)

# Chart 3: Donut Chart - Revenue by Category (Group column)
with row1_col2:
    st.subheader("🍩 Revenue by Category (Group)")
    rev_by_category = (
        filtered_df.groupby("Group")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )
    
    fig_donut = px.pie(
        rev_by_category,
        names="Group",
        values="Revenue",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>Share: %{percent}"
    )
    fig_donut.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# Chart 2: Line Chart - Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")

# Group by Month-Year
filtered_df["YearMonth"] = filtered_df["Order_Datetime"].dt.to_period("M").dt.to_timestamp()
monthly_rev = (
    filtered_df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="YearMonth")
)

fig_trend = px.line(
    monthly_rev,
    x="YearMonth",
    y="Revenue",
    markers=True,
    labels={"YearMonth": "Month", "Revenue": "Revenue (₹)"}
)
fig_trend.update_traces(
    line=dict(color="#d97706", width=3),
    marker=dict(size=8, color="#b45309", symbol="circle"),
    hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: ₹%{y:,.2f}<extra></extra>"
)
fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (₹)",
    height=360,
    margin=dict(l=20, r=20, t=30, b=20),
    hovermode="x unified"
)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Top 10 Items Data Table
# ---------------------------------------------------------
st.subheader("🏆 Top 10 Items by Revenue")

top_items = (
    filtered_df.groupby(["Item", "Group"])
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum")
    )
    .reset_index()
    .sort_values(by="Total_Revenue", ascending=False)
    .head(10)
)

# Formatting for presentation
top_items_display = top_items.copy()
top_items_display.columns = ["Item Name", "Category", "Quantity Sold", "Total Revenue (₹)"]

# Apply formatting
top_items_display["Quantity Sold"] = top_items_display["Quantity Sold"].apply(lambda x: f"{x:,}")
top_items_display["Total Revenue (₹)"] = top_items_display["Total Revenue (₹)"].apply(lambda x: f"₹{x:,.2f}")

st.dataframe(
    top_items_display,
    use_container_width=True,
    hide_index=True
)
