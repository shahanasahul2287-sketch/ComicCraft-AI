import streamlit as st
import os
import json
from google import genai
from google.genai import types

# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 ComicCraft AI")
st.write("Turn your imagination into an original AI-powered comic.")

# --------------------------------------------------
# API
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is missing.")
    st.stop()

client = genai.Client(api_key=api_key)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ Comic Settings")

title = st.sidebar.text_input(
    "Comic Title",
    "The Almost Confession"
)

num_panels = st.sidebar.slider(
    "Number of Panels",
    min_value=1,
    max_value=4,
    value=4
)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Classic Manga",
        "Anime",
        "Comic Book",
        "Watercolor",
        "Cartoon"
    ]
)

# --------------------------------------------------
# STORY IDEA
# --------------------------------------------------

idea = st.text_area(
    "💡 What should your comic be about?",
    "A shy college girl discovers that her mysterious classmate has a magical secret."
)

# --------------------------------------------------
# GENERATE STORY
# --------------------------------------------------

if st.button("✨ Generate Story", use_container_width=True):

    story_prompt = f"""
Create a coherent {num_panels}-panel comic story.

Comic title:
{title}

Story idea:
{idea}

Art style:
{art_style}

Requirements:
- The story must flow naturally from panel to panel.
- Keep the same characters throughout.
- Each panel must continue from the previous panel.
- Give every panel a clear visual scene.
- Give every panel natural dialogue.
- Keep dialogue short enough for a comic speech bubble.
- Do not make the story repetitive.

Return ONLY valid JSON in this format:

{{
  "panels": [
    {{
      "scene": "Detailed visual description of the panel",
      "dialogue": "Short character dialogue"
    }}
  ]
}}
"""

    try:

        with st.spinner("✍️ Creating your story..."):

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=story_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

        data = json.loads(response.text)

        st.session_state["comic_panels"] = data["panels"]

        st.success("🎉 Story created! You can edit the panels below.")

    except Exception as e:

        st.error("❌ Story generation failed.")
        st.code(str(e))

# --------------------------------------------------
# EDIT PANELS
# --------------------------------------------------

if "comic_panels" in st.session_state:

    st.subheader("📝 Edit Your Comic Panels")

    panels = st.session_state["comic_panels"]

    for i in range(len(panels)):

        st.markdown(f"### 🎬 Panel {i + 1}")

        panels[i]["scene"] = st.text_area(
            "Scene description",
            panels[i]["scene"],
            key=f"scene_{i}"
        )

        panels[i]["dialogue"] = st.text_input(
            "Dialogue",
            panels[i]["dialogue"],
            key=f"dialogue_{i}"
        )

        st.divider()

    # --------------------------------------------------
    # GENERATE ACTUAL IMAGES
    # --------------------------------------------------

    if st.button("🎨 Generate Comic Images", use_container_width=True):

        st.subheader("📖 Your AI Comic")

        for i, panel in enumerate(panels):

            image_prompt = f"""
Create a single comic panel image.

Comic title:
{title}

Panel:
{i + 1} of {len(panels)}

Scene:
{panel["scene"]}

Dialogue context:
{panel["dialogue"]}

Art style:
{art_style}

Important visual requirements:
- Create an actual illustrated comic panel.
- Keep the characters visually consistent.
- Make the scene match the description.
- Clear facial expressions and body language.
- Cinematic comic composition.
- Leave suitable space for a speech bubble.
- Do NOT write the dialogue as text inside the image.
- No placeholder boxes.
- No words such as "Image will appear here".
"""

            try:

                with st.spinner(
                    f"🎨
