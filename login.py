import streamlit as st
import os

st.title("THE BEST BUDGETING APP!!")

switch = st.button('Login')
if switch:
    st.switch_page("pages/page.py")