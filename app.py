import streamlit as st
import os
import json
from google import genai
from google.genai import types

st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 ComicCraft AI")
st.write("Turn your imagination into an original AI-powered comic.")

# API KEY
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is not configured.")
    st.info("Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# SIDEBAR
st.sidebar.header("⚙️ Comic Settings")

title = st.sidebar.text_input(
    "Comic Title",
    "The Almost Confession"
)

num_panels = st.sidebar.slider(
    "Number of Panels",
    1,
    4,
    4
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

# STORY IDEA
idea = st.text_area(
    "💡 Your Story Idea",
    "A shy college girl discovers that her mysterious classmate has a magical secret."
)

# GENERATE STORY
if st.button("✨ Generate Story", use_container_width=True):

    prompt = f"""
Create a coherent {num_panels}-panel comic story.

Title: {title}

Idea: {idea}

Requirements:
- The story must flow from panel to panel.
- Keep the same characters throughout.
- Each panel must continue the previous panel.
- Every panel needs a clear visual scene.
- Every panel needs short natural dialogue.
- Keep dialogue suitable for speech bubbles.

Return only valid JSON:

{{
  "panels": [
    {{
      "scene": "visual description",
      "dialogue": "short dialogue"
    }}
  ]
}}
"""

    try:
        with st.spinner("✍️ Creating your story..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

        story = json.loads(response.text)

        st.session_state["panels"] = story["panels"]

        st.success("🎉 Story created!")

    except Exception as error:
        st.error("❌ Story generation failed.")
        st.code(str(error))


# EDIT PANELS
if "panels" in st.session_state:

    st.subheader("📝 Edit Your Panels")

    panels = st.session_state["panels"]

    for index in range(len(panels)):

        st.markdown("### 🎬 Panel " + str(index + 1))

        panels[index]["scene"] = st.text_area(
            "Scene",
            panels[index]["scene"],
            key="scene_" + str(index)
        )

        panels[index]["dialogue"] = st.text_input(
            "Dialogue",
            panels[index]["dialogue"],
            key="dialogue_" + str(index)
        )

        st.divider()

    # GENERATE COMIC
    if st.button("🎨 Generate Comic", use_container_width=True):

        st.subheader("📖 Your AI Comic")

        for index, panel in enumerate(panels):

            image_prompt = f"""
Create a single illustrated comic panel.

Comic title: {title}

Panel number: {index + 1}

Scene:
{panel["scene"]}

Art style:
{art_style}

Create an actual illustrated comic panel.
Keep characters visually consistent.
Show clear expressions and body language.
Use cinematic comic composition.
Leave space for a speech bubble.
Do not put written dialogue inside the image.
Do not create placeholder boxes.
"""

            try:

                with st.spinner(
                    "🎨 Generating Panel " + str(index + 1) + "..."
                ):

                    image_response = client.models.generate_content(
                        model="gemini-2.5-flash-image",
                        contents=image_prompt
                    )

                image_found = False

                for part in image_response.parts:

                    if part.inline_data is not None:

                        image = part.as_image()

                        st.image(
                            image,
                            caption="Panel " + str(index + 1),
                            use_container_width=True
                        )

                        image_found = True
                        break

                if image_found:

                    st.markdown(
                        "💬 **Dialogue:** "
                        + panel["dialogue"]
                    )

                else:

                    st.warning(
                        "⚠️ No image was returned for Panel "
                        + str(index + 1)
                        + "."
                    )

            except Exception as error:

                st.error(
                    "❌ Panel "
                    + str(index + 1)
                    + " failed."
                )

                st.code(str(error))

            st.divider()

        st.success("🎉 Comic generation finished!")

else:

    st.info(
        "👆 Enter your story idea and click "
        "**Generate Story** to begin."
    )
