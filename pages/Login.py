import streamlit as st

from database import check_user

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

    user_id = check_user(username, password)
    if user_id:
        st.success(f"Seccess your user_id: {user_id}")
        st.write(f"(http://localhost:8501/ProfilePage?user_id={user_id})")
    else:
        st.error("fail")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Sign Up", "Journal", "Gym", "Meditate", "French Duolingo"])