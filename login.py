import streamlit as st
import os

style_heading = 'text-align: center'
style_image = 'display: block; margin-left: auto; margin-right: auto; margin-top: 100px' 

st.markdown(f"<h1 style='{style_heading}'>Bobcat Budgeting</h1>", unsafe_allow_html=True)

left, center, right = st.columns([1.8, 1.5, 1.9], vertical_alignment="bottom")

with center:
    colLeft, colRight = st.columns(2, vertical_alignment="bottom")
    with colLeft:
        switch_login = st.button('Login', type="primary")
        if switch_login:
            st.switch_page("pages/login_page.py")
    with colRight:
        switch_signup = st.button('Sign Up', type="primary")
        if switch_signup:
            st.switch_page("pages/signup_page.py")