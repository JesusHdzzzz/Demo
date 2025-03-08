import streamlit as st
import plotly.express as px

st.title("Your Budget")

random_x = [100, 2000, 550]
names = ['A', 'B', 'C']
 
fig = px.pie(values=random_x, names=names)
st.plotly_chart(fig, theme=None)