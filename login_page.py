import streamlit as st
from pymongo import MongoClient
import certifi
import bcrypt
import datetime

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"],
    tlsCAFile=certifi.where())

client = init_connection()
db = client.HackathonX
users_collection = db.users

style_heading = 'text-align: center; font-size:80px'

st.markdown(f"<h1 style='{style_heading}'>Bobcat Budgeting</h1>", unsafe_allow_html=True)

st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")

st.title("Login / Sign Up")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

with login_tab:
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
                    if bcrypt.checkpw(password.encode('utf-8'), user["password_hash"]):
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        #st.session_state.userid = usrID
                        st.success("Login successful!")
                        st.switch_page("pages/app.py")  # Update with your main page path
                    else:
                        st.error("Incorrect password")

with signup_tab:
    with st.form("signup_form"):
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account")

        if submitted:
            try:
                if not all([new_email, new_password, confirm_password]):
                    raise ValueError("Please fill in all fields")
                
                if new_password != confirm_password:
                    raise ValueError("Passwords do not match")
                
                if users_collection.find_one({"email": new_email}):
                    raise ValueError("Email already exists")
                
                # Hash password with bcrypt
                hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                users_collection.insert_one({
                    "email": new_email,
                    "password_hash": hashed_pw,
                    "created_at": datetime.datetime.utcnow()
                })
                
                st.success("Account created successfully! Please login.")
                
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Signup failed: {str(e)}")

if st.session_state.logged_in:
    st.write(f"Logged in as: {st.session_state.user_email}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()