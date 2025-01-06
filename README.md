# AI Cockpit Stream

AI Cockpit Stream ist eine Flask-basierte Anwendung, die es ermöglicht, Starter aus einem Live-Stream durch Bild- und Sprachanalyse zu identifizieren. Die Software verwendet OpenCV zur Bildverarbeitung, pytesseract zur Texterkennung und Google Speech Recognition für die Spracherkennung.

## Funktionsübersicht

- **Live-Stream Verfolgung**: Analysiert in Echtzeit Videostreams, um Starter anhand von Grafiken und Sprache zu erkennen.
- **Grafikerkennung**: Erkennt automatisch Namen und Kopfnummern von Reitern und Pferden durch Texterkennung.
- **Spracherkennung**: Nutzt Audio aus dem Stream zur Erkennung von Starter-Informationen.
- **Web-Dashboard**: Interaktive Benutzeroberfläche zur Steuerung und Überwachung der Erkennung.
- **API-Steuerung**: Start/Stop der Erkennung über API-Endpunkte.
- **Ergebnisprotokollierung**: Ergebnisse werden gespeichert und können als JSON abgerufen werden.

---

## Voraussetzungen

- **Python 3.8+**
- **ffmpeg** (zur Verarbeitung von Audio- und Videodaten)
- **Tesseract OCR** (für die Texterkennung)
- **PIP-Pakete**:
  - Flask
  - opencv-python-headless
  - pytesseract
  - speechrecognition
  - numpy
  - ffmpeg-python

---

## Installation

### 1. Projekt klonen oder herunterladen

```bash
https://github.com/Herbert-Sch/AI-Cockpit.git
cd ai_cockpit_stream
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Tesseract installieren (falls nicht vorhanden)

- Linux:
```bash
sudo apt update
sudo apt install tesseract-ocr
```
- Windows:
Lade Tesseract von [hier](https://github.com/UB-Mannheim/tesseract/wiki) herunter und installiere es.

---

## Nutzung

### 1. Anwendung starten

```bash
python app/main.py
```

Die Anwendung wird auf `http://localhost:5000` laufen. Rufe im Browser die URL auf, um das Web-Dashboard zu öffnen.

---

## Web-Dashboard

### Funktionen des Dashboards
- **Start und Stop** der Erkennung über Buttons.
- **Anzeige der Startliste** auf der linken Seite.
- **Live-Stream Player** zur Anzeige des Streams.
- **Hervorhebung des aktuellen Starters**.
- **Einstellungen**: Möglichkeit zur Hochladung einer Startliste und Abruf gespeicherter Ergebnisse.

### Starten der Erkennung über die API

```bash
curl -X POST http://localhost:5000/start \
-H "Authorization: Bearer secureapitoken123" \
-H "Content-Type: application/json" \
-d '{"stream_url": "<stream-url>", "startlist": {}}'
```

### Stoppen der Erkennung

```bash
curl -X POST http://localhost:5000/stop -H "Authorization: Bearer secureapitoken123"
```

### Ergebnisse abrufen

```bash
curl http://localhost:5000/results
```

---

## Konfiguration

### API-Token anpassen

In der Datei `app/main.py` kann der API-Token geändert werden:

```python
API_TOKEN = "secureapitoken123"
```

Ändere dies zu einem sicheren Token, um die API abzusichern.

---

## Projektstruktur

```
ai_cockpit_stream/
│
├── app/
│   ├── main.py                # Hauptanwendung
│   ├── templates/
│   │   └── dashboard.html     # Web-Dashboard
│   └── static/                # Statische Dateien (CSS, JS, etc.)
│
├── results/                   # Ergebnis-JSONs
├── requirements.txt           # Python-Abhängigkeiten
└── README.md                  # Diese Datei
```

---

## Fehlersuche

- **Stream verbindet sich nicht?**
  - Prüfe, ob die Stream-URL korrekt ist.
  - Stelle sicher, dass `ffmpeg` installiert ist.
- **Keine Texterkennung?**
  - Stelle sicher, dass Tesseract OCR installiert ist und korrekt konfiguriert wurde.
- **Spracherkennung schlägt fehl?**
  - Überprüfe, ob das Mikrofon aktiviert ist und `speech_recognition` funktioniert.

---

## Autor
Erstellt von: [Dein Name]  
Kontakt: [deine.email@example.com]
