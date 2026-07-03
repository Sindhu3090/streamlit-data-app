import requests
import streamlit as st

from src.api import fetch_rates
from src.database import query_orders

st.title("External Data")

# -----------------------------
# Database
# -----------------------------
st.subheader("Sales by region (from the database)")

try:
    db_orders = query_orders(
        "SELECT region, SUM(sales) AS sales, SUM(profit) AS profit "
        "FROM orders GROUP BY region ORDER BY sales DESC"
    )
    st.dataframe(db_orders, hide_index=True, width="stretch")
except Exception:
    st.error("Could not read the database. Confirm data/superstore.db exists.")

# -----------------------------
# API
# -----------------------------
st.subheader("Live currency rates")

if st.button("Refresh rates"):
    fetch_rates.clear()

st.caption(
    "Exchange rates are cached for up to 1 hour. "
    "Click 'Refresh rates' to fetch the latest values."
)

try:
    rates_url = st.secrets["api"]["rates_url"]
except Exception:
    rates_url = None

if not rates_url:
    st.info("Add api.rates_url to .streamlit/secrets.toml to enable live rates.")
else:
    try:
        rates = fetch_rates(rates_url)
        st.dataframe(rates, hide_index=True, width="stretch")

    except requests.exceptions.Timeout:
        st.warning(
            "The rates service is taking too long to respond. Please try again later."
        )

    except requests.exceptions.RequestException:
        st.error(
            "Could not reach the rates service right now. Please try again later."
        )
