import streamlit as st
import os
from google.generativeai import GenerativeModel

#testing Jason's commit

st.title("Testing input")

prompt = st.text_input("Enter your prompt: ")

if len(prompt) > 10: # Check if prompt:
    st.write("Prompt is longer than 10 characters")
else:
    st.write("Prompt is shorter than 10 characters")