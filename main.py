import cv2
import pyautogui
from core.camera import Camera
from core.hand_tracker import HandTracker
from gestures.gesture_engine import GestureEngine
from actions.mouse_controller import MouseController
import math

# Init
camera = Camera()
tracker = HandTracker()
gesture = GestureEngine()

screen_w, screen_h = pyautogui.size()
mouse = MouseController(screen_w, screen_h)

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