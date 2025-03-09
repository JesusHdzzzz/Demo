import streamlit as st
from pymongo import MongoClient
import certifi
import google.generativeai as genai

@st.cache_resource
def init_connection():
    try:
        # Initialize connection with diagnostics
        client = MongoClient(
            st.secrets["MONGODB_URI"]["uri"],
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000  # Fail fast for quicker feedback
        )
        
        # Immediate connection test
        client.admin.command('ping')
        st.toast("✅ Successfully connected to MongoDB!", icon="🔗")
        return client
        
    except Exception as e:
        st.error(f"""
        **MongoDB Connection Failed**
        Error: {str(e)}
        
        Troubleshooting Steps:
        1. Verify MongoDB URI in secrets
        2. Check network access in Atlas
        3. Confirm internet connection
        """)
        st.stop()  # Halt entire app if connection fails

client = init_connection()
db = client.HackathonX
users_collection = db.users
finances_collection = db.finances

st.title("Your Financial Info")

if "user_email" not in st.session_state:
    st.error("Please log in first.")
    st.stop()

current_user = users_collection.find_one({"email": st.session_state.user_email})
if not current_user:
    st.error("User not found.")
    st.stop()

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
            try:
                income_val = float(income)
                expenses = {
                    "food": float(food),
                    "housing": float(housing),
                    "utilities": float(utilities),
                    "transportation": float(transportation),
                    "entertainment": float(entertainment),
                    "other": float(other)
                }

                total_spending = sum(expenses.values())
                remaining = income_val - total_spending

                financial_data = {
                    "user_id": current_user["_id"],
                    "income": income_val,
                    "expenses": expenses,
                    "total_spending": total_spending,
                    "remaining": remaining,
                    #"created_at": datetime.datetime.utcnow()
                }

                result = finances_collection.insert_one(financial_data)

                st.success(f"Data saved successfully! ID: {result.inserted_id}")
                st.balloons()
                st.switch_page("pages/page.py")
            except ValueError:
                st.error("Please enter a valid number in all fields.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
