import plotly.express as px
import streamlit as st
import pandas as pd
import certifi
import google.generativeai as genai

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["MONGODB_URI"]["uri"],
    tlsCAFile=certifi.where())

client = init_connection()
db = client.HackathonX
users_collection = db.users
finance_collection = db.finances

current_user = users_collection.find_one({"email": st.session_state.user_email})
user_match = finance_collection.find_one({"user_id": current_user["_id"]})
user_expenses = user_match["expenses"]

st.title("Your Budget")

left, center, right = st.columns([2, 1, 1])

with left:
    expenses = [100, 2000, 550]
    names = ['A', 'B', 'C']
    
    fig = px.pie(values=random_x, names=names)
    st.plotly_chart(fig, theme=None)

#Sidebar Chat START
api_key = st.secrets["GEMINI_API_KEY"]["api_key"]
tlsCAFile=certifi.where()
if not api_key:
    st.error("API key is not set. Please set the API key in your environment variables.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Only answer questions about finance, refuse unrelated questions.")

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