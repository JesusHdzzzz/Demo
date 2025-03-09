import streamlit as st
import os
import google.generativeai as genai
import certifi

#testing Jason's commit
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

#Chat container
    chat_container = st.container()
    with chat_container:

        for msg in (st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    prompt = st.chat_input("Ask a finance question: ")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        # Get conversation context
        conversation_context = ""
        for msg in st.session_state.messages:
            conversation_context += f"{msg['role']}: {msg['content']}\n"

        # Generate response

        try:
            response = model.generate_content(conversation_context)

            st.session_state.messages.append({"role": "bot", "content": response.text})

            with st.chat_message("bot"):
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

#Sidebar Chat END
