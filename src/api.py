# [SOLUTION]
import pandas as pd
import requests
import streamlit as st


def rates_to_frame(payload):
    rates = payload.get("rates", {})
    return pd.DataFrame(
        [{"currency": currency, "rate": rate} for currency, rate in rates.items()]
    )


@st.cache_data(ttl=3600)
def fetch_rates(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return rates_to_frame(response.json())
# [/SOLUTION]
