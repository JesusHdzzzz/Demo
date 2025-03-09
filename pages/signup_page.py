import streamlit as st
from pymongo import MongoClient
import certifi

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"],
    tlsCAFile=certifi.where())

client = init_connection()
db = client.HackathonX
users_collection = db.users

st.title("Sign Up")

with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not all([name, email, password]):
            st.error("Please fill in all fields.")
        else:
            user_data = {
                "name": name,
                "email": email,
                "password": password,
                #"created_at": datetime.datetime.utcnow()
            }

            try:
                result = users_collection.insert_one(user_data)
                st.success(f"User created! ID: {result.inserted_id}")
                st.switch_page("pages/login_page.py")
            except Exception as e:
                st.error(f"Error saving to database: {e}")

#email = st.text_input("Email")
#st.write(email)
#
#password = st.text_input("Password")
#st.write(password)
#
#confirm_password = st.text_input("Confirm Password")
#st.write(confirm_password)