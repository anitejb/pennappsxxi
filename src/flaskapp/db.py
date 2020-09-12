import pyrebase

firebase_config = {
  "apiKey": os.getenv(FIREBASE_API_KEY),
  "authDomain": f"{os.getenv(FIREBASE_PROJECT_ID)}.firebaseapp.com",
  "databaseURL": f"https://{os.getenv(FIREBASE_PROJECT_ID)}.firebaseio.com",
  "storageBucket": f"{os.getenv(FIREBASE_PROJECT_ID)}.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

def get_all_texts():
    users = db.child("users").get().val()
    for user in users:
        print(user, users[user])
    return {"texts" : users}
