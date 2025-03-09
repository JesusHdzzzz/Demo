import streamlit as st

st.title("Your Financial Info")

st.subheader("Income")
income = st.text_input("Your monthly income estimate")

st.subheader("Monthly Expenditures")
food = st.text_input("Food")
housing = st.text_input("Rent/Mortgage")
utilities = st.text_input("Utilities")
transportation = st.text_input("Transportation")
entertainment = st.text_input("Entertainment")
other = st.text_input("Other")