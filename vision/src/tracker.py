"""
=========================================================
ORBITAL AI
Vehicle Tracker
Sprint 11.1

Author : Himanshu Sharma

Features
---------------------------------------------------------
• Stable ByteTrack IDs
• Bounding box updates
• Vehicle history (30 frames)
• Lane support
=========================================================
"""

from collections import deque


class Track:

    def __init__(self, track_id, bbox, class_id):

        self.id = track_id
        self.bbox = bbox
        self.class_id = class_id

        self.lane = 0

        # Store last 30 positions
        self.history = deque(maxlen=30)


class VehicleTracker:

    def __init__(self):

        self.tracks = {}

    # --------------------------------------------------
    # Update active tracks
    # --------------------------------------------------

    def update(self, detections):

        active_tracks = {}

        for det in detections:

            track_id = det["id"]

            if track_id not in self.tracks:

                self.tracks[track_id] = Track(
                    track_id,
                    det["bbox"],
                    det["class_id"]
                )

            track = self.tracks[track_id]

            track.bbox = det["bbox"]
            track.class_id = det["class_id"]

            x1, y1, x2, y2 = det["bbox"]

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Save trajectory point
            track.history.append((cx, cy))

            active_tracks[track_id] = track

        # Remove disappeared tracks
        self.tracks = active_tracks

        return list(active_tracks.values())