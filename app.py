# CORRECT IMPORTS
import google.generativeai as genai
import streamlit as st

# Initialize Gemini client
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])  # Use Streamlit secrets for security!

st.write("""
# My first app
I have deployed my first app using Streamlit*
""")

# Generate response
model = genai.GenerativeModel('gemini-pro')  # Use valid model name
response = model.generate_content("Explain how AI works")

# Display output safely
try:
    st.write(response.text)
except Exception as e:
    st.error(f"Error generating response: {e}")