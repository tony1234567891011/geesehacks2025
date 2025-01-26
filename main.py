import streamlit as st

# Initialize session state for tower height
if "tower_height" not in st.session_state:
    st.session_state.tower_height = 5  # Default initial height

# Streamlit UI
st.title("Progress Tracker")
st.write("Make your tower as big as possible!")

# Display the current tower height
st.write(f"Current Tower Height: {st.session_state.tower_height}")

# Add Block Button
if st.button("Add Block"):
    if st.session_state.tower_height < 200:  # Limit the number of blocks to 200
        st.session_state.tower_height += 1
    else:
        st.warning("Maximum tower height reached!")

# Reset Button
if st.button("Reset Tower"):
    st.session_state.tower_height = 1  # Reset to one block

# Add CSS for a black to night blue gradient background
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #000000, #001f3f); /* Black to Night Blue */
        height: auto; /* Allow height to grow dynamically */
        margin: 0;
        overflow-x: hidden;
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

        // Create blocks
        for (let i = 0; i < towerHeight; i++) {{
            let geometry = new THREE.BoxGeometry(blockWidth, blockHeight, blockWidth);
            let hue = (i / towerHeight) * 360; // Define hue within the loop
            let color = new THREE.Color(`hsl(${{hue}}, 100%, 50%)`); // Escape the ${{}} for JavaScript
            let material = new THREE.MeshBasicMaterial({{ color: color }});
            let block = new THREE.Mesh(geometry, material);
            block.position.y = i * blockHeight;
            scene.add(block);
            blocks.push(block);
        }}

        camera.position.set(3, towerHeight * blockHeight, 5); // Adjust camera position for an angled, upper view
        camera.lookAt(0, towerHeight * blockHeight / 2, 0); // Make the camera look at the center of the tower

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
st.components.v1.html(three_js_code, height=600, scrolling=False)

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