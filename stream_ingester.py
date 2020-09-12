import subprocess
import glob, os
from datetime import datetime
import time
from src.audio.speech_to_text import speech_to_text
import pyrebase
import signal


config = {
  "apiKey": os.environ['FIREBASE_API_KEY'],
  "databaseURL": os.environ['FIREBASE_DB_URL'],
  "authDomain": "",
  "storageBucket": ""
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def process_chunks():
    for file in glob.glob("*.wav"):
        filename = '/Users/tianyizhang/Downloads/pennappsxxi/' + file
        try:
            result = speech_to_text(filename)
        except ValueError:
            # incomplete chuncks not ready to read for now
            continue

        if result['message'] == 'success':
            print(f'Transcribe successful for {file}. Saving to DB.')
            text = result['transcript']
            timestamp = time.time()
            # data to save
            data = {
                "text": text
            }
            # Pass the user's idToken to the push method
            results = db.child("audio-chunks").child(timestamp).push(data)
        else:
            print(f'Unable to transcribe: {result["error"]}')
        os.remove(filename)
    time.sleep(10)

def remove_chunk_files():
    for file in glob.glob("*.wav"):
        os.remove(file)

if __name__ == "__main__":
    os.setpgrp() # create new process group, become its leader
    try:
        cmd = ["ffmpeg", "-i", "rtmp://34.122.188.26/live/test", "-f", "segment", "-segment_time", "10", "-ar", "22050", "-strftime", "1", "audio_%Y-%m-%d_%H-%M-%S.wav"]
        subprocess.Popen(cmd)
        while True:
            process_chunks()
    finally:
        os.killpg(0, signal.SIGKILL) # kill all processes in my group
        remove_chunk_files()

