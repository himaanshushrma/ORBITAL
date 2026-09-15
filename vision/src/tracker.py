from dataclasses import dataclass

# =====================================================
# ORBITAL - Vehicle Tracking Engine
# Sprint 2.3 : Persistent ID Assignment
# =====================================================

@dataclass
class Track:
    id: int
    bbox: tuple
    class_id: int
    confidence: float
    age: int = 0


class VehicleTracker:

    def __init__(self):
        # Dictionary -> {id : Track}
        self.tracks = {}
        self.next_id = 1

    # -------------------------------------------------
    # IoU (Intersection over Union)
    # -------------------------------------------------
    def calculate_iou(self, boxA, boxB):

        ax1, ay1, ax2, ay2 = boxA
        bx1, by1, bx2, by2 = boxB

        inter_x1 = max(ax1, bx1)
        inter_y1 = max(ay1, by1)

        inter_x2 = min(ax2, bx2)
        inter_y2 = min(ay2, by2)

        if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
            return 0.0

        intersection = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)

        areaA = (ax2 - ax1) * (ay2 - ay1)
        areaB = (bx2 - bx1) * (by2 - by1)

        union = areaA + areaB - intersection

        return intersection / union

    # -------------------------------------------------
    # Assign persistent IDs to detections
    # -------------------------------------------------
    def update(self, detections):

        updated_tracks = {}

        for det in detections:

            best_iou = 0
            best_track = None

            # Compare with existing tracks
            for track in self.tracks.values():

                iou = self.calculate_iou(track.bbox, det["bbox"])

                if iou > best_iou:
                    best_iou = iou
                    best_track = track

            # Same vehicle
            if best_iou > 0.30:

                best_track.bbox = det["bbox"]
                best_track.confidence = det["confidence"]
                best_track.age = 0

                updated_tracks[best_track.id] = best_track

            # New vehicle
            else:

                new_track = Track(
                    id=self.next_id,
                    bbox=det["bbox"],
                    class_id=det["class_id"],
                    confidence=det["confidence"]
                )

                updated_tracks[self.next_id] = new_track
                self.next_id += 1

        self.tracks = updated_tracks

        return list(self.tracks.values())