import streamlit as st
import pandas as pd
import json

# Mock database functions
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def load_friend_requests():
    try:
        with open('friend_requests.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_friend_requests(requests):
    with open('friend_requests.json', 'w') as f:
        json.dump(requests, f)

# Load data
users = load_users()
friend_requests = load_friend_requests()

# Sample user data
current_user = 'john_doe'  # Replace with the actual current user
users = [
    {'username': 'john_doe', 'name': 'John Doe'},
    {'username': 'jane_smith', 'name': 'Jane Smith'},
    {'username': 'alice_brown', 'name': 'Alice Brown'},
    {'username': 'bob_jones', 'name': 'Bob Jones'},
]

# Function to send a friend request
def send_friend_request(from_user, to_user):
    friend_requests.append({'from': from_user, 'to': to_user, 'status': 'pending'})
    save_friend_requests(friend_requests)

# Function to accept a friend request
def accept_friend_request(request):
    request['status'] = 'accepted'
    save_friend_requests(friend_requests)

# Function to deny a friend request
def deny_friend_request(request):
    request['status'] = 'denied'
    save_friend_requests(friend_requests)

# Streamlit UI
st.title("Friends Page")

# Lookup people and send friend requests
st.subheader("Look Up People")
search_username = st.text_input("Search by username")
if st.button("Search"):
    searched_users = [user for user in users if search_username.lower() in user['username'].lower()]
    if searched_users:
        for user in searched_users:
            st.write(f"Username: {user['username']}, Name: {user['name']}")
            if st.button(f"Send Friend Request to {user['username']}"):
                send_friend_request(current_user, user['username'])
                st.success(f"Friend request sent to {user['username']}!")
    else:
        st.error("No users found with that username.")

# View and manage friend requests
st.subheader("Pending Friend Requests")
pending_requests = [request for request in friend_requests if request['to'] == current_user and request['status'] == 'pending']
if pending_requests:
    for request in pending_requests:
        st.write(f"Friend request from {request['from']}")
        if st.button(f"Accept {request['from']}"):
            accept_friend_request(request)
            st.success(f"Accepted friend request from {request['from']}")
        if st.button(f"Deny {request['from']}"):
            deny_friend_request(request)
            st.success(f"Denied friend request from {request['from']}")
else:
    st.write("No pending friend requests.")

