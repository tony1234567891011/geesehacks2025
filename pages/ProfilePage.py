import streamlit as st
from datetime import datetime, timedelta

# Function to calculate streak (days without break)
def calculate_streak(completed_dates):
    if not completed_dates:
        return 0
    
    # Sort dates to ensure they are in order
    completed_dates = sorted(completed_dates)

    # Check if the most recent date is today or within 24 hours of now
    if (datetime.now() - completed_dates[-1]).days > 1:
        return 0

    streak = 1
    for i in range(len(completed_dates) - 1, 0, -1):
        if completed_dates[i] - completed_dates[i-1] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak

# Example user data
user_name = "John Doe"
profile_picture = "https://picsum.photos/100"  # Replace with your image path or URL
completed_dates = [
    datetime(2025, 1, 20),
    datetime(2025, 1, 21),
    datetime(2025, 1, 22),
    datetime(2025, 1, 23),
    datetime(2025, 1, 24),  # Sample data; replace with actual completed task dates
]

# Calculate streak
streak = calculate_streak(completed_dates)

# Streamlit UI
st.title("Profile Page")

# Display profile picture
st.markdown(
    f"""
    <style>
    .profile-pic {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
    }}
    </style>
    <img src="{profile_picture}" class="profile-pic" alt="Profile Picture">
    """,
    unsafe_allow_html=True
)
# Display name and streak
st.subheader(f"Name: {user_name}")
st.subheader(f"Streak: {streak} days")



