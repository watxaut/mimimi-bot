import logging
import tempfile
import urllib.request as url
from pathlib import Path

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

logger = logging.getLogger(__name__)


def change_all_vowels(text: str):
    return text.lower().replace("a", "i").replace("e", "i").replace("o", "i").replace("u", "i").replace("ó", "í").replace("á", "í").replace("é", "í").replace("ú", "í")


def speech_to_text(audio_file: str, language: str):
    if "www." in audio_file or "https://" in audio_file or "http://" in audio_file:
        audio_file, _ = url.urlretrieve(audio_file)
        tmp = tempfile.NamedTemporaryFile(delete=False)

        sound = AudioSegment.from_ogg(audio_file)
        sound.export(tmp.name, format="wav")
        # assign new path of file to audio_path
        audio_file = tmp.name

    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_file)

    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    try:
        str_audio = r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        str_audio = "Sorry, didn't get what you said"
    except sr.RequestError:
        str_audio = "Seems like the author needs to pay to be able to use Speech to Text..."
    logger.debug(f"Got the following str from audio: {str_audio}")
    return str_audio


def text_to_speech(text: str, language: str):
    speech = gTTS(text=text, lang=language, slow=False)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    speech.save(tmp.name)
    logger.info("Converted text to sound")
    sound = AudioSegment.from_mp3(tmp.name)
    sound.export(tmp.name, format="ogg")
    logger.info(f"Exported file to ogg")
    logger.info(f"File location {tmp.name}")
    # return tmp.name
    return str(Path(tmp.name))


def mimimitify(audio_file: str, language: str):
    text = speech_to_text(audio_file, language)
    text_i = change_all_vowels(text)
    file_i = text_to_speech(text_i, language)
    return file_i, text_i
