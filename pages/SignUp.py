import streamlit as st

from database import create_user  # Import the create_user function from database.py


# Streamlit UI
st.title("Sign Up")

# User input for sign up
with st.form(key="signup_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Form submission
    submit_button = st.form_submit_button(label="Sign Up")

# Handle form submission
if submit_button:
    if password == confirm_password:
        try:
            # Hash the password (in production, use a secure hashing library like bcrypt)
            password_hash = password  # Replace with hash(password) in a real app
            
            # Save the user to the database
            user_id = create_user(username, email, password_hash)
            
            st.success(f"Account created successfully! Your user ID is {user_id}.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Passwords do not match. Please try again.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Journal", "Gym", "Meditate", "French Duolingo"])

# Add navigation behavior (optional)
if page == "Main":
    st.write("Welcome to the main page!")
elif page == "Journal":
    st.write("This is your Journal page.")
elif page == "Gym":
    st.write("Track your gym activities here.")
elif page == "Meditate":
    st.write("Start your meditation journey.")
elif page == "French Duolingo":
    st.write("Practice French with Duolingo.")
