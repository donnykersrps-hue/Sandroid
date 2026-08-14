import asyncio
import os
import re
import tempfile
import edge_tts

class SandroidTTS:
    def __init__(self, voice="id-ID-GadisNeural"):
        self.voice = voice

    async def _generate_audio(self, text: str, output_path: str):
        # Bersihkan karakter formatting/markdown agar artikulasi tetap mulus
        clean_text = re.sub(r'[\*\_\#\`]', '', text)
        communicate = edge_tts.Communicate(clean_text, self.voice)
        await communicate.save(output_path)

    def generate_mp3(self, text: str) -> str:
        """Mengubah teks jadi file MP3 dan mengembalikan path filenya."""
        if not text or not text.strip():
            return None
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name

        asyncio.run(self._generate_audio(text, temp_filename))
        return temp_filename
