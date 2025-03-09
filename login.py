import streamlit as st
import os

st.title("Bobcat Budgeting")

left, center, right = st.columns(3)

with center:
    switch_login = st.button('Login')
    if switch_login:
        st.switch_page("pages/login_page.py")

    switch_signup = st.button('Sign Up')
    if switch_signup:
        st.switch_page("pages/signup_page.py")