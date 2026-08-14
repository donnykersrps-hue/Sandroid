import io
import re
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from core.audio_tts import SandroidTTS
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTING HALAMAN & STYLING FUTURISTIK ---
st.set_page_config(page_title="Sandroid - Humanoid AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
        /* Modern Dark Theme Styling */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .sandroid-card {
            background: linear-gradient(135deg, #1E1E2E 0%, #2D2D44 100%);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 25px;
        }
        .sandroid-avatar {
            font-size: 80px;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 15px #7928CA);
        }
        .status-online {
            color: #00FF87;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1px;
        }
        .mic-box {
            background-color: #161B22;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #30363D;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Engine Suara
@st.cache_resource
def load_tts():
    return SandroidTTS()

tts_engine = load_tts()

# --- 2. FUNGSI TRANSSKRIPSI SUARA (STT) ---
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

# --- 3. DISPLAY UTAMA SANDROID (VISUAL HUD) ---
st.markdown("""
    <div class="sandroid-card">
        <div class="sandroid-avatar">🤖</div>
        <h2 style="margin: 0; color: #FFFFFF;">SANDROID</h2>
        <p class="status-online">● HUMANOID ACTIVE & LISTENING</p>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. AREA KONTROL SUARA ---
st.markdown('<div class="mic-box">', unsafe_allow_html=True)
st.write("🎙️ **Telinga Sandroid (Aktif):**")
st.caption("Bicaralah secara alami. Akhiri kalimat dengan **'jawab aku'** agar Sandroid merespons.")

# Widget Perekam Audio (Auto-Detect / Sekali Klik Buka Mic)
audio = mic_recorder(
    start_prompt="🎙️ Buka Pendengaran",
    stop_prompt="⏹️ Hentikan",
    key='continuous_recorder'
)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. LOGIKA PEMROSESAN PERCAKAPAN & TRIGGER "JAWAB AKU" ---
if audio:
    user_text = transcribe_audio(audio['bytes'])
    
    if user_text not in ["UNKNOWN"] and not user_text.startswith("ERROR"):
        if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio['id']:
            st.session_state.last_processed_audio = audio['id']
            
            st.session_state.messages.append({"role": "user", "content": user_text})
            
            # CEK KATA KUNCI TRIGGER: "jawab aku"
            clean_input = user_text.lower().strip()
            if "jawab aku" in clean_input:
                # Menghapus frasa "jawab aku" agar tidak mengotori jawaban
                prompt_content = re.sub(r'jawab\s+aku', '', user_text, flags=re.IGNORECASE).strip()
                
                # Respon sementara Sandroid
                if prompt_content:
                    response_text = f"Siap Kak Donny, aku mendengar permintaanmu: '{prompt_content}'."
                else:
                    response_text = "Iya Kak Donny, Sandroid di sini. Ada yang bisa aku bantu?"
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Putar Suara Jawaban Sandroid
                audio_file = tts_engine.generate_mp3(response_text)
                if audio_file:
                    st.audio(audio_file, format="audio/mp3", autoplay=True)

# --- 6. RIWAYAT PERCAKAPAN (SEMBUNYI / EXPANDABLE) ---
st.write("")
with st.expander("📄 Lihat Transkrip Percakapan (Hidden Log)"):
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role_label = "👤 Kak Donny" if msg["role"] == "user" else "🤖 Sandroid"
            st.write(f"**{role_label}:** {msg['content']}")
    else:
        st.caption("Belum ada riwayat obrolan.")
