import streamlit as st
import os
import google.generativeai as genai

#testing Jason's commit
api_key = os.environ.get("API_KEY")
if not api_key:
    st.error("API key is not set. Please set the API key in your environment variables.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Only answer questions about finance, refuse unrelated questions.")

st.title("Testing inputs")

prompt = st.text_input("Enter your prompt: ")

if len(prompt) > 10: # Check if prompt:
    # st.write("Prompt is longer than 10 characters")
    try:
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.write("Prompt is shorter than 10 characters")