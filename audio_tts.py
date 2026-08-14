import asyncio
import os
import re
import tempfile
import edge_tts
from pygame import mixer

class SandroidTTS:
    def __init__(self, voice="id-ID-GadisNeural"):
        self.voice = voice
        if not mixer.get_init():
            mixer.init()

    async def _generate_audio(self, text: str, output_path: str):
        # Bersihkan karakter formatting/markdown agar artikulasi tetap mulus
        clean_text = re.sub(r'[\*\_\#\`]', '', text)
        communicate = edge_tts.Communicate(clean_text, self.voice)
        await communicate.save(output_path)

    def speak(self, text: str):
        """Memutar suara Sandroid dari teks input."""
        if not text or not text.strip():
            return
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name

        try:
            asyncio.run(self._generate_audio(text, temp_filename))
            
            mixer.music.load(temp_filename)
            mixer.music.play()
            while mixer.music.get_busy():
                pass
            mixer.music.unload()
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
