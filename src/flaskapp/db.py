import os
import pyrebase

firebase_config = {
  "apiKey": os.getenv(FIREBASE_API_KEY),
  "authDomain": f"{os.getenv(FIREBASE_PROJECT_ID)}.firebaseapp.com",
  "databaseURL": f"https://{os.getenv(FIREBASE_PROJECT_ID)}.firebaseio.com",
  "storageBucket": f"{os.getenv(FIREBASE_PROJECT_ID)}.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

def push_to_audio_chunks(value):
    db.child("audio-chunks").child(time.time()).push(value)

def push_to_results(value):
    db.child("results").child(time.time()).push(value)
