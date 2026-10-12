import os
from io import BytesIO

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Vision Chatbot",
    page_icon="👁️",
    layout="centered",
)

st.markdown("""
<style>
.block-container {max-width: 1000px; padding-top: 2rem;}
.hero {padding: 1.5rem 1.5rem 1.2rem; border-radius: 20px; background: linear-gradient(135deg,#111827,#312e81); color: white; margin-bottom: 1rem;}
.hero h1 {margin-bottom: .35rem;}
.hero p {margin: 0; opacity: .9;}
.badge {display:inline-block; padding:.25rem .65rem; border-radius:999px; background:#ffffff22; font-size:.8rem; margin-bottom:.5rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="badge">🚀 AI Vision Chatbot</div>
  <h1>See it. Understand it. Chat about it.</h1>
  <p>Upload an image and ask Gemini questions about what it sees.</p>
</div>
""", unsafe_allow_html=True)


def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")


api_key = get_api_key()
if not api_key:
    st.warning("Add your Gemini API key to continue. See the README for setup steps.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "mime_type" not in st.session_state:
    st.session_state.mime_type = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📷 Image")
    uploaded = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Use a clear image for better results.",
    )

    if uploaded is not None:
        new_bytes = uploaded.getvalue()
        if new_bytes != st.session_state.image_bytes:
            st.session_state.image_bytes = new_bytes
            st.session_state.mime_type = uploaded.type or "image/jpeg"
            st.session_state.messages = []

    if st.session_state.image_bytes:
        preview = Image.open(BytesIO(st.session_state.image_bytes))
        st.image(preview, caption="Current image", use_container_width=True)
        if st.button("🗑️ Clear image", use_container_width=True):
            st.session_state.image_bytes = None
            st.session_state.mime_type = None
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.caption("Model: Gemini multimodal vision")
    st.caption("Tip: Ask specific questions such as ‘What objects are visible?’ or ‘Describe the scene.’")

if not st.session_state.image_bytes:
    st.info("👈 Upload an image from the sidebar to start.")
    st.stop()

# Display existing chat history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def ask_vision_model(question: str) -> str:
    image_part = types.Part.from_bytes(
        data=st.session_state.image_bytes,
        mime_type=st.session_state.mime_type or "image/jpeg",
    )

    history_text = "\n".join(
        f'{m["role"].upper()}: {m["content"]}'
        for m in st.session_state.messages[-8:]
    )

    prompt = f"""
You are an AI vision assistant.
Analyze the uploaded image carefully and answer the user's question.
Be accurate and do not invent details that are not visible.
If something is uncertain, say so.
Keep answers clear and useful.

Conversation so far:
{history_text or '(none)'}

USER'S NEW QUESTION:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=[image_part, prompt],
    )
    return response.text or "I couldn't generate a text response for that question."


if prompt := st.chat_input("Ask something about the image…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("👁️ Looking at the image…"):
            try:
                answer = ask_vision_model(prompt)
            except Exception as exc:
                answer = f"Sorry, I couldn't analyze the image right now.\n\nError: `{exc}`"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("Built with Streamlit + Google Gemini multimodal AI")
