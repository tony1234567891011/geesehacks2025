import streamlit as st
from pages import page1, page2

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Jounral", "Gym", "Meditate", "French Duolingo"])

# Page selection
if page == "Page 1":
    page1.show()
elif page == "Page 2":
    page2.show()