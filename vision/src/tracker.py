"""
=========================================================
ORBITAL AI
ByteTrack History Manager
Sprint 4.1

Author : Himanshu Sharma

Purpose:
Store the movement history of every ByteTrack ID.
ByteTrack generates IDs; this file only maintains trails.
=========================================================
"""

from dataclasses import dataclass, field


# =========================================================
# Track Object
# =========================================================
@dataclass
class Track:
    """
    Represents one tracked vehicle.
    """

    id: int
    bbox: tuple
    class_id: int
    confidence: float

    # Stores previous center points for trajectory drawing
    history: list = field(default_factory=list)


# =========================================================
# Vehicle Tracker
# =========================================================
class VehicleTracker:

    def __init__(self):
        """
        Dictionary format

        histories = {
            12 : [(x1,y1),(x2,y2)...],
            45 : [...]
        }
        """
        self.histories = {}

        # Maximum trail length
        self.max_history = 30

    # -----------------------------------------------------
    # Update histories using ByteTrack IDs
    # -----------------------------------------------------
    def update(self, detections):

        tracks = []

        for det in detections:

            track_id = det["id"]

            x1, y1, x2, y2 = det["bbox"]

            # Calculate center point
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Create history if vehicle appears first time
            if track_id not in self.histories:
                self.histories[track_id] = []

            # Append latest position
            self.histories[track_id].append((cx, cy))

            # Keep only last 30 points
            if len(self.histories[track_id]) > self.max_history:
                self.histories[track_id].pop(0)

            # Convert detection dictionary into Track object
            tracks.append(
                Track(
                    id=track_id,
                    bbox=det["bbox"],
                    class_id=det["class_id"],
                    confidence=det["confidence"],
                    history=self.histories[track_id]
                )
            )

        return tracks