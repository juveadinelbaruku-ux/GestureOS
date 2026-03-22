import cv2
import pyautogui
from core.camera import Camera
from core.hand_tracker import HandTracker
from gestures.gesture_engine import GestureEngine
from actions.mouse_controller import MouseController
import math
import time

# Init
camera = Camera()
tracker = HandTracker()
gesture = GestureEngine()

screen_w, screen_h = pyautogui.size()
mouse = MouseController(screen_w, screen_h)

prev_scroll_y = 0

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    results = tracker.process(frame)
    landmarks = tracker.get_landmarks(frame, results)

    if landmarks:
        fingers = gesture.fingers_up(landmarks)

        # Index finger tip
        x1, y1 = landmarks[8][1], landmarks[8][2]

        # Move mouse when only index finger is up
        if fingers == [0, 1, 0, 0, 0]:
            mouse.move(x1, y1, frame.shape[1], frame.shape[0])
            mouse.drag_end()

        elif gesture.is_click(landmarks):
            mouse.click()

        # DRAG
        elif gesture.is_drag(landmarks) and fingers[1] == 1:
            mouse.drag_start()
            mouse.move(x1, y1, frame.shape[1], frame.shape[0])

        else:
            mouse.drag_end()
        
         # SCROLL
        if gesture.is_scroll(fingers):
            current_y = y1

            if prev_scroll_y != 0:
                delta = current_y - prev_scroll_y

                if abs(delta) > 5:
                    mouse.scroll(-int(delta * 2))

            prev_scroll_y = current_y
        else:
            prev_scroll_y = 0

        # Click when index + thumb are close
        x2, y2 = landmarks[4][1], landmarks[4][2]
        distance = math.hypot(x2 - x1, y2 - y1)

        if distance < 30:
            mouse.click()
            cv2.circle(frame, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

    cv2.imshow("GestureOS", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()