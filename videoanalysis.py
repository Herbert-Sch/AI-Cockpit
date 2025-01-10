import cv2
import pytesseract
import json
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STREAM_CONFIG = os.path.join(BASE_DIR, 'streamingconf.json')
STARTLIST_PATH = os.path.join(BASE_DIR, 'startlist.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'videototext.json')
START_FILE = os.path.join(BASE_DIR, 'start.json')
STOP_FILE = os.path.join(BASE_DIR, 'stop.json')

def load_stream_config():
    try:
        with open(STREAM_CONFIG, 'r') as file:
            config = json.load(file)
        return config['stream_url']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error: Unable to load streaming configuration.")
        exit(1)

def load_startlist():
    try:
        with open(STARTLIST_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Unable to load startlist.json.")
        exit(1)

def initialize_results_file():
    with open(OUTPUT_FILE, 'w') as file:
        json.dump([], file, indent=4)

def scale_coordinates(areas, frame_width, frame_height):
    scaled_areas = {}
    for key, area in areas.items():
        x_rel, y_rel, w_rel, h_rel = area
        x = int(x_rel * frame_width)
        y = int(y_rel * frame_height)
        w = int(w_rel * frame_width)
        h = int(h_rel * frame_height)
        scaled_areas[key] = (x, y, w, h)
    return scaled_areas

def extract_text_from_frame(frame, areas):
    extracted_data = {}
    for key, area in areas.items():
        x, y, w, h = area
        cropped = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cropped, config='--psm 6 --oem 3')
        extracted_data[key] = text.strip()
    return extracted_data

def save_results(data):
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def process_hls_stream(url, areas, startlist_entries):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Error: Unable to open the HLS stream. Check the URL and accessibility.")
        exit(1)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scaled_areas = scale_coordinates(areas, frame_width, frame_height)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    interval = int(frame_rate * 3)  # Process every 3 seconds
    frame_count = 0
    start_time = time.time()
    results = []

    for entry in startlist_entries:
        rider_name = entry["ridername"]
        sport_name = entry["sport_name"]

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame. Check the HLS source.")
                break

            if frame_count % interval == 0:
                extracted_text = extract_text_from_frame(frame, scaled_areas)
                timestamp = int(time.time() - start_time)
                extracted_text['timestamp'] = timestamp
                extracted_text['ridername'] = rider_name
                extracted_text['sport_name'] = sport_name
                results.append(extracted_text)
                save_results(results)
                print(f"{timestamp}s - {extracted_text}")

            frame_count += 1

            if os.path.exists(STOP_FILE):
                print("Stop file found. Exiting.")
                break

    cap.release()
    save_results(results)

def wait_for_start_file():
    print("Waiting for start.json...")
    while not os.path.exists(START_FILE):
        time.sleep(1)

def main():
    while True:
        wait_for_start_file()
        print("Start file detected. Starting text recognition...")
        initialize_results_file()

        startlist = load_startlist()
        platform = startlist.get("platform", "WEC")
        startlist_entries = startlist.get("startlist", {}).get("entries", [])
        print(f"Loaded {len(startlist_entries)} entries from the startlist.")

        stream_url = load_stream_config()
        # Define areas for text recognition; replace with real configuration
        areas = {"area1": (0.1, 0.1, 0.2, 0.2)}  # Example area config
        process_hls_stream(stream_url, areas, startlist_entries)

        if os.path.exists(START_FILE):
            os.remove(START_FILE)

if __name__ == "__main__":
    main()