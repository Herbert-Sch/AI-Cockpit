from flask import request, jsonify
import json
import threading
import time
from app.recognition import process_stream, STARTLIST, STREAM_URL, clipmyhorse_event_id, class_no, error_message, stop_event

def upload_startlist():
    global STARTLIST, STREAM_URL, clipmyhorse_event_id, class_no, error_message
    try:
        if 'startlist' in request.files and 'stream_url' in request.form:
            file = request.files['startlist']
            STARTLIST = json.load(file)
            STREAM_URL = request.form['stream_url']
            clipmyhorse_event_id = STARTLIST.get('clipmyhorse_event_id', 'unknown_event')
            class_no = STARTLIST.get('class_no', 'unknown_class')
            error_message = None
            return jsonify({"message": "Startlist, URL, and event information updated"})
    except Exception as e:
        error_message = f"Failed to upload startlist: {str(e)}"
    return jsonify({"error": "Invalid input"})

def start_recognition():
    global error_message
    try:
        threading.Thread(target=process_stream, args=(STREAM_URL, STARTLIST)).start()
        error_message = None
        return jsonify({"message": "Recognition started successfully"})
    except Exception as e:
        error_message = f"Failed to start recognition: {str(e)}"
        return jsonify({"error": error_message}), 500

def stop_recognition():
    global error_message
    stop_event.set()
    try:
        return jsonify({"message": "Recognition stopped and results saved"})
    except Exception as e:
        error_message = f"Failed to stop recognition: {str(e)}"
        return jsonify({"error": error_message}), 500