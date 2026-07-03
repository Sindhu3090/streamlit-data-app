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

def summary_stats(df):

    top_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    avg_sales = df["Sales"].mean()

    return top_region, top_category, avg_sales

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

top_region, top_category, avg_sales = summary_stats(filtered)

category_region = (
    filtered.groupby(["Region", "Category"], as_index=False)["Sales"]
    .sum()
)

c1, c2, c3 = st.columns(3)

c1.metric("Top Region", top_region)

c2.metric("Top Category", top_category)

c3.metric(
    "Average Sale",
    f"${avg_sales:,.2f}"
)

view = st.segmented_control(
    "Chart", ["Monthly trend", "Sales by region", "Sales vs profit", "By region & category",],
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

elif view == "By region & category":
    st.subheader("Sales by Region & Category")
    fig = px.bar(
        category_region,
        x="Category",
        y="Sales",
        color="Category",
        facet_col="Region",
        title="Sales by Category Across Regions",
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
