
# [SOLUTION]
import streamlit as st


def active_rate(active, total):
    if total == 0:
        return 0.0
    return active / total


def format_percent(value):
    return f"{value:.1%}"


st.set_page_config(page_title="Sales Insights", layout="wide")

st.image("assets/app_banner.png", width="stretch")

st.title("Sales Insights")

st.markdown(
    """
    Use this app to review customer activity and prepare for deeper analysis.
    More views - tables, filters, and charts - will be added as the project grows.
    """
)

total_customers = 1250
active_customers = 980
rate = active_rate(active_customers, total_customers)

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Active Customers", f"{active_customers:,}")
col3.metric("Active Rate", format_percent(rate))

st.write("This is the first working version of the application.")
# [/SOLUTION]
