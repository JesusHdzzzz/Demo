import streamlit as st
import os

st.title("THE BEST BUDGETING APP!!!")

switch_login = st.button('pages/Login')
if switch_login:
    st.switch_page("pages/page.py")

switch_signup = st.button('Sign Up')
if switch_signup:
    st.switch_page("page.py")