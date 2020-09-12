import subprocess
import glob, os
from datetime import datetime
import time
from src.audio.speech_to_text import speech_to_text
import pyrebase

# subprocess.Popen(["ffmpeg", "-i", "rtmp://34.122.188.26/live/test", "-f", "segment", "-segment_time", "10", "-c", "copy", "test%d.wav"])
# ffmpeg -i rtmp://34.122.188.26/live/test -f segment -segment_time 10 -ar 22050 -strftime 1 audio_%Y-%m-%d_%H-%M-%S.wav

config = {
}
firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()

while True:
    for file in glob.glob("*.wav"):
        result = speech_to_text(file)
        print(result)
        if result['message'] == 'success':
            text = result['transcript']
            timestamp = datetime.now()
            # data to save
            data = {
                "timestamp": str(timestamp),
                "text": text
            }
            # Pass the user's idToken to the push method
            results = db.child("audio-chunks").push(data)
        os.remove(filename)
    time.sleep(10)


