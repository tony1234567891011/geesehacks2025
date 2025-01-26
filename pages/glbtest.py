import streamlit as st
import plotly.graph_objects as go
from streamlit.connections import FilesConnection
# Title of the Streamlit app
st.title("3D Model Viewer")

# File uploader for .glb files
uploaded_file = st.file_uploader("Upload a .glb file", type=["glb"])

if uploaded_file is not None:
    # Read the .glb file
    model_data = uploaded_file.read()

    # Create a 3D figure using Plotly
    fig = go.Figure()

    # Add the 3D model to the figure
    fig.add_trace(
        go.Mesh3d(
            x=[],  # Provide vertices x-coordinates if needed
            y=[],  # Provide vertices y-coordinates if needed
            z=[],  # Provide vertices z-coordinates if needed
            intensity=[],
            color='blue',
            name='3D Model'
        )
    )

    # Update layout for 3D view
    fig.update_layout(
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ),
        margin=dict(r=0, l=0, b=0, t=0)
    )

    # Render the 3D model
    st.plotly_chart(fig)
else:
    st.info("Please upload a .glb file to view the 3D model.")
