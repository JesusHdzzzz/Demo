import streamlit as st
from pymongo import MongoClient
import certifi

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"], tlsCAFile=certifi.where())

client = init_connection()
db = client.HackathonX
users_collection = db.users

st.title("Your Financial Info")

with st.form("fincancial_info"):
    st.subheader("Income")
    income = float(st.text_input("Your monthly income estimate"))

    st.subheader("Monthly Expenditures")
    st.caption("Note: Enter '0' if none spent in area.")
    food = float(st.text_input("Food"))
    housing = float(st.text_input("Rent/Mortgage"))
    utilities = float(st.text_input("Utilities"))
    transportation = float(st.text_input("Transportation"))
    entertainment = float(st.text_input("Entertainment"))
    other = float(st.text_input("Other"))

    submitted = st.form_submit_button("Done")

    if submitted:
        if not all([income, food, housing, utilities, transportation, entertainment, other]):
            st.error("Please fill in all fields.")
        elif isinstance(food, float) == False or isinstance(housing, float) == False or \
            isinstance(utilities, float) == False or isinstance(transportation, float) == False or \
            isinstance(entertainment, float) == False or isinstance(other, float) == False:
            st.error("Please enter only numbers.")
        else:
            total_spending = food + housing + utilities + transportation + entertainment + other
            remaining = income - total_spending
            user_data = {
                "income": income,
                "food": food,
                "housing": housing,
                "utilities": utilities,
                "transportation": transportation,
                "entertainment": entertainment,
                "other": other,
                "total spending": total_spending,
                "remaining": remaining
                #"created_at": datetime.datetime.utcnow()
            }

            try:
                result = users_collection.insert_one(user_data)
                st.success(f"User created! ID: {result.inserted_id}")
                st.switch_page("pages/login_page.py")
            except Exception as e:
                st.error(f"Error saving to database: {e}")