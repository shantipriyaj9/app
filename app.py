import os
import streamlit as st
from PIL import Image
from google import genai

MODEL = "gemini-3.5-flash"    # model ka naam. Error aaye to yahi badalna hai

st.set_page_config(page_title="Image + Text Chatbot", page_icon="🤖")
st.title("🤖 Image + Text Chatbot (Gemini)")

# API key: pehle Streamlit Secrets se, nahi mila to sidebar me type karwao
# DHYAN: "GEMINI_API_KEY" sirf ek NAAM hai. Apni asli key yahan mat likhna.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API key", type="password")

# Sidebar me image upload (optional)
uploaded = st.sidebar.file_uploader("Image upload karo (optional)", type=["jpg", "jpeg", "png", "webp"])
image = None
if uploaded is not None:
    image = Image.open(uploaded).convert("RGB")
    st.sidebar.image(image, caption="Aapki image")

# Chat history yaad rakhna (Streamlit script baar-baar chalti hai)
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Image ke baare me kuch pucho, ya koi bhi sawaal likho...")

if question:
    if not api_key:
        st.error("Pehle sidebar me Gemini API key daalo.")
        st.stop()

    with st.chat_message("user"):
        st.markdown(question)

    history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.messages)
    text_part = f"Pichli baatcheet:\n{history}\n\nNaya sawaal: {question}" if history else question

    contents = []
    if image is not None:
        contents.append(image)
    contents.append(text_part)

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                client = genai.Client(api_key=api_key)
                reply = client.models.generate_content(model=MODEL, contents=contents).text
            except Exception as e:
                reply = f"Error aaya: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})