from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return {"message": "success"}, 200
