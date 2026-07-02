import streamlit as st


def active_rate(active, total):
    if total == 0:
        return 0.0
    return active / total


def format_percent(value):
    return f"{value:.1%}"


def render_header(title, description, metrics):
    st.image("assets/app_banner.png", width="stretch")
    st.title(title)
    st.markdown(description)

    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label, value)


st.set_page_config(page_title="Sales Insights", layout="wide")

with st.sidebar:
    st.header("Filters")
    st.write("Filters will appear here.")

total_customers = 1250
active_customers = 980

metrics = {
    "Total Customers": f"{total_customers:,}",
    "Active Customers": f"{active_customers:,}",
    "Active Rate": format_percent(
        active_rate(active_customers, total_customers)
    ),
}

render_header(
    title="Sales Insights",
    description="""
Use this app to review customer activity and prepare for deeper analysis.
More views - tables, filters, and charts - will be added as the project grows.
""",
    metrics=metrics,
)

st.write("This is the first working version of the application.")