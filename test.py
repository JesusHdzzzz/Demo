import streamlit as st
from pymongo import MongoClient
import certifi

# Replace with your MongoDB Atlas URI from Streamlit secrets
try:
    # Create a MongoDB client instance using the URI from secrets.toml
    client = MongoClient(st.secrets["MONGODB_URI"]["uri"],
                         tlsCAFile=certifi.where())

    # Check if the connection is successful by listing the databases
    st.write("Connection successful!")
    st.write("Databases:", client.list_database_names())  # List all available databases

except Exception as e:
    st.error(f"Error occurred while connecting to MongoDB Atlas: {e}")
