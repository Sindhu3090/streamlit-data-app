# [SOLUTION]
import sqlite3

import pandas as pd
import streamlit as st


@st.cache_data(ttl=600)
def query_orders(
    query="SELECT region, category, sales, profit FROM orders",
    db_path="data/superstore.db",
):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)
# [/SOLUTION]
