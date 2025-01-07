from flask import request, jsonify, render_template, redirect, url_for, session
from app import app
from app.controllers import upload_startlist, start_recognition, stop_recognition
from app.recognition import results, error_message
from flask import send_file

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', results=results, error_message=error_message)

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/start', methods=['POST'])
def start():
    return start_recognition()

@app.route('/stop', methods=['POST'])
def stop():
    return stop_recognition()

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(results)

@app.route('/errors', methods=['GET'])
def get_errors():
    return jsonify({"error_message": error_message})
    
@app.route('/video_feed')
def video_feed():
    def generate_frames():
        camera = cv2.VideoCapture(STREAM_URL)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/download_latest', methods=['GET'])
def download_latest():
    try:
        base_dir = "results"
        latest_file = None
        latest_time = 0

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    file_time = os.path.getmtime(filepath)
                    if file_time > latest_time:
                        latest_time = file_time
                        latest_file = filepath

        if latest_file:
            return send_file(latest_file, as_attachment=True)
        else:
            return jsonify({"error": "No result files found"}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to download file: {str(e)}"}), 500