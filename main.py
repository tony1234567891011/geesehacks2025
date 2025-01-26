import streamlit as st
import datetime

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

# Streamlit UI
st.title("🏗️ Habit Tracker: Build Your Tower!")
st.write("Each completed task adds a block to your tower!")

# Sidebar Navigation
st.sidebar.title("📌 Your Habits")
page = st.sidebar.radio("Select Habit", list(st.session_state.habits.keys()) + ["Add New Habit"])

# Add New Habit
if page == "Add New Habit":
    new_habit = st.sidebar.text_input("Enter new habit name:")
    if st.sidebar.button("Add Habit") and new_habit:
        if new_habit not in st.session_state.habits:
            st.session_state.habits[new_habit] = 0
            st.session_state.streaks[new_habit] = 0
            st.session_state.last_completed[new_habit] = None
            st.success(f"{new_habit} added to habits!")
        else:
            st.warning("This habit already exists!")

# Main Habit Page
if page in st.session_state.habits:
    st.header(f"📌 {page} Habit Progress")
    st.write(f"Blocks Earned: {st.session_state.habits[page]}")
    st.write(f"🔥 Streak: {st.session_state.streaks[page]} days")
    
    # Complete Task Button
    if st.button("✅ Mark as Completed Today"):
        today = datetime.date.today()
        last_date = st.session_state.last_completed[page]
        
        if last_date is not None and (today - last_date).days == 1:
            st.session_state.streaks[page] += 1  # Maintain streak
        else:
            st.session_state.streaks[page] = 1  # Reset streak if broken
        
        st.session_state.habits[page] += 1  # Increase block count
        st.session_state.last_completed[page] = today
        st.success(f"{page} completed today! Tower growing!")
    
    # Reset Habit Progress
    if st.button("🔄 Reset Habit"):
        st.session_state.habits[page] = 0
        st.session_state.streaks[page] = 0
        st.session_state.last_completed[page] = None
        st.warning(f"{page} progress reset.")

# Three.js Integration for Tower Visualization
three_js_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3D Habit Tower</title>
    <style>
        body {{ margin: 0; background: linear-gradient(to bottom, #000000, #001f3f); }}
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

        let light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(2, 5, 5);
        scene.add(light);

        let blockWidth = 1;
        let blockHeight = 0.5;
        let towerHeight = {sum(st.session_state.habits.values())};

        for (let i = 0; i < towerHeight; i++) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let color = new THREE.Color(`hsl(${{(i / towerHeight) * 360}}, 100%, 50%)`);
            let material = new THREE.MeshPhongMaterial({{ color: color, shininess: 50 }});
            let block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
        }}

        camera.position.set(2, towerHeight * blockHeight, 5);
        camera.lookAt(0, towerHeight * blockHeight / 2, 0);

        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.005;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

st.components.v1.html(three_js_code, height=600, scrolling=False)
