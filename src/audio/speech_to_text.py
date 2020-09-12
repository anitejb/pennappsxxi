from os import path
from google.cloud import speech

def speech_to_text(filename):
    client = speech.SpeechClient()

    # path = "filename.wav", must be in current directory
    # filepath = path.join(path.dirname(path.realpath(__file__)), filename)
    filepath = filename
    with open(filepath, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript.strip() + " "
    return {"message": "success", "transcript": transcript}
