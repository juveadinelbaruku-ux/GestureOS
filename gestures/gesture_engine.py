class GestureEngine:
    def __init__(self):
        pass

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

        # Other fingers (y comparison)
        for i in range(1, 5):
            if landmarks[tips[i]][2] < landmarks[tips[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers