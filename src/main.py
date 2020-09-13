from db.db import db
from nlp.dispatcher import Dispatcher


dispatcher = Dispatcher()

def stream_handler(event):
    messages = event['data']

    if "text" in messages:
        print(messages)
        dispatcher.update_result(messages)
        return

    for key in messages:
        message = messages[key]
        print(message)
        dispatcher.update_result(message)

def start_event_stream():
    my_stream = db.child("audio-chunks").stream(stream_handler)
    return my_stream

stream = start_event_stream()

