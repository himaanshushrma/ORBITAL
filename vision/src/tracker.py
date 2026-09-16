"""
=========================================================
ORBITAL AI
Tracker Module
Sprint 7.0 (Compatible)

Author : Himanshu Sharma
=========================================================
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Track:
    id: int
    class_id: int
    bbox: Tuple[int, int, int, int]
    history: List[Tuple[int, int]] = field(default_factory=list)
    lane: int = 0


class VehicleTracker:

    def __init__(self):
        self.histories = {}

    # ------------------------------------------------------
    # Update Tracks
    # ------------------------------------------------------
    def update(self, detections):

        current_tracks = []

        if len(detections) == 0:
            return current_tracks

        for det in detections:

            track_id = det["id"]
            class_id = det["class_id"]

            x1, y1, x2, y2 = det["bbox"]

            center = (
                (x1 + x2) // 2,
                (y1 + y2) // 2
            )

            if track_id not in self.histories:
                self.histories[track_id] = []

            self.histories[track_id].append(center)

            # Keep only last 30 points
            self.histories[track_id] = self.histories[track_id][-30:]

            current_tracks.append(
                Track(
                    id=track_id,
                    class_id=class_id,
                    bbox=(x1, y1, x2, y2),
                    history=self.histories[track_id].copy()
                )
            )

        return current_tracks