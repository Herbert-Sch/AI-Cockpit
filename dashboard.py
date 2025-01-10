from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import subprocess

app = Flask(__name__)

# Set the paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_ANALYSIS_DIR = BASE_DIR
STREAMING_CONF_PATH = os.path.join(BASE_DIR, 'streamingconf.json')
STARTLIST_PATH = os.path.join(BASE_DIR, 'startlist.json')
START_PATH = os.path.join(BASE_DIR, 'start.json')
STOP_PATH = os.path.join(BASE_DIR, 'stop.json')
COCKPIT_EXPORT = os.path.join(BASE_DIR, 'cockpitexport.json')
VIDEOTOTEXT_PATH = os.path.join(BASE_DIR, 'videototext.json')

video_analysis_process = None

def write_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def validate_startlist(data):
    """Validate the structure of the startlist JSON."""
    required_keys = ["clipmyhorse_event_id", "class_no", "startlist", "platform"]
    startlist_required_keys = ["class_name", "start_time", "entries"]
    entry_required_keys = [
        "sport_name", "breed_name", "horse_iso", "year_of_birth", "color_en",
        "gender_en", "breeder", "fei", "name_father", "iso_father",
        "name_mother", "iso_mother", "ridername", "team",
        "start_time", "startnr", "headnr"
    ]
    
    # Check top-level keys
    for key in required_keys:
        if key not in data:
            return False, f"Missing top-level key: {key}"

    # Check startlist keys
    startlist_data = data.get("startlist", {})
    for key in startlist_required_keys:
        if key not in startlist_data:
            return False, f"Missing key in startlist: {key}"
    
    # Check entries
    entries = startlist_data.get("entries", [])
    if not isinstance(entries, list):
        return False, "Entries must be a list."
    
    for entry in entries:
        for key in entry_required_keys:
            if key not in entry:
                return False, f"Missing key in entry: {key}"

    return True, "Valid"

@app.route('/')
def index():
    stream_url = None
    if os.path.exists(STREAMING_CONF_PATH):
        with open(STREAMING_CONF_PATH, 'r') as f:
            stream_url = json.load(f).get("stream_url")
    return render_template('index.html', stream_url=stream_url)

@app.route('/configure_stream', methods=['POST'])
def configure_stream():
    stream_url = request.form.get('stream_url')
    if not stream_url:
        return jsonify({"error": "No stream URL provided"}), 400

    conf_data = {"stream_url": stream_url}
    write_json_file(STREAMING_CONF_PATH, conf_data)
    return jsonify({"message": "Streaming configuration saved."}), 200

@app.route('/upload_startlist', methods=['POST'])
def upload_startlist():
    file = request.files.get('startlist')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        startlist_data = json.load(file)
        valid, message = validate_startlist(startlist_data)
        if not valid:
            return jsonify({"error": message}), 400

        write_json_file(STARTLIST_PATH, startlist_data)
        return jsonify({"message": "Startlist uploaded successfully."}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format."}), 400

@app.route('/start', methods=['POST'])
def start_stream():
    global video_analysis_process

    if not os.path.exists(STREAMING_CONF_PATH) or not os.path.exists(STARTLIST_PATH):
        return jsonify({"error": "Required files are missing."}), 400

    start_data = {"status": "started"}
    write_json_file(START_PATH, start_data)

    if video_analysis_process is None:
        video_analysis_process = subprocess.Popen(['python', 'videoanalysis.py'])

    return jsonify({"message": "Stream started."}), 200

@app.route('/stop', methods=['POST'])
def stop_stream():
    global video_analysis_process

    if not os.path.exists(START_PATH):
        return jsonify({"error": "Stream not started."}), 400

    stop_data = {"status": "stopped"}
    write_json_file(STOP_PATH, stop_data)

    if video_analysis_process is not None:
        video_analysis_process.terminate()
        video_analysis_process = None

    delete_file(START_PATH)
    delete_file(STOP_PATH)

    return jsonify({"message": "Stream stopped and files deleted."}), 200

@app.route('/download_cockpit', methods=['GET'])
def download_cockpit():
    # Path to the cockpit export script
    cockpit_script_path = os.path.join(BASE_DIR, 'startlistverification.py')

    try:
        # Execute the script to generate cockpitexport.json
        subprocess.run([
            'python', cockpit_script_path, 
            '--videototext', VIDEOTOTEXT_PATH, 
            '--startlist', STARTLIST_PATH, 
            '--output', COCKPIT_EXPORT
        ], check=True)

        # Check if the cockpitexport.json file was created
        if not os.path.exists(COCKPIT_EXPORT):
            return jsonify({"error": "Cockpit export generation failed."}), 500

        # Send the generated file to the user
        return send_file(COCKPIT_EXPORT, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to execute the export script: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)