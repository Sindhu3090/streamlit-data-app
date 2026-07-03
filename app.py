# [SOLUTION]
import streamlit as st

st.set_page_config(page_title="Sales App", layout="wide")

overview = st.Page("pages/overview.py", title="Overview", icon=":material/home:")
explorer = st.Page("pages/explorer.py", title="Explorer", icon=":material/table_view:")
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/insights:")
external = st.Page("pages/external.py", title="External Data", icon=":material/cloud:")

pg = st.navigation([overview, explorer, dashboard, external])
pg.run()
# [/SOLUTION]
