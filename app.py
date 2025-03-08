import google.generateai as genai
import streamlit as st

genai.configure(api_key="AIzaSyDwVFHhjS6X8wxoLmFgi7Y4oq2gPBEatMY")

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