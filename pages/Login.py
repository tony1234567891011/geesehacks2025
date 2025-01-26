import streamlit as st

# Streamlit UI
st.title("Login")

# User input for login
with st.form(key="login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Form submission
    submit_button = st.form_submit_button(label="Login")

if submit_button:
    # Example credentials validation (in a real app, you would validate against a database)
    if username == "user" and password == "pass":
        st.success("Logged in successfully!")
    else:
        st.error("Invalid username or password. Please try again.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Sign Up", "Journal", "Gym", "Meditate", "French Duolingo"])

