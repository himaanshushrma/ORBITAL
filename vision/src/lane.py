"""
=========================================================
ORBITAL AI
Lane Detection Module
Sprint 6.2

Author : Himanshu Sharma

Purpose
---------------------------------------------------------
Assign each vehicle to a highway lane using its
bird's-eye transformed X coordinate.
=========================================================
"""

from calibration import PerspectiveCalibrator


class LaneDetector:

    def __init__(self):

        # Perspective transformer
        self.calibrator = PerspectiveCalibrator()

        # Lane boundaries in Bird's Eye View
        self.boundaries = [0, 480, 960, 1440, 1920]

    # -----------------------------------------------------
    # Return lane number (1–4)
    # -----------------------------------------------------
    def get_lane(self, track):

        x1, y1, x2, y2 = track.bbox

        # Vehicle center
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Convert to Bird's Eye
        bx, _ = self.calibrator.transform_point((cx, cy))

        for i in range(4):
            if self.boundaries[i] <= bx < self.boundaries[i + 1]:
                return i + 1

        return 4