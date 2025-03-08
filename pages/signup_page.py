import streamlit as st

st.title("Sign Up")

email = st.text_input("Email")
st.write(email)

password = st.text_input("Password")
st.write(password)

confirm_password = st.text_input("Confirm Password")
st.write(confirm_password)