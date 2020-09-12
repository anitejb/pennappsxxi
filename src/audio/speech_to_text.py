from os import path
import speech_recognition as sr

from config import GOOGLE_CLOUD_SPEECH_CREDENTIALS


def speech_to_text(filename):
    """Filename in the format `gettysburg.wav`"""
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)

    # Process entire audio file
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    transcript = None
    try:
        transcript = r.recognize_google_cloud(
            audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS
        )
    except sr.UnknownValueError:
        return {
            "message": "error",
            "error": "Google Cloud Speech could not understand audio",
        }
    except sr.RequestError as e:
        return {
            "message": "error",
            "error": f"Could not request results from Google Cloud Speech service; {e}",
        }

    return {
        "message": "success",
        "transcript": transcript,
    }
