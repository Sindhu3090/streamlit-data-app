# [SOLUTION]
import streamlit as st

FILTER_DEFAULTS = {"search": "", "region": "All", "category": "All"}

def reset_filters():
    for key, value in FILTER_DEFAULTS.items():
        st.session_state[f"flt_{key}"] = value

def init_filter_state():
    for key, value in FILTER_DEFAULTS.items():
        if f"flt_{key}" not in st.session_state:
            st.session_state[f"flt_{key}"] = value


def render_filter_sidebar(orders):
    st.sidebar.header("Filters")

    st.sidebar.button("Reset filters", on_click=reset_filters)

    st.sidebar.text_input("Search customer or product", key="flt_search")

    st.sidebar.selectbox(
        "Region",
        ["All"] + sorted(orders["Region"].unique()),
        key="flt_region"
    )

    st.sidebar.selectbox(
        "Category",
        ["All"] + sorted(orders["Category"].unique()),
        key="flt_category"
    )


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


def apply_filters(df):
    return filter_orders(
        df,
        st.session_state.get("flt_search", ""),
        st.session_state.get("flt_region", "All"),
        st.session_state.get("flt_category", "All"),
    )
# [/SOLUTION]
