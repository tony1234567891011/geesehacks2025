import streamlit as st
from database import add_friend, get_db_connection  # Import necessary functions

# Mocked current user (replace with session-based authentication in production)
CURRENT_USER_ID = 1

# Streamlit UI
st.title("Friends Page")

# Add Friend Section
st.subheader("Add a Friend")
friend_email = st.text_input("Enter the Friend's Email:")

if st.button("Add Friend"):
    if not friend_email:
        st.error("Please enter a valid email.")
    else:
        try:
            # Fetch the friend's user_id by email
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = %s;", (friend_email,))
            result = cur.fetchone()
            
            if not result:
                st.error("No user found with this email.")
            else:
                friend_id = result[0]
                
                # Ensure the user is not adding themselves
                if friend_id == CURRENT_USER_ID:
                    st.error("You cannot add yourself as a friend.")
                else:
                    # Add friend
                    add_friend(CURRENT_USER_ID, friend_id)
                    st.success(f"Successfully added {friend_email} as a friend!")

            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Friends List Section
st.subheader("Your Friends List")

# Function to fetch friends by email
def get_friends(user_id):
    """Fetch the list of friends for a given user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id AS friend_id, u.email AS friend_email, u.username
        FROM friends f
        JOIN users u ON f.friend_id = u.id
        WHERE f.user_id = %s;
    """, (user_id,))
    friends = cur.fetchall()
    cur.close()
    conn.close()
    return [{"friend_id": row[0], "friend_email": row[1], "username": row[2]} for row in friends]

# Fetch friends for the current user
friends = get_friends(CURRENT_USER_ID)

if friends:
    st.write("Your friends:")
    for friend in friends:
        st.write(f"👤 {friend['username']} (Email: {friend['friend_email']})")
        st.write(f"[View {friend['username']}'s Tower](http://localhost:8501/viewfriend?friend_id={friend['friend_id']})")
else:
    st.write("You have no friends yet.")