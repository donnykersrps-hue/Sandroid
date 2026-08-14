import io
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from core.audio_tts import SandroidTTS
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Sandroid Humanoid AI", page_icon="🤖", layout="centered")

# Inisialisasi Modul TTS
@st.cache_resource
def load_tts():
    return SandroidTTS()

tts_engine = load_tts()

# Fungsi konversi audio browser (WEBM) -> WAV -> Teks (STT)
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    try:
        # Konversi format audio WEBM/OGG dari browser ke WAV
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

st.title("🤖 Sandroid Dashboard")
st.caption("Humanoid Engine | Repository Mode (Modular Architecture)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo Kak Donny... Sistem repositori Sandroid sudah aktif. Suara dan pendengaranku sudah siap!"}
    ]

# Tampilkan riwayat percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("🎙️ **Bicara dengan Sandroid:**")
    audio = mic_recorder(
        start_prompt="🔴 Klik untuk Bicara",
        stop_prompt="⬛ Selesai Bicara",
        key='recorder'
    )

    if audio:
        user_text = transcribe_audio(audio['bytes'])
        
        if user_text == "UNKNOWN":
            st.warning("Suara kurang jelas terdeteksi. Boleh diulangi Kak Donny?")
        elif user_text.startswith("ERROR"):
            st.error(f"Gagal memproses audio: {user_text}")
        else:
            if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio['id']:
                st.session_state.last_processed_audio = audio['id']
                
                st.session_state.messages.append({"role": "user", "content": user_text})
                
                response_text = f"Sandroid mendengar Kak Donny mengucapkan: '{user_text}'. Pendengaranku dari browser sudah berjalan lancar!"
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.rerun()

with col2:
    st.write("🔊 **Tes Suara Sandroid:**")
    if st.button("Play Voice Test", use_container_width=True):
        audio_file = tts_engine.generate_mp3("Halo Kak Donny, sistem suara dan pendengaranku lewat browser sudah berfungsi sempurna.")
        if audio_file:
            st.audio(audio_file, format="audio/mp3", autoplay=True)

# Auto play suara respon Sandroid
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_msg = st.session_state.messages[-1]["content"]
    if "last_spoken" not in st.session_state or st.session_state.last_spoken != last_msg:
        st.session_state.last_spoken = last_msg
        audio_file = tts_engine.generate_mp3(last_msg)
        if audio_file:
            st.audio(audio_file, format="audio/mp3", autoplay=True)
