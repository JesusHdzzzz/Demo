import plotly.express as px
import streamlit as st
import pandas as pd

st.title("Your Budget")

left, center, right = st.columns(3)

with right:
    random_x = [100, 2000, 550]
    names = ['A', 'B', 'C']
    
    fig = px.pie(values=random_x, names=names)
    st.plotly_chart(fig, theme=None)