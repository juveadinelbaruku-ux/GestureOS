import pyautogui
import numpy as np

pyautogui.FAILSAFE = False

class MouseController:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.prev_x, self.prev_y = 0, 0
        self.smoothening = 5

    def move(self, x, y, frame_w, frame_h):
        screen_x = np.interp(x, (0, frame_w), (0, self.screen_w))
        screen_y = np.interp(y, (0, frame_h), (0, self.screen_h))

        # Smooth movement
        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        pyautogui.click()