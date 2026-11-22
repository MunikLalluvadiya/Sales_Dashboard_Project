from src.forecasting import get_monthly_revenue, time_split, train_and_evaluate, forecast_next

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect("database/sales.db")
    query = """
    SELECT s.Order_ID, s.Order_Date, s.Quantity, s.Sales_Amount, s.Payment_Mode,
           c.Customer_ID, c.Customer_Name, c.City, c.Region,
           p.Product_ID, p.Product_Name, p.Category, p.Unit_Price
    FROM Sales s
    INNER JOIN Customers c ON s.Customer_ID = c.Customer_ID
    INNER JOIN Products p  ON s.Product_ID  = p.Product_ID
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

st.sidebar.header("Filters")

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)

regions = sorted(df["Region"].unique())
categories = sorted(df["Category"].unique())
cities = sorted(df["City"].unique())

region_sel = st.sidebar.multiselect("Region", regions, default=regions)
category_sel = st.sidebar.multiselect("Category", categories, default=categories)
city_sel = st.sidebar.multiselect("City", cities, default=cities)

# date_input returns 1 date while the user is still picking the range
if len(date_range) != 2:
    st.warning("Please select both a start and an end date.")
    st.stop()

start, end = date_range

filtered = df[
    (df["Order_Date"].dt.date >= start) &
    (df["Order_Date"].dt.date <= end) &
    (df["Region"].isin(region_sel)) &
    (df["Category"].isin(category_sel)) &
    (df["City"].isin(city_sel))
]

st.title("Interactive Sales Dashboard")

if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

total_revenue = filtered["Sales_Amount"].sum()
total_orders = filtered["Order_ID"].nunique()
total_customers = filtered["Customer_ID"].nunique()
total_quantity = filtered["Quantity"].sum()
avg_order_value = total_revenue / total_orders

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Total Customers", f"{total_customers:,}")
c4.metric("Quantity Sold", f"{total_quantity:,}")
c5.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")



st.subheader("Sales Performance")

monthly = (
    filtered.groupby(filtered["Order_Date"].dt.to_period("M"))["Sales_Amount"]
    .sum().reset_index()
)
monthly["Order_Date"] = monthly["Order_Date"].astype(str)
monthly["Growth %"] = monthly["Sales_Amount"].pct_change() * 100

col1, col2 = st.columns(2)

fig_trend = px.line(monthly, x="Order_Date", y="Sales_Amount",
                    markers=True, title="Monthly Sales Trend",
                    labels={"Order_Date": "Month", "Sales_Amount": "Revenue"})
col1.plotly_chart(fig_trend, width="stretch")

fig_growth = px.bar(monthly.dropna(), x="Order_Date", y="Growth %",
                    title="Month-over-Month Revenue Growth %",
                    labels={"Order_Date": "Month"})
col2.plotly_chart(fig_growth, width="stretch")




col3, col4 = st.columns(2)

# Daily / Weekly sales
period = col3.radio("View sales by", ["Daily", "Weekly"], horizontal=True)
rule = "D" if period == "Daily" else "W"
time_sales = filtered.set_index("Order_Date")["Sales_Amount"].resample(rule).sum().reset_index()

fig_time = px.line(time_sales, x="Order_Date", y="Sales_Amount",
                   title=f"{period} Sales",
                   labels={"Order_Date": "Date", "Sales_Amount": "Revenue"})
col3.plotly_chart(fig_time, width="stretch")

# Year-wise comparison
yearly = filtered.groupby(filtered["Order_Date"].dt.year)["Sales_Amount"].sum().reset_index()
yearly.columns = ["Year", "Revenue"]

fig_year = px.bar(yearly, x="Year", y="Revenue", title="Year-wise Revenue", text_auto=".3s")
fig_year.update_xaxes(type="category")
col4.plotly_chart(fig_year, width="stretch")

if len(yearly) == 2:
    growth = (yearly["Revenue"].iloc[1] - yearly["Revenue"].iloc[0]) / yearly["Revenue"].iloc[0] * 100
    col4.metric("Year-over-Year Growth", f"{growth:.1f}%")





st.subheader("Regional Performance")

region_sales = (
    filtered.groupby("Region")["Sales_Amount"].sum()
    .sort_values(ascending=False).reset_index()
)
city_sales = (
    filtered.groupby("City")["Sales_Amount"].sum()
    .sort_values(ascending=False).reset_index()
)

top_region = region_sales.iloc[0]
low_region = region_sales.iloc[-1]

m1, m2 = st.columns(2)
m1.metric("Top Region", top_region["Region"], f"₹{top_region['Sales_Amount']:,.0f}")
m2.metric("Lowest Region", low_region["Region"], f"₹{low_region['Sales_Amount']:,.0f}", delta_color="off")

col5, col6 = st.columns(2)

fig_region = px.bar(region_sales, x="Region", y="Sales_Amount",
                    title="Region-wise Sales", text_auto=".3s",
                    labels={"Sales_Amount": "Revenue"})
col5.plotly_chart(fig_region, width="stretch")

fig_city = px.bar(city_sales, x="Sales_Amount", y="City", orientation="h",
                  title="City-wise Revenue",
                  labels={"Sales_Amount": "Revenue"})
fig_city.update_yaxes(autorange="reversed")
col6.plotly_chart(fig_city, width="stretch")



st.subheader("Product Performance")

product_rev = (
    filtered.groupby("Product_Name")["Sales_Amount"].sum()
    .sort_values(ascending=False).head(10).reset_index()
)
product_qty = (
    filtered.groupby("Product_Name")["Quantity"].sum()
    .sort_values(ascending=False).head(10).reset_index()
)
category_rev = (
    filtered.groupby("Category")["Sales_Amount"].sum()
    .sort_values(ascending=False).reset_index()
)

col7, col8 = st.columns(2)

fig_qty = px.bar(product_qty, x="Quantity", y="Product_Name", orientation="h",
                 title="Best-Selling Products (Units Sold)")
fig_qty.update_yaxes(autorange="reversed")
col7.plotly_chart(fig_qty, width="stretch")

fig_top = px.bar(product_rev, x="Sales_Amount", y="Product_Name", orientation="h",
                 title="Top 10 Products by Revenue",
                 labels={"Sales_Amount": "Revenue"})
fig_top.update_yaxes(autorange="reversed")
col8.plotly_chart(fig_top, width="stretch")

col9, col10 = st.columns(2)

fig_cat = px.bar(category_rev, x="Category", y="Sales_Amount",
                 title="Category-wise Revenue", text_auto=".3s",
                 labels={"Sales_Amount": "Revenue"})
col9.plotly_chart(fig_cat, width="stretch")

fig_share = px.pie(product_rev, names="Product_Name", values="Sales_Amount",
                   title="Product Sales Contribution (Top 10)")
col10.plotly_chart(fig_share, width="stretch")




st.subheader("Customer Analysis")

customer_summary = (
    filtered.groupby(["Customer_ID", "Customer_Name"])
    .agg(Orders=("Order_ID", "nunique"), Total_Revenue=("Sales_Amount", "sum"))
    .reset_index()
)
customer_summary["Avg_Order_Value"] = (
    customer_summary["Total_Revenue"] / customer_summary["Orders"]
).round(0)

top_customers = customer_summary.sort_values("Total_Revenue", ascending=False).head(10)

col11, col12 = st.columns(2)

fig_cust = px.bar(top_customers, x="Total_Revenue", y="Customer_Name", orientation="h",
                  title="Top 10 Customers by Revenue",
                  labels={"Total_Revenue": "Revenue"})
fig_cust.update_yaxes(autorange="reversed")
col11.plotly_chart(fig_cust, width="stretch")

fig_freq = px.histogram(customer_summary, x="Orders", nbins=20,
                        title="Customer Purchase Frequency",
                        labels={"Orders": "Orders per Customer"})
col12.plotly_chart(fig_freq, width="stretch")

st.markdown("**Customer-wise Order Value**")
st.dataframe(
    customer_summary.sort_values("Total_Revenue", ascending=False)
    [["Customer_Name", "Orders", "Total_Revenue", "Avg_Order_Value"]],
    hide_index=True,
)



st.subheader("Revenue Forecasting")
st.caption("The forecast uses all historical data and is not affected by the sidebar filters.")

monthly_all = get_monthly_revenue(df)
train, test = time_split(monthly_all)
test_pred, mae, rmse = train_and_evaluate(train, test)
future = forecast_next(monthly_all)

# Model evaluation
e1, e2 = st.columns(2)
e1.metric("MAE", f"₹{mae:,.0f}")
e2.metric("RMSE", f"₹{rmse:,.0f}")

col13, col14 = st.columns(2)

# Historical revenue
fig_hist = px.line(monthly_all, x="Month", y="Revenue", markers=True,
                   title="Historical Monthly Revenue")
col13.plotly_chart(fig_hist, width="stretch")

# Predicted revenue (history + next 3 months)
fig_fc = px.line(monthly_all, x="Month", y="Revenue", title="Next 3 Months Forecast")
fig_fc.update_traces(name="Historical", showlegend=True)
fig_fc.add_scatter(x=future["Month"], y=future["Predicted"], mode="lines+markers",
                   name="Forecast", line=dict(dash="dash"))
col14.plotly_chart(fig_fc, width="stretch")

# Actual vs Predicted
fig_avp = px.line(test_pred, x="Month", y=["Revenue", "Predicted"], markers=True,
                  title="Actual vs Predicted Revenue (Test Period)")
st.plotly_chart(fig_avp, width="stretch")

# Forecast table
forecast_table = future[["Month", "Predicted"]].copy()
forecast_table["Month"] = forecast_table["Month"].dt.strftime("%b %Y")
forecast_table["Predicted"] = forecast_table["Predicted"].round(0)
st.dataframe(forecast_table, hide_index=True)

st.info("Note: This forecast is an estimate based on historical data and is not a guaranteed business outcome.")