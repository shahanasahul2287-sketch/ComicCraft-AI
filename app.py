import streamlit as st

st.set_page_config(page_title="ComicCraft AI")

st.title("🎨 ComicCraft AI")
st.write("Turn your imagination into an AI-powered comic!")

title = st.text_input("Comic Title", "My Amazing Comic")

idea = st.text_area(
    "💡 Your Story Idea",
    "A college student arrives late to class and something funny happens."
)

style = st.selectbox(
    "🎨 Art Style",
    ["Classic Comic", "Classic Manga", "Cartoon", "Anime"]
)

panels = st.slider("Number of Panels", 1, 6, 4)

if st.button("✨ Generate Story"):
    st.success("🎉 Comic generation started!")
    st.write("Title:", title)
    st.write("Story idea:", idea)
    st.write("Style:", style)
    st.write("Number of panels:", panels)

st.subheader("🎨 Comic Panels")

panel1 = st.text_area(
    "Panel 1",
    "The student enters the classroom late."
)

panel2 = st.text_area(
    "Panel 2",
    "Everyone looks at the student."
)

panel3 = st.text_area(
    "Panel 3",
    "The teacher smiles at the student."
)

panel4 = st.text_area(
    "Panel 4",
    "Everyone laughs together."
)

if st.button("✨ Show Panels"):
    st.write("### 🖼️ Panel 1")
    st.write(panel1)

    st.write("### 🖼️ Panel 2")
    st.write(panel2)

    st.write("### 🖼️ Panel 3")
    st.write(panel3)

    st.write("### 🖼️ Panel 4")
    st.write(panel4)

    st.markdown("---")

st.markdown("## 🎨 Your Comic Panels")

panel1 = st.file_uploader(
    "🖼️ Panel 1",
    type=["png", "jpg", "jpeg"],
    key="upload_panel_1"
)

panel2 = st.file_uploader(
    "🖼️ Panel 2",
    type=["png", "jpg", "jpeg"],
    key="upload_panel_2"
)

panel3 = st.file_uploader(
    "🖼️ Panel 3",
    type=["png", "jpg", "jpeg"],
    key="upload_panel_3"
)

panel4 = st.file_uploader(
    "🖼️ Panel 4",
    type=["png", "jpg", "jpeg"],
    key="upload_panel_4"
)

if panel1:
    st.image(panel1, caption="Panel 1", width="stretch")

if panel2:
    st.image(panel2, caption="Panel 2", width="stretch")

if panel3:
    st.image(panel3, caption="Panel 3", width="stretch")

if panel4:
    st.image(panel4, caption="Panel 4", width="stretch")

st.markdown("## 🎨 Your Comic")

comic_image = st.file_uploader(
    "Upload your 4-panel comic",
    type=["png", "jpg", "jpeg"],
    key="comic_image"
)

if comic_image:
    st.image(
        comic_image,
        caption="🎨 ComicCraft AI - 4 Panel Comic",
        width="stretch"
    )

    st.success("🎉 Your ComicCraft AI comic is ready!")
