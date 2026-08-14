import speech_recognition as sr

class SandroidSTT:
    def __init__(self, language="id-ID"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def listen(self, timeout=6, phrase_time_limit=10) -> dict:
        """
        Mendengarkan ucapan dari mikrofon.
        Return dict format: {"status": "success/timeout/unknown/error", "text": "..."}
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return {"status": "success", "text": text}
            except sr.WaitTimeoutError:
                return {"status": "timeout", "text": "Sandroid tidak mendengar suara."}
            except sr.UnknownValueError:
                return {"status": "unknown", "text": "Suara kurang jelas terdeteksi."}
            except Exception as e:
                return {"status": "error", "text": str(e)}
