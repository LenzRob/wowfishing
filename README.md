# Fishing Bot
**Beschreibung:**

Dieser Bot verwendet Computer Vision und Automatisierungsbibliotheken, um auf dem Bildschirm nach bestimmten Mustern zu suchen und darauf zu reagieren. Nutzung erfolgt auf eigene Gefahr und die Erstellung diente nur zu Forschungszwecken.

**Funktionalität:**

- Bildschirmaufnahme: Erfasst einen definierten Bereich des Bildschirms.
- Template Matching: Vergleicht das aufgenommene Bild mit einem vorgegebenen Muster.
- Automatisierte Aktionen: Bewegt die Maus zum gefundenen Muster und führt Klick- und Tastatureingaben aus.

**Nutzung:**

1. Stelle sicher, dass alle erforderlichen Bibliotheken installiert sind:

``pip install numpy opencv-python mss pyautogui pygame_widgets``

2. Platziere das Musterbild (target15.png) im images Ordner.

3. Starte das Programm:

`python main.py`

4. Drücke `q`, um das Programm zu beenden.
