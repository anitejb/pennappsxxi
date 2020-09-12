from db.db import db
from nlp.dispatcher import Dispatcher


dispatcher = Dispatcher()

def stream_handler(event):
    messages = event['data']
    for key in messages:
        message = messages[key]
        # text, timestamp = message['text'], message['timestamp']
        # print(f'{text} : {timestamp}')
        # call NLP to update results
        dispatcher.process_nlp(message)

def start_event_stream():
    my_stream = db.child("audio-chunks").stream(stream_handler)
    return my_stream

stream = start_event_stream()

