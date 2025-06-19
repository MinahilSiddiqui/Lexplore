# tts_utils.py

from gtts import gTTS
from io import BytesIO
import base64
import streamlit as st

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
