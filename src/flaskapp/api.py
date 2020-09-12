from flask import Flask, request

import sys
sys.path.insert(1,'../wolfram/')
from wolfram import wolframURL

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return {"message": "success"}, 200

@app.route('/uploads/url')
def wolframInput():    
    
    return wolframURL("5x5")
