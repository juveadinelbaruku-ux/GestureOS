import math
import time

class GestureEngine:
    def __init__(self):
        pass
        self.last_click_time = 0
        self.click_delay = 0.5  # seconds

    def fingers_up(self, landmarks):
        fingers = []

        if not landmarks:
            return []
                
        # Tip IDs
        tips = [4, 8, 12, 16, 20]

        # Thumb (x comparison)
        if landmarks[tips[0]][1] > landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Thumb
        fingers.append(1 if landmarks[tips[0]][1] > landmarks[tips[0]-1][1] else 0)

        # Other fingers (y comparison)
        # Other fingers
        for i in range(1, 5):
            if landmarks[tips[i]][2] < landmarks[tips[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            fingers.append(1 if landmarks[tips[i]][2] < landmarks[tips[i]-2][2] else 0)

        return fingers

    def is_click(self, landmarks):
        x1, y1 = landmarks[8][1], landmarks[8][2]  # index
        x2, y2 = landmarks[4][1], landmarks[4][2]  # thumb

        distance = math.hypot(x2 - x1, y2 - y1)

        current_time = time.time()

        if distance < 30 and (current_time - self.last_click_time) > self.click_delay:
            self.last_click_time = current_time
            return True

        return False

    def is_drag(self, landmarks):
        x1, y1 = landmarks[8][1], landmarks[8][2]
        x2, y2 = landmarks[4][1], landmarks[4][2]

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance < 40  # slightly larger threshold

    def is_scroll(self, fingers):
        return fingers == [0, 1, 1, 0, 0]  # index + middle