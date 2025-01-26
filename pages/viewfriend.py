import streamlit as st
from database import get_tower, get_user_by_id  # Import the get_tower function from the database

# Function to map a tower string to colors
def generate_tower_colors(color_string):
    color_map = {
        "P": "Red",
        "B": "Blue",
        "Y": "Yellow"
    }
    return [color_map[char] for char in color_string]

# Get the friend_id from the URL query parameters
query_params = st.query_params
friend_id = query_params.get("friend_id", [None])[0]

if friend_id:
    try:
        # Fetch the friend's tower string from the database
        tower_string = get_tower(friend_id)
        tower_colors = generate_tower_colors(tower_string)
        friend = get_user_by_id(friend_id)
        friend_name = friend['username']
        
        if "camera_position" not in st.session_state:
            st.session_state.camera_position = {"x": 3, "y": len(tower_colors) * 0.5, "z": 5}

        st.title(f"{friend_name}'s Tower")

        # Generate the HTML and JavaScript code
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
        st.components.v1.html(three_js_code, height=600)
    except ValueError:
        st.error("Friend's tower not found. Please contact support.")
else:
    st.error("No friend ID provided in the URL query parameters.")