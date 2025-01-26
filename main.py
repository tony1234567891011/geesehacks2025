import streamlit as st
import plotly.graph_objects as go


def create_block_tower(height):
    """Creates a 2D block tower with the specified height, starting at the bottom."""
    fig = go.Figure()

    block_width = 1
    block_height = 0.5

    # Loop to create each block
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
            fillcolor=colour,
        )

    # Dynamically adjust figure height and y-axis range based on the number of blocks
    figure_height = max(800, height * block_height * 200)  # Ensure sufficient vertical space
    yaxis_range = [0, height * block_height + 1]  # Adjust y-axis to show all blocks

    # Customize layout
    fig.update_layout(
        title="2D Block Tower",
        xaxis=dict(visible=False, range=[-1, 1]),  # Centered horizontally
        yaxis=dict(visible=False, range=yaxis_range),  # Adjust y-axis for bottom alignment
        width=400,  # Fixed width
        height=figure_height,  # Dynamically set height
        margin=dict(l=50, r=50, t=50, b=50),  # Add margins for proper positioning
    )

    return fig


# Streamlit UI
st.title("Interactive 2D Block Tower Builder")

# Input for the tower height (1-20)
tower_height = st.slider("Select the height of the tower:", min_value=1, max_value=20, value=5)

# Generate the block tower
fig = create_block_tower(tower_height)

# Display the tower
st.plotly_chart(fig, use_container_width=True)

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