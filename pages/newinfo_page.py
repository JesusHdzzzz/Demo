import streamlit as st
from pymongo import MongoClient
import certifi
import google.generativeai as genai

connection_status = st.empty()

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"],
    tlsCAFile=certifi.where())  # Halt entire app if connection fails

try:
    client = init_connection()
    #st.toast("Connection successful!", icon="✅")
except ConnectionError as e:
    #st.toast(f"Connection failed: {str(e)}", icon="🚫")
    st.stop()

db = client.HackathonX
finances_collection = db.finances
users_collection = db.users

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
#Sidebar Chat START
api_key = st.secrets["GEMINI_API_KEY"]["api_key"]
tlsCAFile=certifi.where()
if not api_key:
    st.error("API key is not set. Please set the API key in your environment variables.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Only answer questions about finance, refuse unrelated questions.")

st.title("ChatAI")
with st.sidebar:
    st.header("Chat with AI")
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask a finance question: ")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "bot", "content": response.text})
            with st.chat_message("bot"):
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")