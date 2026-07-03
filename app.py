# [SOLUTION]
import streamlit as st

st.set_page_config(page_title="Sales App", layout="wide")

overview = st.Page("pages/overview.py", title="Overview", icon=":material/home:")
explorer = st.Page("pages/explorer.py", title="Explorer", icon=":material/table_view:")
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/insights:")
customer = st.Page("pages/customer.py", title="Customer", icon=":material/person:")

pg = st.navigation([overview, explorer, dashboard, customer])
pg.run()
# [/SOLUTION]
