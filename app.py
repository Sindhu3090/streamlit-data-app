# [SOLUTION]
import pandas as pd
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


st.set_page_config(page_title="Order Explorer", layout="wide")
st.title("Order Explorer")

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
else:
    st.dataframe(
        filtered,
        hide_index=True,
        width="stretch",
        column_config={
            "Order Date": st.column_config.DateColumn("Order Date"),
            "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
            "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
            "Quantity": st.column_config.NumberColumn("Quantity"),
        },
    )

    st.subheader("Edit a sample of orders")
    st.caption("Edits apply only to the current session - they do not change the source file.")
    edited = st.data_editor(
        filtered.head(20),
        hide_index=True,
        width="stretch",
        column_config={
            "Order ID": st.column_config.TextColumn("Order ID", disabled=True),
            "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
        },
    )
# [/SOLUTION]
