import streamlit as st

st.set_page_config(
    page_title="Comic Craft",
    layout="wide"
)

st.title("🎨 Comic Craft Studio")
st.caption("Design comic strips with custom panels, prompts, and dialogues.")

# Sidebar
with st.sidebar:
    st.header("Comic Settings")

    comic_title = st.text_input(
        "Comic Title",
        value="The Almost Confession"
    )

    num_panels = st.slider(
        "Number of Panels",
        min_value=1,
        max_value=4,
        value=4
    )

    art_style = st.selectbox(
        "Art Style",
        [
            "Classic Manga",
            "Western Comic",
            "Pixel Art",
            "Watercolor",
            "Cartoon"
        ]
    )

st.subheader(comic_title)

# Comic content
panel_data = [
    (
        "A girl studies quietly in a college library while a shy boy at the next table secretly looks at her.",
        "Why do I keep looking at her instead of my book?"
    ),
    (
        "The girl notices him staring and gives him a small playful smile before returning to her book.",
        "You've been staring at that page for ten minutes."
    ),
    (
        "The boy becomes shy and smiles. He gathers courage to talk to her.",
        "Maybe I was waiting for the courage to talk to you."
    ),
    (
        "They walk out of the library together, smiling and talking.",
        "Can we study together tomorrow?"
    )
]

# Panel preview
st.subheader("📝 Comic Panels")

cols = st.columns(num_panels)

for i, col in enumerate(cols):
    with col:
        st.markdown(f"### Panel {i + 1}")

        st.text_area(
            f"Scene Description {i + 1}",
            value=panel_data[i][0],
            key=f"scene_{i}"
        )

        st.text_input(
            f"Speech Bubble {i + 1}",
            value=panel_data[i][1],
            key=f"dialogue_{i}"
        )

        st.info("🖼️ Image will appear here")

# Generate button
st.divider()

if st.button("🎨 Generate Comic", use_container_width=True):
    st.subheader("🖼️ Generated Comic")

    st.success("🎉 Comic generation completed!")

    for i in range(num_panels):
        st.markdown(f"### Panel {i + 1}")

        st.write(panel_data[i][0])

        st.info(f"💬 {panel_data[i][1]}")
