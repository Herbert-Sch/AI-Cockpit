
# AI Cockpit Stream

Dieses Projekt erkennt Starter aus einem Live-Stream durch Bild- und Sprachanalyse.

## Voraussetzungen
- Python 3.8+
- ffmpeg
- OpenCV
- pytesseract
- Flask
- speech_recognition
- numpy

## Installation
1. Klonen oder laden Sie das Projekt herunter.
2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
3. Starten Sie die Anwendung:
   ```bash
   python app/main.py
   ```

## Nutzung
- Starten Sie die Erkennung per API:
   ```bash
   curl -X POST http://localhost:5000/start -H "Authorization: Bearer secureapitoken123" -d '{"stream_url":"<stream>","startlist":{}}'
   ```
- Stoppen Sie die Erkennung:
   ```bash
   curl -X POST http://localhost:5000/stop -H "Authorization: Bearer secureapitoken123"
   ```
- Ergebnisse abrufen:
   ```bash
   curl http://localhost:5000/results
   ```
