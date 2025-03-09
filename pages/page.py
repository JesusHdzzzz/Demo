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

left, center, right = st.columns([0.5, 3, 0.5], vertical_alignment="center")

#Sidebar Chat START
api_key = st.secrets["GEMINI_API_KEY"]["api_key"]
tlsCAFile=certifi.where()
if not api_key:
    st.error("API key is not set. Please set the API key in your environment variables.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="You are a finance instructor. Only answer questions about finance, refuse unrelated questions.")

with st.sidebar:
    st.header("Chat with AI")
    # Initialize messages
    if "balance" not in st.session_state:
        st.session_state.balance = 20
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

prompt = st.chat_input("Ask a finance question: ")

with st.sidebar:
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        system_instruction= f"""You are a finance instructor. 
                                Only answer questions about finance, refuse unrelated questions. 
                                If a user mention spending money, record that value and ONLY that value as a negative value. 
                                If a user mention gaining money, record that value and ONLY that value as a postive value. 
                                If a user ask about their balance, return zero as a int. 
                                If no spending is mentioned, respond normally."""
        try:
            response = model.generate_content(
                system_instruction + f"\nUser input: {prompt}"
            ).text.strip()

            # ✅ Step 8: Process AI's response & update balance if money is spent
            try:
                spent_amount = float(response)  # Convert response to number
                st.session_state.balance += spent_amount  # Deduct from balance
                if spent_amount == 0:
                    ai_response = f"Your current balance is **${st.session_state.balance}**."
                else: 
                    ai_response = f"Got it. Your new balance is **${st.session_state.balance}**."
            except ValueError:
                ai_response = response  # If no number was detected, return normal AI response

            st.session_state.messages.append({"role": "bot", "content": ai_response})
            with st.chat_message("bot"):
                st.write(ai_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

with center:
    random_x = [user_expenses["food"], user_expenses["housing"], user_expenses["utilities"], user_expenses["transportation"], user_expenses["entertainment"], user_expenses["other"]]
    names = ['Food', 'Housing', 'Utilities', 'Transportation', 'Entertainment', 'Other']
    
    fig = px.pie(values=random_x, names=names)
    st.plotly_chart(fig, theme=None)

    income = user_match["income"]
    total = user_match["total_spending"]
    remaining = user_match["remaining"]

    st.write(f"Income: ${income}")
    st.write(f"Total Expenditure: ${total}")
    st.write(f"Money Remaining: ${remaining}")