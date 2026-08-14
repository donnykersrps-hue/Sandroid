import io
import re
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from core.audio_tts import SandroidTTS
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTING HALAMAN & THEME CYBERPUNK/NEON ---
st.set_page_config(page_title="Sandroid - Humanoid AI", page_icon="🤖", layout="centered")

# URL Gambar background dari repositori / image link Kak Donny
BACKGROUND_IMAGE_URL = "https://raw.githubusercontent.com/donnykersrps-hue/Sandroid/main/background.jpg" # atau URL gambar di atas

st.markdown(f"""
    <style>
        /* Cyberpunk Neon Background */
        .stApp {{
            background: linear-gradient(rgba(14, 17, 23, 0.65), rgba(14, 17, 23, 0.85)), 
                        url('{BACKGROUND_IMAGE_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #FAFAFA;
        }}

        /* Glassmorphism Card Sandroid */
        .sandroid-card {{
            background: rgba(20, 20, 35, 0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 35px;
            text-align: center;
            border: 1px solid rgba(236, 72, 153, 0.3);
            box-shadow: 0 0 25px rgba(236, 72, 153, 0.25), inset 0 0 15px rgba(59, 130, 246, 0.15);
            margin-bottom: 25px;
        }}

        .sandroid-avatar {{
            font-size: 85px;
            margin-bottom: 5px;
            filter: drop-shadow(0 0 20px #ec4899);
        }}

        .status-online {{
            color: #00F0FF;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 8px #00F0FF;
        }}

        /* Container Mic & Control */
        .mic-box {{
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
            text-align: center;
        }}

        /* Styling Expander Log Chat */
        .st-emotion-cache-1h9usn1 {{
            background: rgba(15, 23, 42, 0.6) !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
    </style>
""", unsafe_allow_html=True)
