
# voice_bot.py

import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64
import streamlit as st

def recognize_speech(language_code="en-US"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = recognizer.listen(source, phrase_time_limit=15)

    try:
        text = recognizer.recognize_google(audio, language=language_code)
        return text
    except Exception as e:
        st.error(f"Speech Recognition error: {e}")
        return ""

def text_to_speech(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

def play_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes.read()).decode()
    audio_html = f"""
    <audio controls autoplay>
      <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Refactored to only handle input, not response generation
def voice_assistant_ui(lang="English"):
    lang_code = "en-US" if lang == "English" else "ur-PK"
    return recognize_speech(language_code=lang_code)
