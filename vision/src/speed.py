"""
=========================================================
ORBITAL AI
Speed Estimation Module
Sprint 5.0

Author : Himanshu Sharma

Purpose
---------------------------------------------------------
Calculates vehicle speed using:

1. Pixel displacement
2. Video FPS
3. Pixel-to-meter calibration

Formula:

Speed = (distance / time) × 3.6
=========================================================
"""

from collections import deque
import math


class SpeedEstimator:
    """
    Estimate speed for every tracked vehicle.

    Each vehicle keeps a short history of its center points.
    """

    def __init__(self, fps, pixels_per_meter=8.5):

        # Frames per second of the video
        self.fps = fps

        # Calibration value
        # 8.5 pixels ≈ 1 meter
        self.pixels_per_meter = pixels_per_meter

        # Vehicle histories
        self.history = {}

        # Latest computed speeds
        self.speeds = {}

    # -----------------------------------------------------
    # Euclidean Distance
    # -----------------------------------------------------
    def pixel_distance(self, p1, p2):

        x1, y1 = p1
        x2, y2 = p2

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # -----------------------------------------------------
    # Update Speed
    # -----------------------------------------------------
    def update(self, tracks):

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if track.id not in self.history:
                self.history[track.id] = deque(maxlen=10)

            self.history[track.id].append((cx, cy))

            pts = self.history[track.id]

            if len(pts) < 2:
                self.speeds[track.id] = 0
                continue

            start = pts[0]
            end = pts[-1]

            pixel_dist = self.pixel_distance(start, end)

            meter_dist = pixel_dist / self.pixels_per_meter

            frame_diff = len(pts) - 1
            time_sec = frame_diff / self.fps

            if time_sec == 0:
                speed = 0
            else:
                speed = (meter_dist / time_sec) * 3.6

            self.speeds[track.id] = round(speed, 1)

        return self.speeds

    # -----------------------------------------------------
    # Get speed of one vehicle
    # -----------------------------------------------------
    def get_speed(self, track_id):

        return self.speeds.get(track_id, 0)