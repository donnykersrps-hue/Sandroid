import io
import re
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from core.audio_tts import SandroidTTS
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTING HALAMAN & THEME CYBERPUNK NEON ---
st.set_page_config(
    page_title="Sandroid - Humanoid AI", 
    page_icon="🤖", 
    layout="centered"
)

BACKGROUND_IMAGE_URL = "https://raw.githubusercontent.com/donnykersrps-hue/Sandroid/main/background.jpg"

st.markdown(f"""
    <style>
        /* Cyberpunk Neon Background Overlay */
        .stApp {{
            background: linear-gradient(rgba(10, 10, 18, 0.70), rgba(10, 10, 18, 0.85)), 
                        url('{BACKGROUND_IMAGE_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #FAFAFA;
        }}

        /* Glassmorphism Sandroid HUD Card */
        .sandroid-card {{
            background: rgba(18, 18, 32, 0.55);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 24px;
            padding: 30px;
            text-align: center;
            border: 1px solid rgba(236, 72, 153, 0.35);
            box-shadow: 0 0 30px rgba(236, 72, 153, 0.25), inset 0 0 20px rgba(0, 240, 255, 0.15);
            margin-bottom: 25px;
        }}

        .sandroid-avatar {{
            font-size: 80px;
            margin-bottom: 5px;
            filter: drop-shadow(0 0 18px #ec4899);
        }}

        .sandroid-title {{
            margin: 0;
            color: #FFFFFF;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }}

        .status-online {{
            color: #00F0FF;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 10px #00F0FF;
            margin-top: 5px;
        }}

        /* Glass Box Control Tempat Mic */
        .mic-box {{
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
            text-align: center;
            margin-bottom: 20px;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- 2. INISIALISASI ENGINE ---
@st.cache_resource
def load_tts():
    return SandroidTTS()

tts_engine = load_tts()

def transcribe_audio(audio_bytes):
    """Konversi audio WEBM browser -> WAV -> Teks (Google STT)"""
    recognizer = sr.Recognizer()
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="id-ID")
            return text
    except sr.UnknownValueError:
        return "UNKNOWN"
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- 3. DISPLAY HUD UTAMA ---
st.markdown("""
    <div class="sandroid-card">
        <div class="sandroid-avatar">🤖</div>
        <div class="sandroid-title">SANDROID</div>
        <div class="status-online">● HUMANOID SYSTEM ONLINE</div>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. PANEL PENDENGARAN ---
st.markdown('<div class="mic-box">', unsafe_allow_html=True)
st.write("🎙️ **Modul Pendengaran Aktif**")
st.caption("Klik tombol mikrofon di bawah untuk mulai mengobrol secara otomatis bersama Sandroid.")

audio = mic_recorder(
    start_prompt="🔴 Buka Pendengaran",
    stop_prompt="⬛ Selesai",
    key='sandroid_continuous_listener'
)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. LOGIKA PEMROSESAN TANPA TRIGGER ("AUTO-HUMAN RESPONSE") ---
if audio:
    user_text = transcribe_audio(audio['bytes'])
    
    if user_text not in ["UNKNOWN"] and not user_text.startswith("ERROR"):
        # Pencegahan pemrosesan ulang audio ID yang sama saat Streamlit rerun
        if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio['id']:
            st.session_state.last_processed_audio = audio['id']
            
            # Rekam pesan user ke dalam memory session
            st.session_state.messages.append({"role": "user", "content": user_text})
            
            # Respon Alami tanpa Kata Kunci & tanpa Pengumuman Modul Sistem
            # [Catatan: Tempat ini siap disambungkan ke API LLM/Gemini sesuai sandroid_persona.json]
            response_text = f"Halo Kak Donny! Aku dengar tadi kamu bilang '{user_text}'. Ada hal menarik apa lagi yang mau kita bahas?"
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            # Trigger Audio Output TTS
            audio_file = tts_engine.generate_mp3(response_text)
            if audio_file:
                st.audio(audio_file, format="audio/mp3", autoplay=True)

# --- 6. TRANSKRIP PERCAKAPAN (HIDDEN LOG) ---
with st.expander("📄 Transkrip Percakapan (Hidden Log)"):
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role_label = "👤 Kak Donny" if msg["role"] == "user" else "🤖 Sandroid"
            st.write(f"**{role_label}:** {msg['content']}")
    else:
        st.caption("Belum ada riwayat percakapan.")
