import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os
import requests

# Set environment variables or replace with your own Google client details
os.environ["GOOGLE_CLIENT_ID"] = "your-google-client-id"
os.environ["GOOGLE_CLIENT_SECRET"] = "your-google-client-secret"

# Set up Google OAuth2 client
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
token_endpoint = "https://accounts.google.com/o/oauth2/token"
userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"
redirect_uri = "http://localhost:8501"

# Streamlit UI
st.title("Login with Google")

if "token" not in st.session_state:
    if st.button("Login with Google"):
        # OAuth2 session
        oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope="openid email profile")
        authorization_url, state = oauth.create_authorization_url(authorization_endpoint)

        # Save state
        st.session_state["state"] = state
        st.query_params = {"url": authorization_url}

        st.write(f"[Click here to authorize]({authorization_url})")

    params = st.query_params
    if "code" in params:
        code = params["code"][0]
        oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, state=st.session_state["state"])
        token = oauth.fetch_token(token_endpoint, code=code)

        st.session_state["token"] = token

        userinfo_response = requests.get(userinfo_endpoint, headers={"Authorization": f"Bearer {token['access_token']}"})
        user_info = userinfo_response.json()
        st.write("Welcome,", user_info["name"])
        st.write("Email:", user_info["email"])
else:
    st.write("You are already logged in!")
    userinfo_response = requests.get(userinfo_endpoint, headers={"Authorization": f"Bearer {st.session_state['token']['access_token']}"})
    user_info = userinfo_response.json()
    st.write("Welcome,", user_info["name"])
    st.write("Email:", user_info["email"])

