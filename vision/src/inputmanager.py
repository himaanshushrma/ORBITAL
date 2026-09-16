
"""
ORBITAL AI
Input Manager
Supports:
1. Video file
2. Webcam
3. RTSP CCTV
"""

import cv2


class InputManager:

    def __init__(self, source):
        """
        source can be:
        - '../data/video.mp4'
        - 0 (webcam)
        - 'rtsp://....'
        """
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise Exception(f"Cannot open source: {source}")

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()

    def width(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    def height(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def fps(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return 30 if fps == 0 else fps