import streamlit as st

st.title("Login")

email = st.text_input("Email")
st.write(email)

password = st.text_input("Password")
st.write(password)