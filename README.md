# AI Cockpit Stream - README

## Projektbeschreibung
AI Cockpit Stream ist eine Flask-basierte Webanwendung, die es ermöglicht, Starter aus einem Live-Stream durch Bild- und Sprachanalyse zu identifizieren. 

**Hauptfunktionen:**
- Live-Stream-Überwachung
- Grafikerkennung mittels OpenCV und pytesseract
- Spracherkennung mit Google Speech Recognition
- Web-Dashboard zur Verwaltung der Erkennung
- API zur Steuerung der Start- und Stop-Erkennung
- Upload der Startliste und Eingabe der Streaming-URL
- Benutzer-Login zur Absicherung

---

## Systemanforderungen
### Mindestanforderungen
- **Betriebssystem:** Ubuntu 20.04 oder höher
- **RAM:** 2 GB
- **CPU:** 2 vCPUs
- **Speicherplatz:** 10 GB freier Speicherplatz
- **Netzwerk:** Stabiler Internetzugang für Streamverarbeitung

### Empfohlene Anforderungen
- **RAM:** 4 GB oder mehr
- **CPU:** 4 vCPUs
- **GPU:** Für verbesserte Texterkennung (optional, CUDA-Unterstützung)
- **Speicherplatz:** 20 GB oder mehr

---

## Installationsanleitung für AWS EC2 (Ubuntu)

### 1. AWS EC2-Instanz erstellen
1. Melde dich bei der [AWS-Managementkonsole](https://aws.amazon.com/de/) an.
2. Navigiere zu **EC2** und klicke auf **Instanz starten**.
3. Wähle als Amazon Machine Image (AMI) **Ubuntu Server 20.04 LTS**.
4. Wähle den Instanztyp (mindestens **t2.medium** für 2 vCPUs und 4 GB RAM).
5. Konfiguriere Sicherheitsgruppen:
    - Port **22** für SSH-Zugriff
    - Port **80** für den Flask-Webserver
6. Erstelle oder wähle ein vorhandenes Schlüsselpaar für SSH-Zugriff.
7. Starte die Instanz.

---

### 2. Verbindung zur EC2-Instanz

```bash
ssh -i <dein-key.pem> ubuntu@<EC2-IP-Adresse>
