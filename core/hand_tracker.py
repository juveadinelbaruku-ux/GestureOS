import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options

mp.solutions = vision

class HandTracker:
    def __init__(self):
        self.base_options = base_options.BaseOptions(model_asset_path='hand_landmarker.task')
        self.options = mp.solutions.HandLandmarkerOptions(
            base_options=self.base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.landmarker = mp.solutions.HandLandmarker.create_from_options(self.options)

    def process(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = self.landmarker.detect(mp_image)
        return results

    def get_landmarks(self, frame, results):
        h, w, _ = frame.shape
        landmarks = []

        if results.hand_landmarks:
            for hand in results.hand_landmarks:
                for id, lm in enumerate(hand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((id, cx, cy))

                # mp.solutions.HandLandmarker.draw_landmarks(frame, hand, connections=mp.solutions.HandLandmarker.HAND_CONNECTIONS)

        return landmarks