import streamlit as st

from src.data import load_orders
from src.filters import init_filter_state, render_filter_sidebar, apply_filters

init_filter_state()
orders = load_orders()

render_filter_sidebar(orders)

filtered = apply_filters(orders)

st.title("Customer Detail")

if filtered.empty:
    st.warning("No data after applying filters.")
    st.stop()


customers = sorted(orders["Customer Name"].unique())
customer = st.selectbox("Select Customer", customers)


customer_df = filtered[filtered["Customer Name"] == customer]

if customer_df.empty:
    st.warning("No data for this customer under current filters.")
    st.stop()

orders_count = customer_df["Order ID"].nunique()
total_sales = customer_df["Sales"].sum()

top_category = (
    customer_df.groupby("Category")["Sales"].sum().idxmax()
    if not customer_df.empty else "N/A"
)

col1, col2, col3 = st.columns(3)
col1.metric("Orders", orders_count)
col2.metric("Total Sales", f"${total_sales:,.2f}")
col3.metric("Top Category", top_category)

st.dataframe(customer_df, hide_index=True, width="stretch")
