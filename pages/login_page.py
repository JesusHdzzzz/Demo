import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"])

client = init_connection()
db = client.HackathonX
users_collection = db.users

st.title("Login")

email = st.text_input("Email")
st.write(email)

password = st.text_input("Password")
st.write(password)