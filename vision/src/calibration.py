"""
=========================================================
ORBITAL AI
Perspective Calibration
Sprint 6.1
=========================================================
"""

import cv2
import numpy as np


class PerspectiveCalibrator:
    """
    Converts image coordinates into Bird's Eye coordinates
    using a homography matrix.
    """

    def __init__(self):

        # -------- Source points (1920x1080 traffic video) --------
        self.src = np.float32([
            [620, 430],      # Top Left
            [1295, 430],     # Top Right
            [1880, 1035],    # Bottom Right
            [80, 1035]       # Bottom Left
        ])

        # -------- Destination rectangle --------
        self.dst = np.float32([
            [300, 0],
            [1620, 0],
            [1620, 1080],
            [300, 1080]
        ])

        # Compute homography matrix
        self.matrix = cv2.getPerspectiveTransform(self.src, self.dst)

    # -----------------------------------------------------
    # Convert one image point into Bird's Eye coordinates
    # -----------------------------------------------------
    def transform_point(self, point):

        pts = np.array([[point]], dtype=np.float32)

        warped = cv2.perspectiveTransform(pts, self.matrix)

        x, y = warped[0][0]

        return (float(x), float(y))

    # -----------------------------------------------------
    # Warp an entire frame (for debugging)
    # -----------------------------------------------------
    def warp(self, frame):

        return cv2.warpPerspective(
            frame,
            self.matrix,
            (1920, 1080)
        )