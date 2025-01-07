from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, session
import cv2
import pytesseract
import speech_recognition as sr
import threading
import ffmpeg
import json
import os
import datetime
import time
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'

results = []
current_starter = None
start_time = None
stop_event = threading.Event()
API_TOKEN = "secureapitoken123"
STREAM_URL = ""
STARTLIST = {}

class StopController:
    def __init__(self):
        self._stop = False

    def set(self):
        self._stop = True

    def clear(self):
        self._stop = False

    def is_set(self):
        return self._stop

stop_event = StopController()

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'Admin' and request.form['password'] == 'Horsemyclip25':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', results=results)


@app.route('/upload', methods=['POST'])
def upload_startlist():
    global STARTLIST, STREAM_URL
    if 'startlist' in request.files and 'stream_url' in request.form:
        file = request.files['startlist']
        STARTLIST = json.load(file)
        STREAM_URL = request.form['stream_url']
        return jsonify({"message": "Startlist and URL updated"})
    return jsonify({"error": "Invalid input"})


@app.route('/start', methods=['POST'])
def start_recognition():
    threading.Thread(target=process_stream, args=(STREAM_URL, STARTLIST)).start()
    return jsonify({"message": "Recognition started"})


@app.route('/stop', methods=['POST'])
def stop_recognition():
    stop_event.set()
    return jsonify({"message": "Recognition stopped"})


def process_stream(stream_url, startlist):
    global current_starter, start_time, results
    stop_event.clear()
    video_stream = cv2.VideoCapture(stream_url)
    recognizer = sr.Recognizer()
    
    while not stop_event.is_set():
        ret, frame = video_stream.read()
        if not ret:
            continue

        recognized_text = recognize_text_from_frame(frame)
        current_starter = match_with_startlist(recognized_text, startlist)
        if current_starter:
            start_time = datetime.datetime.now().timestamp()
            save_result(current_starter, start_time)

    video_stream.release()


def recognize_text_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)


def match_with_startlist(text, startlist):
    for entry in startlist['startlist']['entries']:
        if entry['sport_name'].lower() in text.lower():
            return entry
    return None


def save_result(entry, start_time):
    entry['start_time'] = start_time
    results.append(entry)
    with open(f"{RESULTS_DIR}/{entry['sport_name'].replace(' ', '_')}.json", 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
