import streamlit as st
import os

left, center, right = st.columns([2, 2, 1], vertical_alignment="bottom", border=True)

style_heading = 'text-align: center'
style_image = 'display: block; margin-left: auto; margin-right: auto; margin-top: 100px' 

with st.container():
    st.markdown(f"<h1 style='{style_heading}'>Bobcat Budgeting</h1>", unsafe_allow_html=True)

    switch_login = st.button('Login')
    if switch_login:
        st.switch_page("pages/login_page.py")

    switch_signup = st.button('Sign Up')
    if switch_signup:
        st.switch_page("pages/signup_page.py")