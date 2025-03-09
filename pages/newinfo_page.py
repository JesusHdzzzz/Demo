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
    income = st.text_input("Your monthly income estimate")

    st.subheader("Monthly Expenditures")
    st.caption("Note: Enter '0' if none spent in area.")
    food = st.text_input("Food")
    housing = st.text_input("Rent/Mortgage")
    utilities = st.text_input("Utilities")
    transportation = st.text_input("Transportation")
    entertainment = st.text_input("Entertainment")
    other = st.text_input("Other")

    submitted = st.form_submit_button("Done")

    if submitted:
        if not all([income, food, housing, utilities, transportation, entertainment, other]):
            st.error("Please fill in all fields.")
        elif isinstance(float(food), float) == False or isinstance(float(housing), float) == False or \
                isinstance(float(utilities), float) == False or isinstance(float(transportation), float) == False or \
                isinstance(float(entertainment), float) == False or isinstance(float(other), float) == False:
            st.error("Please enter only numbers.")
        else:
            total_spending = float(food) + float(housing) + float(utilities) + float(transportation) + \
                                float(entertainment) + float(other)
            remaining = float(income) - total_spending
            user_data = {
                "income": float(income),
                "food": float(food),
                "housing": float(housing),
                "utilities": float(utilities),
                "transportation": float(transportation),
                "entertainment": float(entertainment),
                "other": float(other),
                "total spending": float(total_spending),
                "remaining": float(remaining)
                #"created_at": datetime.datetime.utcnow()
            }

            try:
                result = users_collection.insert_one(user_data)
                st.success("Financial info saved!")
                st.switch_page("pages/page.py")
            except Exception as e:
                st.error(f"Error saving to database: {e}")