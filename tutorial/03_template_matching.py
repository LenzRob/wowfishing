import cv2
import numpy as np
import mss

import pyautogui
x_screen_size, y_screen_size = pyautogui.size()

# Aufnahmebereich definieren
bounding_box = {
    'top': int(y_screen_size * 0.2),
    'left': int(x_screen_size * 0.4),
    'width': int(x_screen_size * 0.2),
    'height': int(y_screen_size * 0.4)
}

# images\target2.png

# Lade das Musterbild (Template)
template = cv2.imread("images/target9.png", cv2.IMREAD_UNCHANGED)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # Graustufen für besseres Matching
w, h = template_gray.shape[::-1]  # Breite und Höhe des Templates

with mss.mss() as sct:
    while True:
        # Screenshot des gewählten Bereichs machen
        screenshot = sct.grab(bounding_box)

        # Konvertiere das Bild in ein numpy-Array (BGR-Farbraum für OpenCV)
        frame = np.array(screenshot)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)  # In Graustufen konvertieren

        # Template Matching durchführen
        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Schwellenwert für Erkennung setzen (je nach Test evtl. anpassen)
        threshold = 0.7  # 0.7 bis 0.9 ist meist ein guter Wert

        if max_val >= threshold:
            top_left = max_loc  # Position des besten Matches
            bottom_right = (top_left[0] + w, top_left[1] + h)

            # Zeichne ein Rechteck um das erkannte Muster
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            # Position des gefundenen Musters ausgeben
            print(f"Fishing Target gefunden bei: {top_left}")

        # Zeige das Live-Bild mit Markierung an
        cv2.imshow("Pattern Matching", frame)

        # Breche mit "q" die Aufnahme ab
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Fenster schließen
cv2.destroyAllWindows()