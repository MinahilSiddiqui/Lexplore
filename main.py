import os
import streamlit as st
from dotenv import load_dotenv

# Core imports
from llm_api import ask_llm
from web_search import search_web
from rag_engine import load_pdf, query_doc, index
from model_router import classify_query
from query import query_law
import tts_utils
import translation_utils
from voice_module import voice_assistant_ui  # Updated voice input

# Init
load_dotenv()
st.set_page_config(page_title="Lexplore", layout="wide")
st.title("⚖️🔍 Lexplore")

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_mode_active" not in st.session_state:
    st.session_state.pdf_mode_active = False

# Sidebar settings
with st.sidebar:
    st.header("🛠 Tools & Settings")

    audio_lang = st.selectbox("🔊 Audio Language", ["English", "Urdu"])
    uploaded_pdf = st.file_uploader("📄 Upload PDF", type="pdf")
    use_voice = st.toggle("🎤 Use Voice Input")

    if uploaded_pdf:
        load_pdf(uploaded_pdf)

# Voice or text input
user_input = None
source = "text"

if use_voice:
    st.subheader("🎤 Voice Input")
    if st.button("Click here for voice input"):
        spoken_text = voice_assistant_ui(lang=audio_lang)
        if spoken_text:
            st.success(f"🗣️ You said: {spoken_text}")
            user_input = spoken_text
            source = "voice"
        else:
            st.warning("No voice input detected or transcription failed.")
else:
    text_input = st.chat_input("Ask me anything...")
    if text_input:
        user_input = text_input
        source = "text"

# Chat logic
if user_input:
    st.chat_message("user").markdown(f"🎙️ *You said:* {user_input}" if source == "voice" else user_input)
    st.session_state.chat_history.append(("user", user_input))

    route = classify_query(user_input)

    # Reset mode if requested
    if route == "reset":
        st.session_state.pdf_mode_active = False
        route = "general"

    # If PDF mode is active and not web search, stick to PDF
    if st.session_state.pdf_mode_active and route != "web_search":
        route = "pdf_qa"

    # Activate PDF mode if relevant
    if route == "pdf_qa":
        st.session_state.pdf_mode_active = True

    with st.chat_message("assistant"):
        st.markdown(f"🔍 **Detected Mode:** `{route}`")
        lang_code = "ur" if audio_lang == "Urdu" else "en"

        try:
            # Route-based processing
            if route == "web_search":
                results = search_web(user_input)
                combined = ""
                for r in results:
                    st.markdown(f"- [{r['title']}]({r['link']})\n> {r['snippet']}")
                    combined += r['snippet'] + " "
                reply = combined or "No relevant results found."

            elif route == "pdf_qa":
                if uploaded_pdf and index is not None:
                    context = query_doc(user_input)
                    prompt = f"Use this document info to answer:\n\n{context}\n\nQ: {user_input}"
                    reply = ask_llm(prompt)
                else:
                    reply = "⚠️ Please upload a PDF before asking document-related questions."

            elif route == "legal":
                response = query_law(user_input)
                reply = response["result"]
                if response.get("source_documents"):
                    with st.expander("📄 Retrieved Law Sections"):
                        for doc in response["source_documents"]:
                            st.markdown(f"**Section:** {doc.metadata.get('section', 'N/A')}")
                            st.text(doc.page_content)

            else:
                reply = ask_llm(user_input)

        except Exception as e:
            reply = f"❌ Error: {e}"

        # Translate and speak
        speak_text = translation_utils.translate_to_urdu(reply) if lang_code == "ur" else reply
        audio_data = tts_utils.text_to_speech(speak_text, lang=lang_code)
        tts_utils.play_audio(audio_data)

        st.markdown(f"**🤖 Lexi:** {reply}")
        st.session_state.chat_history.append(("Lexi", reply))

# Re-display history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
