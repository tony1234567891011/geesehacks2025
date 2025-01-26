import streamlit as st
from datetime import datetime, timedelta
import time
from database import get_tower, add_block, remove_blocks, set_tower  # Import database functions

# Get the user ID (for simplicity, assume user ID is hardcoded or retrieved after login)
USER_ID = 1  # Replace with actual user authentication logic

# Fetch the current tower string from the database
try:
    tower_string = get_tower(USER_ID)
except ValueError:
    st.error("User tower not found. Please contact support.")
    tower_string = ""

# Function to map a tower string to colors
def generate_tower_colors(color_string):
    color_map = {
        "P": "Red",
        "B": "Blue",
        "Y": "Yellow"
    }
    return [color_map[char] for char in color_string]

# Generate tower colors based on the database string
tower_colors = generate_tower_colors(tower_string)

# Initialize camera position
if "camera_position" not in st.session_state:
    st.session_state.camera_position = {"x": 3, "y": len(tower_colors) * 0.5, "z": 5}

# Initialize flag for adding a new block
if "new_block_added" not in st.session_state:
    st.session_state.new_block_added = False

# Initialize task completion times
if "task_completion_times" not in st.session_state:
    st.session_state.task_completion_times = {"task1": None, "task2": None, "task3": None}

# Calculate time left until next day
now = datetime.now()
next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
time_left = next_day - now


# Add CSS for a black to night blue gradient background and overlay card
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #000000, #001f3f); /* Black to Night Blue */
        height: 100vh; /* Set height to 100% of the viewport height */
        width: 100vw;
        margin: 0;
        overflow: hidden;
    }
    .overlay-card {
        position: absolute;
        top: 20px;
        right: -15vw;
        width: 25vw;
        height: 80vh;
        background-color: rgba(38,39,48,255);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        z-index: 1000;
    }
    canvas {
        position: fixed;
        top: 0;
        left: -40vw; /* Move the canvas 10vw to the left */
        width: 120vw; /* Increase the width to cover the viewport */
        height: 100vh;
    }
    button:hover {
        border: 2px solid green;
        color: green;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create the overlay card with Streamlit buttons
# st.markdown('<div class="overlay-card">', unsafe_allow_html=True)
st.markdown(f"<h3>Blocks Expire in : {str(time_left).split('.')[0]}</h3>", unsafe_allow_html=True)

# Task buttons
task1_container = st.empty()
task2_container = st.empty()
task3_container = st.empty()

if st.session_state.task_completion_times["task1"] is None or datetime.now() - st.session_state.task_completion_times["task1"] > timedelta(days=1):
    if task1_container.button("Go for a walk"):
        add_block(USER_ID, "P")
        tower_string += "P"  # Update the local tower string
        set_tower(USER_ID, tower_string)  # Update the tower in the database
        tower_colors = generate_tower_colors(tower_string)  # Update the tower colors
        st.session_state.task_completion_times["task1"] = datetime.now()
        st.success("Body Block Earned!")
        st.session_state.new_block_added = True
        task1_container.empty()  # Hide the button after it's clicked
else:
    task1_container.empty()  # Hide the button if the task is already completed

if st.session_state.task_completion_times["task2"] is None or datetime.now() - st.session_state.task_completion_times["task2"] > timedelta(days=1):
    if task2_container.button("Meditate for 10 minutes"):
        add_block(USER_ID, "B")
        tower_string += "B"  # Update the local tower string
        set_tower(USER_ID, tower_string)  # Update the tower in the database
        tower_colors = generate_tower_colors(tower_string)  # Update the tower colors
        st.session_state.task_completion_times["task2"] = datetime.now()
        st.success("Mind Block Earned!")
        st.session_state.new_block_added = True
        task2_container.empty()  # Hide the button after it's clicked
else:
    task2_container.empty()  # Hide the button if the task is already completed

if st.session_state.task_completion_times["task3"] is None or datetime.now() - st.session_state.task_completion_times["task3"] > timedelta(days=1):
    if task3_container.button("Call mom"):
        add_block(USER_ID, "Y")
        tower_string += "Y"  # Update the local tower string
        set_tower(USER_ID, tower_string)  # Update the tower in the database
        tower_colors = generate_tower_colors(tower_string)  # Update the tower colors
        st.session_state.task_completion_times["task3"] = datetime.now()
        st.success("Soul Block Earned!")
        st.session_state.new_block_added = True
        task3_container.empty()  # Hide the button after it's clicked
else:
    task3_container.empty()  # Hide the button if the task is already completed

# Three.js HTML and JavaScript code for rendering the tower
three_js_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Block Tower</title>
    <style>
        body {{ margin: 0; background: linear-gradient(to bottom, #000000, #001f3f); }}
        canvas {{ display: block; position: fixed; top: 0; left: -10vw; width: 120vw; height: 100vh; }}
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>

        let scene, camera, renderer, blocks = [];

        let blockWidth = 1;
        let blockHeight = 0.5;
        let towerHeight = {len(tower_colors)}; // Dynamically injected Python variable
        let blockColors = {tower_colors}; // Dynamically injected Python variable

        function init() {{
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({{ alpha: true }});
            renderer.setClearColor(0x000000, 0);
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            let ambientLight = new THREE.AmbientLight(0x404040);
            scene.add(ambientLight);

            let directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(5, 10, 7.5).normalize();
            scene.add(directionalLight);

            camera.position.set({st.session_state.camera_position["x"]}, {st.session_state.camera_position["y"]}, {st.session_state.camera_position["z"]});
            camera.lookAt(0, towerHeight * blockHeight / 2, 0);

            for (let i = 0; i < towerHeight; i++) {{
                let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
                let color = new THREE.Color(blockColors[i]);
                let material = new THREE.MeshLambertMaterial({{ color: color }});
                let block = new THREE.Mesh(geometry, material);
                block.position.y = i * blockHeight;
                scene.add(block);
                blocks.push(block);
            }}

            // Add raycaster and mouse for hover effect
            let raycaster = new THREE.Raycaster();
            let mouse = new THREE.Vector2();
            let INTERSECTED;

            function onMouseMove(event) {{
                mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            }}

            window.addEventListener('mousemove', onMouseMove, false);

            function animate() {{
                requestAnimationFrame(animate);

                // Update the raycaster with the camera and mouse position
                raycaster.setFromCamera(mouse, camera);

                // Calculate objects intersecting the raycaster
                let intersects = raycaster.intersectObjects(blocks);

                if (intersects.length > 0) {{
                    if (INTERSECTED != intersects[0].object) {{
                        if (INTERSECTED) INTERSECTED.material.color.setHex(INTERSECTED.currentHex);
                        INTERSECTED = intersects[0].object;
                        INTERSECTED.currentHex = INTERSECTED.material.color.getHex();
                        INTERSECTED.material.color.setHex(0xff0000); // Change hover color here
                    }}
                }} else {{
                    if (INTERSECTED) INTERSECTED.material.color.setHex(INTERSECTED.currentHex);
                    INTERSECTED = null;
                }}

                renderer.render(scene, camera);
            }}

            animate();
        }}

        function addBlockAnimation(color) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let material = new THREE.MeshLambertMaterial({{ color: new THREE.Color(color) }});
            let block = new THREE.Mesh(geometry, material);
            block.position.y = towerHeight * blockHeight;
            block.scale.set(1, 0, 1);
            scene.add(block);
            blocks.push(block);

            let targetScaleY = 1;
            let currentScaleY = 0;
            let animationSpeed = 0.05;

            function growBlock() {{
                if (currentScaleY < targetScaleY) {{
                    currentScaleY += animationSpeed;
                    block.scale.y = currentScaleY;
                    block.position.y = (towerHeight + currentScaleY / 2) * blockHeight;
                    requestAnimationFrame(growBlock);
                }} else {{
                    block.scale.y = targetScaleY;
                    block.position.y = towerHeight * blockHeight;
                }}
            }}
            growBlock();
        }}

        if (!window.initialized) {{
            init();
            window.initialized = true;
        }}

        if ({st.session_state.new_block_added}) {{
            addBlockAnimation(blockColors[blockColors.length - 1]);
        }}
    </script>
</body>
</html>
"""

# Embed the Three.js code in Streamlit
st.components.v1.html(three_js_code, height=800, scrolling=False)

# Reset the flag after rendering
st.session_state.new_block_added = False
