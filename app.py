import streamlit as st
import os
from google.generativeai import GenerativeModel

os.environ.get("AIzaSyDwVFHhjS6X8wxoLmFgi7Y4oq2gPBEatMY")

model = GenerativeModel('gemini-pro')

st.title("Gemini Chatbot")

prompt = st.text_input("Enter your prompt: Explain how AI works")

if prompt:
    # Send prompt to Gemini API
    response = model.generate_content(prompt)

    # Display response
    st.write("Gemini:", response.text)