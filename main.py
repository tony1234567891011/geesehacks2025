import streamlit as st

# Initialize session state for tower height and block colors
if "tower_height" not in st.session_state:
    st.session_state.tower_height = 5  # Default initial height
if "block_colors" not in st.session_state:
    st.session_state.block_colors = ["hsl(0, 90%, 70%)"] * st.session_state.tower_height  # Default colors

# Initialize session state for camera position
if "camera_position" not in st.session_state:
    st.session_state.camera_position = {"x": 3, "y": st.session_state.tower_height * 0.5, "z": 5}

# Function to update camera position in session state
def update_camera_position(x, y, z):
    st.session_state.camera_position = {"x": x, "y": y, "z": z}

# Streamlit UI
st.title("Progress Tracker")
st.write("Make your tower as big as possible!")

# Color picker for new block
new_block_color = st.color_picker("Pick a color for the new block", "#ff0000")

# Add Block Button
if st.button("Add Block"):
    if st.session_state.tower_height < 200:  # Limit the number of blocks to 200
        st.session_state.tower_height += 1
        st.session_state.block_colors.append(new_block_color)
    else:
        st.warning("Maximum tower height reached!")

# Reset Button
if st.button("Reset Tower"):
    st.session_state.tower_height = 1  # Reset to one block
    st.session_state.block_colors = [new_block_color]

# Display the current tower height
st.write(f"Current Tower Height: {st.session_state.tower_height}")
st.write(f"Current Block Colors: {st.session_state.block_colors}")

# Button to print block colors array to console
if st.button("Print Block Colors"):
    st.markdown(
        f"""
        <script>
        function printBlockColors() {{
            console.log({st.session_state.block_colors});
        }}
        printBlockColors();
        </script>
        """,
        unsafe_allow_html=True,
    )

# Add CSS for a black to night blue gradient background
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #000000, #001f3f); /* Black to Night Blue */
        height: 100vh; /* Set height to 100% of the viewport height */
        margin: 0;
        overflow: hidden;
    }

    .scrollable-container {
        overflow-y: visible; /* Let the container grow naturally */
        border: 1px solid rgba(255, 255, 255, 0.2); /* Optional border */
        padding: 10px;
        background-color: rgba(0, 0, 0, 0); /* Fully transparent background */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Three.js HTML and JavaScript code
three_js_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Block Tower</title>
    <style>
        body {{ margin: 0; background: linear-gradient(to bottom, #000000, #001f3f); }} /* Set background gradient */
        canvas {{ display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, #000000, #001f3f); }} /* Fix position and size */
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene = new THREE.Scene();
        let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        let renderer = new THREE.WebGLRenderer({{ alpha: true }}); // Enable transparency
        renderer.setClearColor(0x000000, 0); // Set the clear color to transparent
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        let blockWidth = 1;
        let blockHeight = 0.5;
        let blocks = [];
        let towerHeight = {st.session_state.tower_height}; // Dynamically injected Python variable
        let blockColors = {st.session_state.block_colors}; // Dynamically injected Python variable

        // Create blocks
        for (let i = 0; i < towerHeight; i++) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let color = new THREE.Color(blockColors[i]); // Use the color from the session state
            let material = new THREE.MeshLambertMaterial({{ color: color }}); // Use Lambert material for better lighting
            let block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
            blocks.push(block);
        }}

        // Add ambient light
        let ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
        scene.add(ambientLight);

        // Add directional light
        let directionalLight = new THREE.DirectionalLight(0xffffff, 1); // White light
        directionalLight.position.set(5, 10, 7.5).normalize();
        scene.add(directionalLight);

        // Restore camera position from session state
        camera.position.set({st.session_state.camera_position["x"]}, {st.session_state.camera_position["y"]}, {st.session_state.camera_position["z"]});
        camera.lookAt(0, towerHeight * blockHeight / 2, 0); // Make the camera look at the center of the tower

        // Add event listener for mouse wheel to scroll in the z-axis
        window.addEventListener('wheel', (event) => {{
            camera.position.y += event.deltaY * 0.01; // Adjust the scroll speed as needed
            // Save camera position to session state
            fetch(`/?x=${{camera.position.x}}&y=${{camera.position.y}}&z=${{camera.position.z}}`);
        }});

        // Add event listener for keydown to move the camera with arrow keys
        window.addEventListener('keydown', (event) => {{
            if (event.key === 'ArrowUp') {{
                camera.position.y += 0.1; // Move camera up
            }} else if (event.key === 'ArrowDown') {{
                camera.position.y -= 0.1; // Move camera down
            }}
            // Save camera position to session state
            fetch(`/?x=${{camera.position.x}}&y=${{camera.position.y}}&z=${{camera.position.z}}`);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

# Embed the Three.js code in Streamlit
st.components.v1.html(three_js_code, height=800, scrolling=False)  # Set height to 800 to span the whole page

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Journal", "Gym", "Meditate", "French Duolingo"])

# Placeholder for other pages
if page == "Journal":
    st.write("Welcome to the Journal page!")
elif page == "Gym":
    st.write("Welcome to the Gym page!")
elif page == "Meditate":
    st.write("Welcome to the Meditate page!")
elif page == "French Duolingo":
    st.write("Welcome to the French Duolingo page!")