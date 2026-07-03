# [SOLUTION]
import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def load_orders(path="data/superstore.csv"):
    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    return df


def filter_orders(df, search="", region="All", category="All"):
    result = df
    if search:
        mask = (
            result["Customer Name"].str.contains(search, case=False, na=False)
            | result["Product Name"].str.contains(search, case=False, na=False)
        )
        result = result[mask]
    if region != "All":
        result = result[result["Region"] == region]
    if category != "All":
        result = result[result["Category"] == category]
    return result


def sales_by_region(df):
    return (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


def monthly_sales(df):
    return (
        df.set_index("Order Date")
        .resample("MS")["Sales"]
        .sum()
        .reset_index()
    )


st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard")

orders = load_orders()

st.sidebar.header("Filters")
search = st.sidebar.text_input("Search customer or product")
region = st.sidebar.selectbox("Region", ["All"] + sorted(orders["Region"].unique()))
category = st.sidebar.selectbox("Category", ["All"] + sorted(orders["Category"].unique()))

filtered = filter_orders(orders, search, region, category)

col1, col2, col3 = st.columns(3)
col1.metric("Orders", f"{len(filtered):,}")
col2.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col3.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")

if filtered.empty:
    st.warning("No orders match the current filters. Try clearing a filter.")
    st.stop()

view = st.segmented_control(
    "Chart", ["Monthly trend", "Sales by region", "Sales vs profit"],
    default="Monthly trend",
)

if view == "Monthly trend":
    st.subheader("Monthly Sales Trend")
    st.line_chart(monthly_sales(filtered), x="Order Date", y="Sales")

elif view == "Sales by region":
    st.subheader("Sales by Region")
    fig = px.bar(
        sales_by_region(filtered),
        x="Region", y="Sales",
        title="Total Sales by Region",
        labels={"Sales": "Total Sales"},
    )
    st.plotly_chart(fig, width="stretch")

else:
    st.subheader("Sales vs Profit")
    scatter = (
        alt.Chart(filtered)
        .mark_circle(size=60, opacity=0.5)
        .encode(
            x=alt.X("Sales:Q", title="Sales"),
            y=alt.Y("Profit:Q", title="Profit"),
            color=alt.Color("Category:N", title="Category"),
            tooltip=["Customer Name:N", "Sales:Q", "Profit:Q", "Region:N"],
        )
    )
    st.altair_chart(scatter, width="stretch")
# [/SOLUTION]
