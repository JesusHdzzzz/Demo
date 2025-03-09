import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"])

client = init_connection()
db = client.HackathonX
users_collection = db.users

st.title("Login")

with st.form("user_login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        if not all([email, password]):
            st.error("Please fill out all the fields.")
        else:
            # check if the user exists
            user = users_collection.find_one({"email": email})

            if not user:
                st.error("User not found! Please sign up first.")
            else:
                # Verify password
                if user["password"] == password:
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    # Redirect to main app page
                    st.switch_page("pages/app.py")
                else:
                    st.error("Incorrect password")

#email = st.text_input("Email")
#st.write(email)
#
#password = st.text_input("Password")
#st.write(password)