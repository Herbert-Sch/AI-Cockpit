# Videoanalysis

Ein Python-basiertes Tool zur Texterkennung in Livestreams.

## Voraussetzungen
1. Python 3.8 oder höher
2. Tesseract OCR installiert
3. FFMPEG zur Unterstützung von Video-Streams

## Installation
1. Repository klonen:
   ```bash
   git clone https://github.com/Herbert-Sch/videoanalysis.git
   cd videoanalysis
   ```

2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. Tesseract installieren (Linux):
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

4. Konfigurationsdateien bearbeiten:
   - Bearbeite `streamingconf.json` mit deiner Livestream-URL.
   - Passe die Pixelbereiche in `videopix.json` an deine Stream-Auflösung an.

## Ausführung
Starten des Programms:
```bash
python3 videoanalysis.py
```

Beenden des Programms:
1. Erstelle eine Datei `stop.json` im Projektverzeichnis:
   ```bash
   touch stop.json
   ```
2. Das Programm beendet sich sicher und speichert die Ergebnisse in `videototext.json`.

## Hinweise
- Verwenden Sie virtuelle Umgebungen (venv), um Abhängigkeiten zu isolieren.
- Nutzen Sie `screen` oder `tmux`, um das Programm im Hintergrund laufen zu lassen.

## Erweiterungen
- Hinzufügen neuer Textbereiche: Bearbeiten Sie die Datei `videopix.json` und passen Sie das Programm entsprechend an.
- Anpassungen für spezifische Livestreams und Texterkennungsbedürfnisse können über Tesseract-Konfigurationen erfolgen.
