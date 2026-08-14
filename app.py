import streamlit as st
from core.audio_tts import SandroidTTS
from core.audio_stt import SandroidSTT

st.set_page_config(page_title="Sandroid Humanoid AI", page_icon="🤖", layout="centered")

# Inisialisasi Modul
@st.cache_resource
def load_modules():
    return SandroidSTT(), SandroidTTS()

stt_engine, tts_engine = load_modules()

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
    if st.button("🎙️ Bicara dengan Sandroid", use_container_width=True, type="primary"):
        st.toast("🎤 Sandroid sedang mendengarkan...", icon="🔴")
        result = stt_engine.listen()
        
        if result["status"] == "success":
            user_text = result["text"]
            st.session_state.messages.append({"role": "user", "content": user_text})
            
            # Respon sementara sebelum disambungkan ke Otak Cloud Uncensored
            response_text = f"Sandroid mendengar Kak Donny mengucapkan: '{user_text}'. Struktur repositori kita berjalan dengan lancar!"
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.rerun()
        else:
            st.warning(result["text"])

with col2:
    if st.button("🔊 Tes Suara Sandroid", use_container_width=True):
        tts_engine.speak("Halo Kak Donny, sistem modular repositori kita sudah berfungsi dengan sangat baik.")

# Auto play suara respon Sandroid
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_msg = st.session_state.messages[-1]["content"]
    if "last_spoken" not in st.session_state or st.session_state.last_spoken != last_msg:
        st.session_state.last_spoken = last_msg
        tts_engine.speak(last_msg)
