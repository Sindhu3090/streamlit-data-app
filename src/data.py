# [SOLUTION]
import pandas as pd
import streamlit as st


@st.cache_data
def load_orders(path="data/superstore.csv"):
    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    return df
# [/SOLUTION]
