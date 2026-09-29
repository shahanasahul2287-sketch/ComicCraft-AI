import streamlit as st
import base64
import time
from google import genai


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 ComicCraft AI")
st.write("Turn your imagination into an original AI-powered comic.")


# --------------------------------------------------
# GET API KEY
# --------------------------------------------------

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("❌ GEMINI_API_KEY is not configured.")
    st.info(
        "Go to Streamlit → Manage app → Settings → Secrets "
        "and add GEMINI_API_KEY."
    )
    st.stop()


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ Comic Settings")

title = st.sidebar.text_input(
    "Comic Title",
    "My Amazing Comic"
)

panels = st.sidebar.slider(
    "Number of Panels",
    1,
    6,
    4
)

style = st.sidebar.selectbox(
    "Art Style",
    [
        "Classic Comic",
        "Classic Manga",
        "Cartoon",
        "Anime"
    ]
)


# --------------------------------------------------
# STORY IDEA
# --------------------------------------------------

idea = st.text_area(
    "💡 Your Story Idea",
    placeholder="Example: A shy college girl discovers a magical talking cat..."
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button("✨ Generate Story", use_container_width=True):

    if not idea.strip():
        st.warning("⚠️ Please enter your story idea first.")
        st.stop()


    # --------------------------------------------------
    # CREATE STORY
    # --------------------------------------------------

    story_prompt = f"""
Create an original comic story.

Comic Title: {title}

Number of Panels: {panels}

Art Style: {style}

Story Idea:
{idea}

Create exactly {panels} panels.

For each panel provide:

Panel Number:
Scene:
Characters:
Dialogue:
Narration:

Keep the story simple, fun and suitable for a college project.

Make sure every panel has a clear scene that can be turned into an image.
"""


    with st.spinner("📖 Creating your comic story..."):

        try:

            story_response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=story_prompt
            )

            story_text = story_response.text

        except Exception as e:

            st.error("❌ Story generation failed.")
            st.code(str(e))
            st.stop()


    # --------------------------------------------------
    # SHOW STORY
    # --------------------------------------------------

    st.success("🎉 Comic story generated!")

    st.markdown("---")
    st.markdown("## 📖 Your Comic Story")

    st.markdown(story_text)


    # --------------------------------------------------
    # GENERATE COMIC IMAGES
    # --------------------------------------------------

    st.markdown("---")
    st.markdown("## 🎨 Generated Comic Panels")

    st.info(
        "The AI is now creating the comic artwork. "
        "This may take a little time."
    )


    # Generate each panel separately
    for panel_number in range(1, panels + 1):

        st.markdown(f"### 🖼️ Panel {panel_number}")

        image_prompt = f"""
Create ONE comic panel image for an original story.

Comic title:
{title}

Panel number:
{panel_number} of {panels}

Art style:
{style}

Original story idea:
{idea}

Story information:
{story_text}

Create a visually clear comic scene for panel {panel_number}.

IMPORTANT:
- Generate ONLY the artwork for this panel.
- Do not create multiple panels.
- Do not create a comic page containing several panels.
- Keep the same characters and visual appearance throughout the story.
- Use expressive characters.
- Use a clean composition.
- Make it suitable for a college project.
- Leave enough visual space for speech bubbles.
- Do NOT write dialogue inside the image.
- Do NOT add random text.
- Make the image look like a polished {style} comic illustration.
"""


        try:

            with st.spinner(
                f"🎨 Creating Panel {panel_number}..."
            ):

                interaction = client.interactions.create(
                    model="gemini-3.1-flash-image",
                    input=image_prompt,
                    response_format={
                        "type": "image",
                        "aspect_ratio": "16:9",
                        "image_size": "1K"
                    }
                )


            # Get generated image
            if interaction.output_image:

                image_data = base64.b64decode(
                    interaction.output_image.data
                )

                st.image(
                    image_data,
                    use_container_width=True
                )

                st.success(
                    f"✅ Panel {panel_number} created!"
                )

            else:

                st.warning(
                    f"⚠️ No image was returned for Panel {panel_number}."
                )


        except Exception as e:

            st.error(
                f"❌ Panel {panel_number} image generation failed."
            )

            st.code(str(e))


        # Small pause between image requests
        time.sleep(1)


    # --------------------------------------------------
    # FINISHED
    # --------------------------------------------------

    st.markdown("---")

    st.success(
        "🎉 Your ComicCraft AI comic is ready!"
    )

    st.balloons()
