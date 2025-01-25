import streamlit as st

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

if submit_button:
    if password == confirm_password:
        st.success("Account created successfully!")
    else:
        st.error("Passwords do not match. Please try again.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Journal", "Gym", "Meditate", "French Duolingo"])

# Placeholder for other pages
if page == "Main":
    st.write("Welcome to the Main page!")
elif page == "Journal":
    st.write("Welcome to the Journal page!")
elif page == "Gym":
    st.write("Welcome to the Gym page!")
elif page == "Meditate":
    st.write("Welcome to the Meditate page!")
elif page == "French Duolingo":
    st.write("Welcome to the French Duolingo page!")
