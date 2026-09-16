"""
=========================================================
ORBITAL AI
Perspective Calibration
Sprint 8.0 (Dynamic)
=========================================================
"""

import cv2
import numpy as np


class PerspectiveCalibrator:

    def __init__(self):

        self.matrix = None
        self.src = None

    # --------------------------------------------------
    # Create homography from 4 clicked points
    # Order:
    # Top Left
    # Top Right
    # Bottom Right
    # Bottom Left
    # --------------------------------------------------
    def compute(self, points, width=1920, height=1080):

        if len(points) != 4:
            raise ValueError("Exactly 4 points required")

        self.src = np.float32(points)

        dst = np.float32([
            [300, 0],
            [1620, 0],
            [1620, 1080],
            [300, 1080]
        ])

        self.matrix = cv2.getPerspectiveTransform(
            self.src,
            dst
        )

        return self.matrix

    # --------------------------------------------------
    # Convert image point
    # --------------------------------------------------
    def transform_point(self, point):

        if self.matrix is None:
            return point

        pts = np.array([[point]], dtype=np.float32)

        warped = cv2.perspectiveTransform(
            pts,
            self.matrix
        )

        x, y = warped[0][0]

        return float(x), float(y)

    # --------------------------------------------------
    # Bird eye frame
    # --------------------------------------------------
    def warp(self, frame):

        if self.matrix is None:
            return frame

        return cv2.warpPerspective(
            frame,
            self.matrix,
            (1920, 1080)
        )