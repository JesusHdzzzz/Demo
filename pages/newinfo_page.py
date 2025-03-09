import streamlit as st
from pymongo import MongoClient
import certifi
import google.generativeai as genai

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