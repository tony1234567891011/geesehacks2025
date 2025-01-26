import streamlit as st
from database import create_user

st.title("📊 Habit Tracker - Build Your Tower")

# User Registration Form
username = st.text_input("Enter your username:")
email = st.text_input("Enter your email:")
password = st.text_input("Enter your password:", type="password")

if st.button("Register"):
    if username and email and password:
        user_id = create_user(username, email, password)  # Call database function
        st.success(f"User {username} registered successfully! (User ID: {user_id})")
    else:
        st.warning("Please fill in all fields.")

# Run Streamlit App
if __name__ == "__main__":
    st.write("Welcome to the Habit Tracker!")
