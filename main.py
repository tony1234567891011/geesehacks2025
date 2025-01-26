import streamlit as st
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

# Streamlit UI
st.title("Progress Tracker")
st.write("Make your tower as big as possible!")

# Display the current tower colors
st.write("Tower colors:", tower_colors)

# Color picker for a new block
new_block_color = st.selectbox("Choose a color for the new block:", ["P", "B", "Y"])

# Add Block Button
if st.button("Add Block"):
    if len(tower_colors) < 200:  # Limit the number of blocks to 200
        try:
            add_block(USER_ID, new_block_color)
            st.success(f"Added block {new_block_color} to the tower!")
            tower_string += new_block_color  # Update the local string for immediate feedback
            tower_colors = generate_tower_colors(tower_string)
        except Exception as e:
            st.error(f"Failed to add block: {e}")
    else:
        st.warning("Maximum tower height reached!")

# Reset Button
if st.button("Reset Tower"):
    try:
        set_tower(USER_ID, "")  # Reset the tower in the database
        tower_string = ""  # Clear the local tower string
        tower_colors = []  # Reset tower colors
        st.success("Tower has been reset!")
    except Exception as e:
        st.error(f"Failed to reset tower: {e}")

# Display the current tower height
st.write(f"Current Tower Height: {len(tower_colors)}")
st.write(f"Current Block Colors: {tower_colors}")

if st.button("Remove 3 Blocks"):
    try:
        updated_tower = remove_blocks(USER_ID, 3)
        st.success("Removed 3 blocks from the tower!")
        tower_string = updated_tower  # Update local variable for immediate feedback
        tower_colors = generate_tower_colors(tower_string)  # Re-generate colors
    except ValueError as e:
        st.error(f"Error: {e}")

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Three.js HTML and JavaScript code for rendering the tower
three_js_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Block Tower</title>
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
        let renderer = new THREE.WebGLRenderer({{ alpha: true }});
        renderer.setClearColor(0x000000, 0);
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        let blockWidth = 1;
        let blockHeight = 0.5;
        let blocks = [];
        let towerHeight = {len(tower_colors)}; // Dynamically injected Python variable
        let blockColors = {tower_colors}; // Dynamically injected Python variable

        for (let i = 0; i < towerHeight; i++) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let color = new THREE.Color(blockColors[i]);
            let material = new THREE.MeshLambertMaterial({{ color: color }});
            let block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
            blocks.push(block);
        }}

        let ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);

        let directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 10, 7.5).normalize();
        scene.add(directionalLight);

        camera.position.set({st.session_state.camera_position["x"]}, {st.session_state.camera_position["y"]}, {st.session_state.camera_position["z"]});
        camera.lookAt(0, towerHeight * blockHeight / 2, 0);

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
st.components.v1.html(three_js_code, height=800, scrolling=False)
