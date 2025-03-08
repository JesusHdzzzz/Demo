from google import genai
import streamlit as st

client = genai.Client(api_key="AIzaSyDwVFHhjS6X8wxoLmFgi7Y4oq2gPBEatMY")

st.write("""
# My first app
I have deployed my first app using Streamlit*
""")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

st.write(response.text)