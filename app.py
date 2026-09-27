import streamlit as st
from google import genai

st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 ComicCraft AI")
st.write("Turn your imagination into an original AI-powered comic.")

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.info("Add GEMINI_API_KEY in Streamlit → Manage app → Settings → Secrets.")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)

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

idea = st.text_area(
    "💡 Your Story Idea",
    placeholder="Example: A shy college girl discovers a magical talking cat..."
)

if st.button("✨ Generate Story", use_container_width=True):

    if not idea.strip():
        st.warning("Please enter your story idea first.")
        st.stop()

    prompt = f"""
Create an original comic story.

Title: {title}
Number of panels: {panels}
Art style: {style}

Story idea:
{idea}

For each panel provide:
1. Panel number
2. Scene description
3. Character dialogue
4. Narration

Make the story fun, clear and suitable for a college project.
"""

    with st.spinner("🎨 Creating your comic story..."):

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            st.success("🎉 Comic story generated!")

            st.markdown("## 📖 Your Comic")
            st.markdown(response.text)

        except Exception as e:
            st.error("❌ Story generation failed.")
            st.code(str(e))
