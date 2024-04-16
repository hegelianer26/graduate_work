
import speech_recognition as sr
import io
from gtts import gTTS


class Speech_and_text():

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.dictor = gTTS

    async def recognize(self, file_input):

        audio_data = await file_input.read()

        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = self.recognizer.record(source)

        try:
            transcription = self.recognizer.recognize_google(
                audio, language="ru-RU")
        except sr.UnknownValueError:
            return {
                "transcription": "Speech recognition could not understand the audio"}
        except sr.RequestError as e:
            return {
                "transcription": f"Could not request results from' Google Web Speech API; {e}"}
        transcription = transcription.lower()

        return transcription

    async def dictate(self, text):
        speech = self.dictor(text=text, lang='ru')
        output_file = "output.mp3"
        speech.save(output_file)
        return output_file


def get_tts():
    tts = Speech_and_text()
    return tts
