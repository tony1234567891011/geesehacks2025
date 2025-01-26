import streamlit as st

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Space Themed To-Do List",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🚀 Build Your Space Tower!")
st.write("Add your own tasks below. One click on “Complete” adds a block to the tower and removes the task.")

##############################################
# 1) SESSION STATE: STORE AND MANAGE TO-DO TASKS
##############################################
# We'll store tasks as a list of dicts, each with "name" and "completed"
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add input for a new task
new_task = st.text_input("Add a new task:")
if st.button("Add Task"):
    task_name = new_task.strip()
   
