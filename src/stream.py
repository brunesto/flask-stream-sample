from flask import Flask, stream_template, request, Response
import os
import time


def send_messages(messages):
    # spits one character at a time
    for c in "A quick brown fox jumps over the lazy dog.":
        time.sleep(0.2)
        yield c


app = Flask(__name__)


@app.route("/")
def index():
    return stream_template("./stream.html")


@app.route("/stream", methods=["GET", "POST"])
def stream():
    if request.method == "POST":
        messages = request.json["messages"]

        def event_stream():
            for chunk in send_messages(messages=messages):
                print(chunk)
                yield chunk

        response = Response(event_stream(), mimetype="text/event-stream")
        response.headers["X-Accel-Buffering"] = "no"
        return response
