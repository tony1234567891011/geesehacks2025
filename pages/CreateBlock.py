import streamlit as st
import json
from datetime import datetime
from database import add_block  # Import add_block function

# Initialize session state variables
if 'block_colors' not in st.session_state:
    st.session_state.block_colors = []
if 'tower_height' not in st.session_state:
    st.session_state.tower_height = 0

# Mock database
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

# Load tasks
tasks = load_tasks()

# Function to add a new task
def add_task(task, category):
    tasks.append({'task': task, 'category': category, 'completed': False, 'date': datetime.now().isoformat()})
    save_tasks(tasks)

# Function to complete a task
def complete_task(task_index):
    tasks[task_index]['completed'] = True
    save_tasks(tasks)
    # Add a block with the corresponding color
    category = tasks[task_index]['category']
    color = ''
    if category == 'Athletic':
        color = 'P'
        st.session_state.block_colors.append('red')
    elif category == 'Social':
        color = 'Y'
        st.session_state.block_colors.append('yellow')
    elif category == 'Mental':
        color = 'B'
        st.session_state.block_colors.append('blue')
    st.session_state.tower_height += 1
    # Add block to the tower in the database
    add_block(1, color)  # Assuming USER_ID is 1 for simplicity

# Map category to color
category_colors = {
    'Athletic': 'red',
    'Social': 'yellow',
    'Mental': 'blue'
}

# Streamlit UI
st.title("Tasks Page")

# Task creation form
st.subheader("Create a New Task")
task = st.text_input("Task Description")
category = st.selectbox("Category", ["Athletic", "Social", "Mental"])

if st.button("Add Task"):
    if task:
        add_task(task, category)
        st.success("Task added successfully!")
    else:
        st.error("Task description cannot be empty.")

# List of pending tasks
st.subheader("Pending Tasks")
for index, task in enumerate(tasks):
    if not task['completed']:
        if st.checkbox(f"{task['task']} ({task['category']})", key=index):
            complete_task(index)
            st.query_params = {"rerun": index}
        
        # Display task with color
        st.markdown(
            f"""
            <div style='border-left: 5px solid {category_colors[task['category']]}; padding-left: 10px; margin-bottom: 5px;'>
                <strong>{task['task']}</strong> ({task['category']})
            </div>
            """,
            unsafe_allow_html=True
        )

