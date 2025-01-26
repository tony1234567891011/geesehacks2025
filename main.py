import streamlit as st

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Space Themed To-Do List",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🚀 Build Your Space Tower!")
st.write("Add your own tasks below. Mark them complete with one click to add a block to the tower!")

##############################################
# 1) SESSION STATE: STORE AND MANAGE TO-DO TASKS
##############################################
if "tasks" not in st.session_state:
    # Each task is a dict: {"name": str, "completed": bool}
    st.session_state.tasks = []

# Add input for a new task
new_task = st.text_input("Add a new task:")
if st.button("Add Task"):
    task_name = new_task.strip()
    if task_name:
        st.session_state.tasks.append({"name": task_name, "completed": False})
        st.success(f"Task '{task_name}' added!")
    else:
        st.warning("Please enter a valid task name.")

st.write("---")

##########################################
# 2) DISPLAY TASKS AND MARK COMPLETION
##########################################
for i, task in enumerate(st.session_state.tasks):
    # Show the task's name and status
    if task["completed"]:
        st.write(f"**{task['name']}** (Completed)")
    else:
        st.write(f"**{task['name']}** (Incomplete)")

        # Single-click completion
        if st.button("Complete", key=f"complete_{i}"):
            task["completed"] = True
            st.success(f"'{task['name']}' completed!")

st.write("---")

#####################################
# 3) CALCULATE TOTAL COMPLETED TASKS
#####################################
total_blocks = sum(1 for t in st.session_state.tasks if t["completed"])
st.write(f"**Total Completed Tasks (Blocks):** {total_blocks}")

#####################################
# 4) RESET ALL TASKS (ONE CLICK)
#####################################
if st.button("Reset All Tasks"):
    for t in st.session_state.tasks:
        t["completed"] = False
    st.warning("All tasks have been reset to incomplete.")

st.write("---")

###############################################
# 5) SPACE-THEMED THREE.JS TOWER VISUALIZATION
###############################################
# No cross-out needed. We'll keep the same starfield & planet design.
# We do need to double braces {{ }} for JS object literals, since we are using an f-string.

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
        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xffffff, 1, 100);
        pointLight.position.set(10, 20, 20);
        scene.add(pointLight);

        // Starfield
        const starGeometry = new THREE.SphereGeometry(0.1, 24, 24);
        const starMaterial = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
        for (let i = 0; i < 300; i++) {{
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
        const towerHeight = {total_blocks}; // from Python

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

st.components.v1.html(three_js_code, height=600, scrolling=False)

