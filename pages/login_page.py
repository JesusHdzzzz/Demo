import streamlit as st
import sqlite3

conn = sqlite3.connect('../data.db')
c = conn.cursor()


c.execute('''Create TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, usertype TEXT, username TEXT, password TEXT)''')
conn.commit()

c.execute("INSERT INTO users (id, usertype, username, password) VALUES ('1', 'admin', 'admin', 'password')")
conn.commit()

st.title("Login")

email = st.text_input("Email")
# st.write(email)

password = st.text_input("Password", type="password")
# st.write(password)


if st.button("Login"):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (email, password))
    user = c.fetchone()

    if user:
        st.success("Login Successful")
    else:
        st.error("Invalid Email or Password")

conn.close()