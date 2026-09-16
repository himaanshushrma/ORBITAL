"""
=========================================================
ORBITAL AI
Perspective Speed Estimation
Sprint 6.1
=========================================================
"""

from collections import deque
import math

from calibration import PerspectiveCalibrator


class SpeedEstimator:

    def __init__(self, fps, pixels_per_meter=18):

        self.fps = fps
        self.pixels_per_meter = pixels_per_meter

        self.history = {}
        self.speeds = {}

        # Perspective transformer
        self.calibrator = PerspectiveCalibrator()

    # -----------------------------------------
    # Euclidean distance
    # -----------------------------------------
    def distance(self, p1, p2):

        return math.sqrt(
            (p2[0] - p1[0]) ** 2 +
            (p2[1] - p1[1]) ** 2
        )

    # -----------------------------------------
    # Update vehicle speeds
    # -----------------------------------------
    def update(self, tracks):

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            # Vehicle center
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            # Convert to Bird's Eye coordinates
            bird_point = self.calibrator.transform_point((cx, cy))

            if track.id not in self.history:
                self.history[track.id] = deque(maxlen=10)

            self.history[track.id].append(bird_point)

            pts = self.history[track.id]

            if len(pts) < 2:
                self.speeds[track.id] = 0
                continue

            pixel_dist = self.distance(pts[0], pts[-1])

            meter_dist = pixel_dist / self.pixels_per_meter

            time_sec = (len(pts) - 1) / self.fps

            if time_sec <= 0:
                speed = 0
            else:
                speed = (meter_dist / time_sec) * 3.6

            self.speeds[track.id] = round(speed, 1)

        return self.speeds

    def get_speed(self, track_id):
        return self.speeds.get(track_id, 0)