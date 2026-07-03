# [SOLUTION]
import altair as alt
import plotly.express as px
import streamlit as st

from src.data import load_orders
from src.filters import apply_filters, init_filter_state, render_filter_sidebar


@st.fragment
def chart_panel(filtered):
    view = st.segmented_control(
        "Chart", ["Monthly trend", "Sales by region", "Sales vs profit"],
        default="Monthly trend",
    )

    if view == "Monthly trend":
        data = (
            filtered.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
        )
        st.line_chart(data, x="Order Date", y="Sales")

    elif view == "Sales by region":
        data = (
            filtered.groupby("Region", as_index=False)["Sales"].sum()
            .sort_values("Sales", ascending=False)
        )
        st.plotly_chart(
            px.bar(data, x="Region", y="Sales", title="Sales by Region"),
            width="stretch",
        )

    else:
        scatter = (
            alt.Chart(filtered)
            .mark_circle(size=60, opacity=0.5)
            .encode(
                x=alt.X("Sales:Q"),
                y=alt.Y("Profit:Q"),
                color=alt.Color("Category:N"),
                tooltip=["Customer Name:N", "Sales:Q", "Profit:Q"],
            )
        )
        st.altair_chart(scatter, width="stretch")


init_filter_state()
orders = load_orders()
render_filter_sidebar(orders)
filtered = apply_filters(orders)

st.title("Dashboard")

if filtered.empty:
    st.warning("No orders match the current filters.")
else:
    chart_panel(filtered)
# [/SOLUTION]
