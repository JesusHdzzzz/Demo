import streamlit as st

login_page = st.page("login.py", title="Login")
other_page = st.page("page.py", title="other page")

pg = st.navigation([login_page, other_page])
pg.run()