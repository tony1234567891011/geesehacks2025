# streamlit_app.py
import streamlit as st
import datetime
import random

###############################
# SESSION STATE INITIALIZATION
###############################

# Keep track of daily tasks (reset them if a new day starts)
if "daily_tasks" not in st.session_state:
    # Simple static tasks for demonstration;
    # in practice, you could randomize these or load from a database
    st.session_state.daily_tasks = [
        {"name": "Daily Task 1", "completed": False},
        {"name": "Daily Task 2", "completed": False},
        {"name": "Daily Task 3", "completed": False}
    ]

if "daily_task_date" not in st.session_state:
    st.session_state.daily_task_date = datetime.date.today()

# If it's a new day, reset the tasks
if st.session_state.daily_task_date != datetime.date.today():
    st.session_state.daily_tasks = [
        {"name": "Daily Task 1", "completed": False},
        {"name": "Daily Task 2", "completed": False},
        {"name": "Daily Task 3", "completed": False}
    ]
    st.session_state.daily_task_date = datetime.date.today()

# Initialize session state for habits
if "habits" not in st.session_state:
    st.session_state.habits = {
        "Journal": 0,
        "Gym": 0,
        "Meditate": 0,
        "French Duolingo": 0
    }
    st.session_state.streaks = {habit: 0 for habit in st.session_state.habits}
    st.session_state.last_completed = {habit: None for habit in st.session_state.habits}


##################
# STREAMLIT LAYOUT
##################

st.set_page_config(
    page_title="Habit Tracker",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🏗️ Habit Tracker: Build Your Tower in Space!")
st.write("Each completed task adds a block to your tower. Complete daily tasks and habits for maximum height!")

# Sidebar Navigation
st.sidebar.title("📌 Your Habits")
page = st.sidebar.radio("Select Page", ["Home"] + list(st.session_state.habits.keys()) + ["Add New Habit"])


#########################
# ADD NEW HABIT FUNCTION
#########################

def add_new_habit(new_habit: str):
    """Add a new habit to the session state."""
    if new_habit not in st.session_state.habits:
        st.session_state.habits[new_habit] = 0
        st.session_state.streaks[new_habit] = 0
        st.session_state.last_completed[new_habit] = None
        st.success(f"'{new_habit}' added to your habits!")
    else:
        st.warning("This habit already exists!")


#############################
# HOME PAGE - DAILY TASKS
#############################

if page == "Home":
    st.subheader("Today's To-Do List")
    st.write("Complete these 3 tasks to earn additional blocks!")

    for task in st.session_state.daily_tasks:
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            # Strikethrough if completed
            if task["completed"]:
                st.markdown(f"- ~~{task['name']}~~")
            else:
                st.markdown(f"- {task['name']}")
        with col2:
            if not task["completed"]:
                if st.button(f"Mark '{task['name']}' Completed"):
                    task["completed"] = True
                    # If there's no special 'Daily Tasks' habit yet, create it
                    if "Daily Tasks" not in st.session_state.habits:
                        st.session_state.habits["Daily Tasks"] = 0
                        st.session_state.streaks["Daily Tasks"] = 0
                        st.session_state.last_completed["Daily Tasks"] = None

                    # Add one block for completing this task
                    st.session_state.habits["Daily Tasks"] += 1
                    st.success(f"{task['name']} completed!")
            else:
                st.write("✅ Done")

    # Display daily tasks reset info
    st.write(f"These tasks will reset on {st.session_state.daily_task_date + datetime.timedelta(days=1)}.")


######################
# ADD NEW HABIT PAGE
######################

if page == "Add New Habit":
    st.sidebar.write("Add a new habit:")
    new_habit = st.sidebar.text_input("Enter new habit name")
    if st.sidebar.button("Add Habit") and new_habit:
        add_new_habit(new_habit)


#############################
# HABIT DETAILS PAGES
#############################

if page in st.session_state.habits:
    st.header(f"📌 {page} Habit Progress")
    st.write(f"Blocks Earned: {st.session_state.habits[page]}")
    st.write(f"🔥 Streak: {st.session_state.streaks[page]} days")

    # Complete Task Button
    if st.button("✅ Mark as Completed Today"):
        today = datetime.date.today()
        last_date = st.session_state.last_completed[page]

        if last_date is not None and (today - last_date).days == 1:
            # Continue the streak
            st.session_state.streaks[page] += 1
        else:
            # Reset streak
            st.session_state.streaks[page] = 1

        st.session_state.habits[page] += 1  # Increase block count
        st.session_state.last_completed[page] = today
        st.success(f"{page} completed today! Tower grows!")

    # Reset Habit Progress
    if st.button("🔄 Reset Habit"):
        st.session_state.habits[page] = 0
        st.session_state.streaks[page] = 0
        st.session_state.last_completed[page] = None
        st.warning(f"{page} progress reset.")


#############################################
# 3D TOWER WITH STARS & PLANET BACKDROP
#############################################

# Calculate total blocks from all habits, including 'Daily Tasks' if present
total_blocks = sum(st.session_state.habits.values())

three_js_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3D Habit Tower in Space</title>
    <style>
        body {{ margin: 0; background: #000; }}
        canvas {{ display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene = new THREE.Scene();
        let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        let renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Add a soft ambient light
        let ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
        scene.add(ambientLight);

        // Add a point light to mimic a star/sun
        let pointLight = new THREE.PointLight(0xffffff, 1, 100);
        pointLight.position.set(10, 20, 20);
        scene.add(pointLight);

        // Create a starfield
        let starGeometry = new THREE.SphereGeometry(0.1, 24, 24);
        let starMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });

        for (let i = 0; i < 300; i++) {{
            let star = new THREE.Mesh(starGeometry, starMaterial);
            // Random position in a wide range
            let x = (Math.random() - 0.5) * 200;
            let y = (Math.random() - 0.5) * 200;
            let z = (Math.random() - 0.5) * 200;
            star.position.set(x, y, z);
            scene.add(star);
        }}

        // Create a planet in the background
        let planetGeometry = new THREE.SphereGeometry(5, 32, 32);
        let planetMaterial = new THREE.MeshPhongMaterial({ color: 0x5555ff, shininess: 10 });
        let planet = new THREE.Mesh(planetGeometry, planetMaterial);
        planet.position.set(-15, 10, -30);
        scene.add(planet);

        let blockWidth = 1;
        let blockHeight = 0.5;
        let towerHeight = {total_blocks};

        for (let i = 0; i < towerHeight; i++) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let color = new THREE.Color(`hsl(${{(i / (towerHeight + 1)) * 360}}, 100%, 50%)`);
            let material = new THREE.MeshPhongMaterial({{ color: color, shininess: 50 }});
            let block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
        }}

        camera.position.set(2, towerHeight * blockHeight + 5, 8);
        camera.lookAt(0, towerHeight * blockHeight / 2, 0);

        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.002; // slowly rotate the scene for a cool effect
            planet.rotation.y += 0.001; // rotate the planet slightly
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

# Embed the Three.js code in Streamlit
st.components.v1.html(three_js_code, height=600, scrolling=False)
