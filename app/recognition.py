import cv2
import pytesseract
from vosk import Model, KaldiRecognizer
import ffmpeg
import os
import numpy as np
import datetime
import time
import logging
import json
import queue
import threading
from flask import request
from collections import defaultdict

results = []
error_message = None
STARTLIST = {}
STREAM_URL = ""
clipmyhorse_event_id = None
class_no = None


# Validierung der Streaming-URL
if not STREAM_URL:
    error_message = "Streaming URL not set."
    exit(1)


MODEL_DIR = "vosk-model"
if not os.path.exists(MODEL_DIR):
    error_message = "Vosk model not found."
    exit(1)

model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, 16000)


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



# Audio-Queue für parallele Spracherkennung
audio_queue = queue.Queue()
recognized_starters = {}
start_time = None
recognized_headnumbers = set()  # Set zur Verhinderung doppelter Erkennungen



def load_startlist():
    global STARTLIST
    try:
        if 'startlist' in request.files:
            file = request.files['startlist']
            STARTLIST = json.load(file)
        else:
            error_message = "No startlist provided."
    except Exception as e:
        error_message = f"Failed to load startlist: {str(e)}"



def extract_audio(stream_url):
    try:
        process = (
            ffmpeg.input(stream_url)
            .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )
        return process
    except Exception as e:
        global error_message
        error_message = f"Failed to extract audio: {str(e)}"
        return None



def match_entry(text):
    for entry in STARTLIST.get("startlist", {}).get("entries", []):
        if entry['ridername'].lower() in text.lower() or entry['sport_name'].lower() in text.lower() or entry['headnr'] in text:
            elapsed_time = int(time.time() - start_time)
            if entry['headnr'] not in recognized_starters:
                recognized_starters[entry['headnr']] = entry
                recognized_starters[entry['headnr']]['live_chapter'] = []
            recognized_starters[entry['headnr']]['live_chapter'].append({"second": elapsed_time})
            print(f"Matched Entry: {entry['ridername']} - {entry['sport_name']}")



def preprocess_frame(frame):
    # Konvertierung in Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Bild entrauschen (Gaussian Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Anwendung von adaptivem Thresholding
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
    
    # Bildvergrößerung für bessere Texterkennung
    scaled = cv2.resize(threshold, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Schärfen des Bildes
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(scaled, -1, kernel)
    
    # Morphologische Operation zur Rauschreduzierung
    kernel_morph = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(sharpened, cv2.MORPH_CLOSE, kernel_morph)
    
    # Kantenanhebung mit Canny Edge Detection
    edges = cv2.Canny(morph, 100, 200)
    
    return edges



def match_entry(text):
    for entry in STARTLIST.get("entries", []):
        if entry['ridername'].lower() in text.lower() or entry['sport_name'].lower() in text.lower() or entry['headnr'] in text:
            if entry['headnr'] not in recognized_headnumbers:
                elapsed_time = int(time.time() - start_time)
                recognized_headnumbers.add(entry['headnr'])

                if entry['headnr'] not in recognized_starters:
                    recognized_starters[entry['headnr']] = entry
                    recognized_starters[entry['headnr']]['live_chapter'] = []
                
                # Füge den gleichen Zeitstempel zweimal hinzu
                recognized_starters[entry['headnr']]['live_chapter'].append({"second": elapsed_time})
                recognized_starters[entry['headnr']]['live_chapter'].append({"second": elapsed_time})
                
                print(f"Matched Entry: {entry['ridername']} - {entry['sport_name']} mit Zeit: {elapsed_time} Sekunden")



def process_stream(stream_url):
    global error_message, start_time
    load_startlist()
    start_time = time.time()

    video_stream = cv2.VideoCapture(stream_url)
    if not video_stream.isOpened():
        error_message = "Unable to open video stream"
        return

    audio_process = extract_audio(stream_url)
    if not audio_process:
        error_message = "Audio extraction failed"
        return

    audio_thread = threading.Thread(target=process_audio, args=(audio_process,))
    audio_thread.start()

    frame_interval = 2  # Sekunden zwischen den Frames
    last_capture_time = time.time()

    while not stop_event.is_set():
        ret, frame = video_stream.read()
        if not ret:
            break
        
        current_time = time.time()
        if current_time - last_capture_time >= frame_interval:
            processed_frame = preprocess_frame(frame)
            text = pytesseract.image_to_string(processed_frame)

            if text.strip():  # Wenn Text erkannt wurde
                print("Text Recognition (preferred):", text)
                match_entry(text)
            else:
                print("Text Recognition failed, falling back to Speech Recognition.")

            last_capture_time = current_time

    video_stream.release()
    audio_process.stdout.close()
    audio_thread.join()
    save_results()
    print("Processing complete")



def process_audio(process):
    while not stop_event.is_set():
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("Speech Recognition (fallback):", result['text'])
            match_entry(result['text'])



def save_results():
    try:
        now = datetime.datetime.now()
        year = now.strftime('%Y')
        week = now.strftime('%W')
        directory = f"results/{year}/{week}/{clipmyhorse_event_id}"
        os.makedirs(directory, exist_ok=True)
        filepath = f"{directory}/{clipmyhorse_event_id}-{class_no}.json"

        # Umwandlung der erkannten Starter in das gewünschte Ausgabeformat
        output = []
        for starter in recognized_starters.values():
            entry = {
                "sport_name": starter.get("sport_name"),
                "breed_name": starter.get("breed_name"),
                "horse_iso": starter.get("horse_iso"),
                "year_of_birth": starter.get("year_of_birth"),
                "color_en": starter.get("color_en"),
                "gender_en": starter.get("gender_en"),
                "breeder": starter.get("breeder"),
                "fei": starter.get("fei"),
                "name_father": starter.get("name_father"),
                "iso_father": starter.get("iso_father"),
                "name_mother": starter.get("name_mother"),
                "iso_mother": starter.get("iso_mother"),
                "ridername": starter.get("ridername"),
                "team": starter.get("team"),
                "start_time": starter.get("start_time", ""),
                "startnr": starter.get("startnr"),
                "headnr": starter.get("headnr"),
                "live_chapter": starter.get("live_chapter", [])
            }
            output.append(entry)

        with open(filepath, 'w') as file:
            json.dump(output, file, indent=4)
        print(f"Results saved to {filepath}")
    except Exception as e:
        print(f"Failed to save results: {str(e)}")