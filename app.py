import streamlit as st
import os
from google.generativeai import genai

#testing Jason's commit
genai.configure(api_key=os.environ["AIzaSyDwVFHhjS6X8wxoLmFgi7Y4oq2gPBEatMY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Testing input")

prompt = st.text_input("Enter your prompt: ")

if len(prompt) > 10: # Check if prompt:
    # st.write("Prompt is longer than 10 characters")
    response = model.generate(prompt)
    st.write(response)
else:
    st.write("Prompt is shorter than 10 characters")