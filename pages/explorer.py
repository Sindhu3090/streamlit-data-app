# [SOLUTION]
import streamlit as st

from src.data import load_orders
from src.filters import apply_filters, init_filter_state, render_filter_sidebar


def summarize_order(df, order_id):
    rows = df[df["Order ID"] == order_id]
    return {
        "lines": int(len(rows)),
        "total_sales": float(rows["Sales"].sum()),
        "total_profit": float(rows["Profit"].sum()),
    }


@st.dialog("Order detail")
def show_order_detail(df, order_id):
    summary = summarize_order(df, order_id)
    st.write(f"**Order {order_id}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Line items", summary["lines"])
    c2.metric("Order sales", f"${summary['total_sales']:,.2f}")
    c3.metric("Order profit", f"${summary['total_profit']:,.2f}")
    st.dataframe(df[df["Order ID"] == order_id], hide_index=True, width="stretch")


init_filter_state()
orders = load_orders()
render_filter_sidebar(orders)
filtered = apply_filters(orders)

st.title("Order Explorer")

if filtered.empty:
    st.warning("No orders match the current filters.")
else:
    st.dataframe(
        filtered,
        hide_index=True,
        width="stretch",
        column_config={
            "Order Date": st.column_config.DateColumn("Order Date"),
            "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
            "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
        },
    )
    order_id = st.selectbox("Inspect an order", filtered["Order ID"].unique())
    if st.button("View order detail"):
        show_order_detail(filtered, order_id)
# [/SOLUTION]
