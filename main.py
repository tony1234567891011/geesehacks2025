import streamlit as st
import datetime

################################
# STEP 1: SESSION STATE SETUP
################################
if "tasks" not in st.session_state:
    # We'll start with a couple sample tasks
    # Each task has a structure: {task_name: bool_completed}
    st.session_state.tasks = {
        "Read for 30 minutes": False,
        "Practice guitar": False,
        "Go for a run": False
    }

################################
# STEP 2: STREAMLIT LAYOUT
################################
st.set_page_config(page_title="Space Tower", layout="centered")
st.title("🚀 Build a Tower in Space!")
st.write("Add or select tasks below. Mark them as completed to build up your tower!")

################################
# STEP 3: ADD/SELECT TASK
################################
all_tasks = list(st.session_state.tasks.keys()) + ["(Add a new task...)"]
selected_task = st.selectbox("Select a Task to Work On", all_tasks)

if selected_task == "(Add a new task...)":
    new_task_name = st.text_input("Enter the new task name:")
    if st.button("Add new task"):
        if new_task_name.strip():
            st.session_state.tasks[new_task_name] = False
            st.success(f"Added task: {new_task_name}")
        else:
            st.warning("Please enter a valid task name.")
else:
    st.write(f"**Selected Task**: {selected_task}")
    # If it’s already completed, we’ll let user know
    if st.session_state.tasks[selected_task]:
        st.markdown(f"- ~~{selected_task}~~ (already completed)")
    else:
        st.markdown(f"- {selected_task} (not yet completed)")

    if not st.session_state.tasks[selected_task]:
        if st.button("Mark Completed"):
            st.session_state.tasks[selected_task] = True
            st.success(f"'{selected_task}' marked as completed!")

################################
# STEP 4: RESET ALL TASKS (Optional)
################################
if st.button("Reset All Tasks"):
    for task_name in st.session_state.tasks:
        st.session_state.tasks[task_name] = False
    st.warning("All tasks have been reset to incomplete.")

################################
# STEP 5: COUNT COMPLETED TASKS
################################
# Let's say each completed task = 1 block in the tower
total_blocks = sum(1 for completed in st.session_state.tasks.values() if completed)

################################
# STEP 6: 3D TOWER IN SPACE
################################
# We need to carefully use an f-string and double braces for JS objects.
three_js_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3D Tower</title>
    <style>
        body {{
            margin: 0; 
            background: #000;
            overflow: hidden;
        }}
        canvas {{
            display: block; 
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%;
        }}
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
        scene.add(ambientLight);

        // Point light
        const pointLight = new THREE.PointLight(0xffffff, 1, 100);
        pointLight.position.set(10, 20, 20);
        scene.add(pointLight);

        // Starfield
        const starGeometry = new THREE.SphereGeometry(0.1, 24, 24);
        const starMaterial = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
        for (let i = 0; i < 200; i++) {{
            const star = new THREE.Mesh(starGeometry, starMaterial);
            star.position.set(
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200
            );
            scene.add(star);
        }}

        // Planet
        const planetGeometry = new THREE.SphereGeometry(5, 32, 32);
        const planetMaterial = new THREE.MeshPhongMaterial({{ color: 0x5555ff, shininess: 10 }});
        const planet = new THREE.Mesh(planetGeometry, planetMaterial);
        planet.position.set(-15, 10, -30);
        scene.add(planet);

        // Tower blocks
        const blockWidth = 1;
        const blockHeight = 0.5;
        const towerHeight = {total_blocks}; // injected from Python

        for (let i = 0; i < towerHeight; i++) {{
            const geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            const hue = (i / Math.max(1, towerHeight)) * 360;
            const color = new THREE.Color(`hsl(${{hue}}, 100%, 50%)`);
            const material = new THREE.MeshPhongMaterial({{ color: color, shininess: 50 }});
            const block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
        }}

        // Camera positioning
        camera.position.set(2, towerHeight * blockHeight + 5, 8);
        camera.lookAt(0, towerHeight * blockHeight / 2, 0);

        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.001; // gentle rotation
            planet.rotation.y += 0.0005; 
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

# Finally, render the HTML/JS in Streamlit
st.components.v1.html(three_js_code, height=600, scrolling=False)
