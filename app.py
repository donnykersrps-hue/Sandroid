import io
import re
import time
import streamlit as st
import streamlit.components.v1 as components
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
        .stApp {{
            background: linear-gradient(rgba(10, 10, 18, 0.70), rgba(10, 10, 18, 0.85)), 
                        url('{BACKGROUND_IMAGE_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #FAFAFA;
        }}

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

        .status-sleep {{
            color: #FFB703;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 10px #FFB703;
            margin-top: 5px;
        }}

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

        div[data-testid="stCustom"] iframe {{
            display: none;
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

# --- 3. SESSION STATE & TIMER INTI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_awake" not in st.session_state:
    st.session_state.is_awake = False

if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = time.time()

# Cek Auto-Sleep (5 Menit = 300 Detik)
SLEEP_TIMEOUT = 300
if st.session_state.is_awake and (time.time() - st.session_state.last_interaction > SLEEP_TIMEOUT):
    st.session_state.is_awake = False

# --- 4. DISPLAY HUD UTAMA ---
status_html = '<div class="status-online">● HUMANOID SYSTEM ONLINE</div>' if st.session_state.is_awake else '<div class="status-sleep">🌙 SYSTEM SLEEP (PRESS ENTER TO WAKE)</div>'

st.markdown(f"""
    <div class="sandroid-card">
        <div class="sandroid-avatar">🤖</div>
        <div class="sandroid-title">SANDROID</div>
        {status_html}
    </div>
""", unsafe_allow_html=True)

# --- 5. PANEL PENDENGARAN & AUTO-STANDBY JS ---
st.markdown('<div class="mic-box">', unsafe_allow_html=True)
if st.session_state.is_awake:
    st.write("🎙️ **Modul Pendengaran Aktif (Standby)**")
    st.caption("Sandroid sedang menyimak ucapan Kak Donny secara langsung...")
else:
    st.write("💤 **Modul Pendengaran Tertidur**")
    st.caption("Tekan tombol **[ ENTER ]** pada keyboard untuk membangunkan Sandroid.")

audio = mic_recorder(
    start_prompt="🔴 Buka Pendengaran",
    stop_prompt="⬛ Selesai",
    key='sandroid_continuous_listener'
)
st.markdown('</div>', unsafe_allow_html=True)

# Event Listener: Mengaktifkan Mic lewat Enter ATAU Otomatis setelah Suara Sandroid Selesai Diputar
components.html("""
    <script>
        const doc = window.parent.document;
        
        // Fungsi untuk trigger tombol mic tersembunyi
        function startListening() {
            const iframes = doc.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                const btn = iframe.contentDocument?.querySelector('button');
                if (btn) btn.click();
            });
        }

        // Listener 1: Tombol ENTER Manual
        doc.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                startListening();
            }
        });

        // Listener 2: Auto-Standby setelah Audio Sandroid Selesai Berbicara
        setInterval(() => {
            const audioElements = doc.querySelectorAll('audio');
            audioElements.forEach(audio => {
                if (!audio.dataset.hasEndedListener) {
                    audio.dataset.hasEndedListener = "true";
                    audio.onended = function() {
                        setTimeout(() => {
                            startListening();
                        }, 500); // Jeda 0.5 detik agar mulus
                    };
                }
            });
        }, 1000);
    </script>
""", height=0)

# --- 6. LOGIKA PEMROSESAN ---
if audio:
    user_text = transcribe_audio(audio['bytes'])
    
    if user_text not in ["UNKNOWN"] and not user_text.startswith("ERROR"):
        if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio['id']:
            st.session_state.last_processed_audio = audio['id']
            
            st.session_state.is_awake = True
            st.session_state.last_interaction = time.time()
            
            st.session_state.messages.append({"role": "user", "content": user_text})
            
            response_text = f"Halo Kak Donny! Aku dengar kamu bilang '{user_text}'. Ada hal menarik apa lagi yang mau kita bahas?"
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            audio_file = tts_engine.generate_mp3(response_text)
            if audio_file:
                st.audio(audio_file, format="audio/mp3", autoplay=True)

# --- 7. TRANSKRIP PERCAKAPAN (MEMORY LOG) ---
with st.expander("📄 Transkrip Percakapan (Memory Log)"):
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role_label = "👤 Kak Donny" if msg["role"] == "user" else "🤖 Sandroid"
            st.write(f"**{role_label}:** {msg['content']}")
    else:
        st.caption("Belum ada riwayat percakapan.")
