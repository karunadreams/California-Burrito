# California Burrito / Burger Town — Sales Analytics Dashboard

A Streamlit analytics dashboard for analyzing store sales, orders, revenue, and item-level performance across outlets.

## Features
- **Data Caching**: Fast `@st.cache_data` data loading for 300,000+ transaction records.
- **Dynamic Sidebar Filters**: Filter by Outlet, Order Type (Dine-In, Takeaway, Delivery), and Date Range.
- **KPI Metrics**: Total Revenue (₹), Total Orders, Average Order Value (₹), and Top Outlet by Revenue.
- **Interactive Visualizations (Plotly)**:
  - Revenue by Outlet (Horizontal Bar Chart)
  - Monthly Revenue Trend (Line Chart)
  - Revenue by Category (Donut Chart)
- **Item Performance**: Top 10 items table sorted by revenue.

## Setup & Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/karunadreams/California-Burrito.git
   cd California-Burrito
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Streamlit app**:
   ```bash
   streamlit run app.py
   ```
