import cv2

class Camera:
    def __init__(self, width=640, height=480):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        frame = cv2.flip(frame, 1)  # mirror
        return frame

    def release(self):
        self.cap.release()