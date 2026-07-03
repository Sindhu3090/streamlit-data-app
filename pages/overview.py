# [SOLUTION]
import streamlit as st

from src.data import load_orders
from src.filters import apply_filters, init_filter_state, render_filter_sidebar

init_filter_state()
orders = load_orders()
render_filter_sidebar(orders)
filtered = apply_filters(orders)

st.title("Overview")
st.write("Filters in the sidebar apply across every page - change one, then switch pages.")

col1, col2, col3 = st.columns(3)
col1.metric("Orders", f"{len(filtered):,}")
col2.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col3.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
# [/SOLUTION]
