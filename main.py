import streamlit as st
import plotly.graph_objects as go


def create_block_tower(height):
    """Creates a 2D block tower with the specified height, ensuring fixed block size."""
    fig = go.Figure()

    block_width = 1
    block_height = 50 # Fixed height of each block in pixels

    # Generate a gradient from blue (cool) to red (hot)
    gradient_colors = [
        f"rgba({int(255 * (i / height))}, 0, {255 - int(255 * (i / height))}, 1)"
        for i in range(height)
    ]

    # Loop to create each block and add a number annotation
    for i in range(height):
        x0, x1 = -block_width / 2, block_width / 2
        y0, y1 = i * block_height, (i + 1) * block_height
        colour=''
        if i%2==0:
            colour="orange"
        else:
            colour="green"
        fig.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            line=dict(color="black"),

            fillcolor=gradient_colors[i],  # Use the gradient color
        )

        # Add number annotation at the center of each block
        fig.add_annotation(
            x=0,  # Center of the block
            y=y0 + block_height / 2,  # Middle of the block
            text=str(i + 1),  # Block number
            showarrow=False,
            font=dict(size=12, color="black"),  # Customize font size and color
        )

    # Dynamically set the y-axis range to show all blocks
    yaxis_range = [0, height * block_height]  # Ensure all blocks fit the viewport

    # Fix the chart height and make it scrollable
    fig.update_layout(
        xaxis=dict(
            visible=False,
            range=[-1, 1],  # Centered horizontally
            fixedrange=True,  # Disable zoom on x-axis
        ),
        yaxis=dict(
            visible=False,
            range=yaxis_range,  # Dynamically adjust based on block count
            fixedrange=True,  # Disable zoom on y-axis
        ),
        width=400,  # Fixed width
        height= block_height * height,  # Fixed height of the viewport
        margin=dict(l=50, r=50, t=50, b=50),  # Add margins for proper positioning
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Remove background inside the plot
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Remove background outside the plot
    )

    return fig


# Initialize session state for tower height
if "tower_height" not in st.session_state:
    st.session_state.tower_height = 5  # Default initial height

# Streamlit UI
st.title("Progress Tracker")
st.write("Make your tower as big as possible!")

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

# Wrap the chart in a scrollable container

fig = create_block_tower(st.session_state.tower_height)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

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