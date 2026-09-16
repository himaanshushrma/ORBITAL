"""
=========================================================
ORBITAL AI
Visualization Engine
Sprint 4.3

Author : Himanshu Sharma

Purpose:
Draw bounding boxes, labels and trajectory trails.
=========================================================
"""

import cv2

# =========================================================
# Vehicle Names (COCO)
# =========================================================
CLASS_NAMES = {
    2: "Car",
    3: "Bike",
    5: "Bus",
    7: "Truck"
}

# =========================================================
# Colors (BGR)
# =========================================================
CLASS_COLORS = {
    2: (0, 255, 0),      # Green
    3: (255, 255, 0),    # Cyan
    5: (0, 165, 255),    # Orange
    7: (255, 0, 255)     # Purple
}


class Visualizer:

    # -----------------------------------------------------
    # Draw everything
    # -----------------------------------------------------
    def draw(self, frame, tracks):

        for track in tracks:

            x1, y1, x2, y2 = map(int, track.bbox)

            vehicle = CLASS_NAMES.get(track.class_id, "Vehicle")
            color = CLASS_COLORS.get(track.class_id, (255, 255, 255))

            label = f"{vehicle} #{track.id}"

            # Bounding Box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Label size
            (w, h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                2
            )

            # Background
            cv2.rectangle(
                frame,
                (x1, y1 - 24),
                (x1 + w + 8, y1),
                color,
                -1
            )

            # Text
            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

            # -------------------------------------------------
            # Trajectory Trail
            # -------------------------------------------------
            if len(track.history) > 1:

                for i in range(1, len(track.history)):

                    cv2.line(
                        frame,
                        track.history[i - 1],
                        track.history[i],
                        (255, 0, 0),
                        2
                    )

        return frame