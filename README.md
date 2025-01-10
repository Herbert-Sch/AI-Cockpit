# AI Cockpit

AI Cockpit ist ein KI-gestütztes Dashboard zur Analyse von Videostreams und Startlisten. Die Anwendung kombiniert Text-Extraktion, Videoverarbeitung und eine Benutzeroberfläche, um Daten aus Livestreams effizient zu verarbeiten.

## Funktionen

### 1. **Live-Streaming-Integration**
- Unterstützt Livestreams über HLS-URLs.
- Benutzer können die Streaming-URL konfigurieren und speichern.

### 2. **Startlisten-Verwaltung**
- Upload von Startlisten im JSON-Format.
- Validierung der Startlistenstruktur vor der Speicherung.

### 3. **Text-Extraktion aus Videos**
- Extrahiert relevante Informationen wie Kopfnummer, Pferdenamen und Reiternamen aus Videoframes.
- Speichert die extrahierten Daten in einer JSON-Datei (`videototext.json`).

### 4. **Cockpit-Export**
- Generiert eine JSON-Ausgabedatei (`cockpitexport.json`) basierend auf der extrahierten Videotext- und Startlisten-Daten.
- Ermöglicht den Download des Exports über die Benutzeroberfläche.

### 5. **Steuerung der Analyse**
- Start- und Stopp-Funktionen für die Videotextanalyse direkt über das Dashboard.

---

## Installationsanleitung

### Voraussetzungen
- Docker installiert
- Python 3.9 (innerhalb des Docker-Images genutzt)

### Schritte zur Installation
1. Klone das Repository:
   ```bash
   git clone https://github.com/Herbert-Sch/AI-Cockpit.git
   cd AI-Cockpit
   ```

2. Erstelle das Docker-Image:
   ```bash
   docker build -t ai_cockpit_image .
   ```

3. Starte den Docker-Container:
   ```bash
   docker run -d --name ai_cockpit_container -p 5000:5000 ai_cockpit_image
   ```

4. Öffne die Anwendung im Browser:
   - `http://<server-ip>:5000`

---

## Nutzung

### 1. **Starten der Anwendung**
- Besuche die URL deines Servers, z. B. `http://localhost:5000`.

### 2. **Stream-Konfiguration**
- Gib die URL des Livestreams ein und speichere die Konfiguration.

### 3. **Startliste hochladen**
- Lade eine JSON-Startliste hoch. Beispiel für die Struktur:

```json
{
  "clipmyhorse_event_id": 15529,
  "class_no": 3,
  "platform": "WEC",
  "startlist": {
    "class_name": "Class 3 - 1.20 m Special Two Phases",
    "start_time": "2025-01-05T13:20:00+01:00",
    "entries": [
      {
        "sport_name": "Indra 147",
        "ridername": "Sven Sieger",
        "startnr": 1,
        "headnr": "229"
      }
    ]
  }
}
```

### 4. **Textanalyse starten**
- Drücke den "Start AI"-Button, um die Analyse zu starten.
- Ergebnisse werden in der Datei `videototext.json` gespeichert.

### 5. **Cockpit-Export herunterladen**
- Lade den Cockpit-Export mit einem Klick auf "Download Cockpit Export" herunter.

---

## Technische Details

### Projektstruktur
- **`dashboard.py`**: Hauptanwendung für das Dashboard.
- **`videoanalysis.py`**: Führt die Videotextanalyse durch.
- **`startlistverification.py`**: Verifiziert Startlisten und generiert den Cockpit-Export.
- **`index.html`**: Benutzeroberfläche.
- **Konfigurationsdateien**: `streamingconf.json`, `startlist.json`, `videototext.json`.

### Abhängigkeiten
- Flask
- OpenCV
- pytesseract

Die Abhängigkeiten sind in `requirements.txt` definiert.

---

## Empfehlung für AWS-Server

Um diese Anwendung auf AWS zu hosten, wird ein **t2.medium** oder **t3.medium** EC2-Instance empfohlen. Diese Instanzen bieten ausreichend CPU-Leistung und RAM für die Docker-Container und die Verarbeitung von Livestreams.

### Schritte zur Einrichtung:
1. **Erstelle eine EC2-Instanz:**
   - Wähle das Amazon Machine Image (AMI) `Ubuntu 20.04 LTS`.
   - Wähle den Instanztyp `t3.medium` (2 vCPUs, 4 GB RAM).

2. **Installiere Docker:**
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Kopiere das Projekt auf den Server:**
   Nutze `scp` oder ein Git-Repository, um die Dateien zu übertragen.

4. **Führe die Installation aus:**
   ```bash
   bash install_ai_cockpit.sh
   ```

5. **Öffne den Port 5000:**
   Stelle sicher, dass in der AWS-Sicherheitsgruppe der Port 5000 für eingehenden Datenverkehr geöffnet ist.

6. **Zugriff:**
   Besuche `http://<ec2-public-ip>:5000`, um auf die Anwendung zuzugreifen.

---

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` für weitere Informationen.
