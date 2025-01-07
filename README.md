# AI Cockpit - Livestream Erkennungssystem

## 📅 Projektbeschreibung
Das AI Cockpit ist ein Livestream-Erkennungssystem, das mithilfe von Computer Vision und Spracherkennung Reiter und Sportler in Echtzeit erkennt. Es integriert …

- **OpenCV** zur Videobildverarbeitung
- **Vosk** zur Spracherkennung
- **Flask** als Web-Framework zur Bereitstellung eines Dashboards

Das Dashboard bietet:
- Livestream-Anzeige
- Hochladen und Verwalten von Startlisten
- Start/Stopp der Erkennung per Knopfdruck
- Anzeige und Download von Ergebnissen

---

## 🛠️ Projektstruktur
```
.
|-- app/
|   |-- __init__.py       # Initialisierung der Flask-App
|   |-- routes.py         # Web-Routen und Endpunkte
|   |-- controllers.py    # Steuerlogik für Upload und Erkennung
|   |-- recognition.py    # Bild- und Audioverarbeitung
|   |-- vosk_model.py     # Vosk-Spracherkennung
|-- templates/
|   |-- login.html        # Login-Seite
|   |-- dashboard.html    # Dashboard zur Steuerung
|-- main.py               # Startpunkt der Flask-App
|-- requirements.txt      # Projektabhängigkeiten
|-- README.md             # Projektbeschreibung
```

---

## 🛠️ Anforderungen
### Systemvoraussetzungen
- Ubuntu Server (z.B. AWS EC2 mit Ubuntu 22.04)
- Python 3.8 oder höher
- 2+ vCPUs und 4+ GB RAM empfohlen
- ffmpeg und Tesseract OCR installiert

---

## 🖥️ Installation
### 1. Systemaktualisierung
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Benötigte Pakete installieren
```bash
sudo apt install python3 python3-pip python3-venv ffmpeg libsm6 libxext6 tesseract-ocr unzip nginx git -y
```

### 3. Projekt herunterladen
```bash
git clone <GITHUB-REPO-URL>
cd <PROJECT-NAME>
```

### 4. Virtuelle Umgebung erstellen und aktivieren
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 6. Vosk-Modell herunterladen
```bash
mkdir vosk-model
cd vosk-model
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
mv vosk-model-en-us-0.22 vosk-model
cd ..
```

---

## 🛀 Flask-Anwendung starten
```bash
python main.py
```
Die Anwendung läuft nun auf Port **80** und kann über die IP-Adresse des Servers erreicht werden.

---

## 🛠️ Dauerhafter Betrieb mit systemd
1. Erstelle eine systemd-Service-Datei:
```bash
sudo nano /etc/systemd/system/ai_cockpit.service
```

2. Füge folgenden Inhalt ein:
```ini
[Unit]
Description=AI Cockpit Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/<PROJECT-NAME>
ExecStart=/home/ubuntu/<PROJECT-NAME>/venv/bin/python3 /home/ubuntu/<PROJECT-NAME>/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Aktiviere und starte den Service:
```bash
sudo systemctl daemon-reload
sudo systemctl start ai_cockpit
sudo systemctl enable ai_cockpit
```

4. Status prüfen:
```bash
sudo systemctl status ai_cockpit
```

---

## 🌐 Zugriff auf das Dashboard
Die Anwendung ist erreichbar unter:
```
http://<server-ip>
```
Falls Port 80 gesperrt ist, aktualisiere die AWS-Sicherheitsgruppen und erlaube **HTTP (Port 80)**.

---

## 👁 Logs anzeigen
```bash
journalctl -u ai_cockpit -f
```

---

## 🚧 Fehlerbehebung
- **Nginx Error:** Stelle sicher, dass keine anderen Anwendungen Port 80 belegen.
- **Vosk-Fehler:** Stelle sicher, dass das Vosk-Modell im Verzeichnis `vosk-model` liegt.
- **Flask-Fehler:** Überprüfe Logs und stelle sicher, dass alle Abhängigkeiten korrekt installiert sind.

Falls weitere Unterstützung benötigt wird, melde dich gerne!
