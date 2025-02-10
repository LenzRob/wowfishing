import cv2
import numpy as np
import mss
import pyautogui
import threading
import time
# import random

x_screen_size, y_screen_size = pyautogui.size()

# Aufnahmebereich definieren
bounding_box = {
    'top': int(y_screen_size * 0.2),
    'left': int(x_screen_size * 0.4),
    'width': int(x_screen_size * 0.2),
    'height': int(y_screen_size * 0.3)
}

# Lade das Musterbild (Template)
template = cv2.imread("images/target15.png", cv2.IMREAD_UNCHANGED)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = template_gray.shape[::-1]

frame = None  # Gemeinsame Variable für das aktuelle Bild
lock = threading.Lock()  # Lock, um race conditions zu vermeiden
running = True  # Flag zum Beenden der Threads
match_found_event = threading.Event()  # Signalisiert, ob ein Match gefunden wurde


def capture_screen():
    """Erfasst den Bildschirmbereich und speichert ihn in 'frame'."""
    global frame, running
    with mss.mss() as sct:
        while running:
            screenshot = sct.grab(bounding_box)
            img = np.array(screenshot)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

            with lock:
                frame = img_gray.copy()  # Bild in die globale Variable speichern


def process_image():
    """Verarbeitet das Bild und führt Template Matching aus."""
    global frame, running, mouse_position
    while running:
        if frame is None:
            continue  # Warte auf das erste Bild

        with lock:
            img_gray = frame.copy()  # Kopie des aktuellen Frames holen

        # Template Matching durchführen
        result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.7
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            # Zeichne das Rechteck
            img_color = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
            cv2.rectangle(img_color, top_left, bottom_right, (0, 255, 0), 2)

            print(f"Fishing Target gefunden bei: {top_left}")

            # Speichert die Mausposition für den Mouse-Thread
            with lock:
                mouse_position = (
                    bounding_box["left"] + top_left[0] + w // 2,
                    bounding_box["top"] + top_left[1] + h // 2
                )

            match_found_event.set()  # Maus-Thread benachrichtigen

        cv2.imshow("Pattern Matching", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

def mouse_action():
    # Bewege Maus zum Match
    global mouse_position, last_fish_time
    while running:
        match_found_event.wait()  # Warten bis ein Match gefunden wurde
        match_found_event.clear()  # Reset des Events

        with lock:
            if mouse_position is None:
                continue

            mouse_x, mouse_y = mouse_position  # Maus-Koordinaten übernehmen

        print(f"Bewege Maus zu {mouse_x}, {mouse_y} und klicke")
        pyautogui.moveTo(mouse_x, mouse_y, duration=0.5)
        pyautogui.click(button='right', duration=0.1)

        print("Drücke Taste '0'")
        pyautogui.press("0")

        last_fish_time = time.time()  # Timer für die erneute Prüfung zurücksetzen

        # Nicht-blockierendes Warten für max. 35 Sekunden
        for _ in range(350):  # 350 x 0.1s = 35 Sekunden
            if not running:
                return  # Falls das Programm beendet wird, sofort aussteigen
            
            # Falls in der Zwischenzeit ein neuer Fisch gefunden wird -> sofort weiter!
            if match_found_event.is_set():
                print("Neuer Fisch gefunden während der Wartezeit!")
                print("+++ ",time.time() - last_fish_time, " +++ TIME Passed")
                last_fish_time = time.time()
                break  
            
            time.sleep(0.1)  # Kurze Pause (nicht blockierend)

        # Falls nach 35 Sekunden kein Fisch gefunden wurde, erneut "0" drücken
        if time.time() - last_fish_time >= 35.0:
            print("Kein Fisch gefunden, erneut '0' drücken")
            pyautogui.press("0")
            # reset time
            last_fish_time = time.time()

# Threads starten
thread1 = threading.Thread(target=capture_screen, daemon=True)
thread2 = threading.Thread(target=process_image, daemon=True)
thread3 = threading.Thread(target=mouse_action, daemon=True)

thread1.start()
thread2.start()
thread3.start()

# Hauptthread warten lassen, bis "q" gedrückt wird
try:
    while running:
        pass
except KeyboardInterrupt:
    running = False

cv2.destroyAllWindows()
