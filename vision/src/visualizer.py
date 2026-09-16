"""
=========================================================
ORBITAL AI
Visualizer Module
Sprint 5.0

Draws:
- Bounding boxes
- Vehicle labels
- Trajectory trails
- Live speed (km/h)
=========================================================
"""

import cv2


class Visualizer:

    def __init__(self):

        self.names = {
            2: "Car",
            3: "Bike",
            5: "Bus",
            7: "Truck"
        }

        self.colors = {
            2: (0, 255, 0),       # Car
            3: (255, 255, 0),     # Bike
            5: (0, 165, 255),     # Bus
            7: (255, 0, 255)      # Truck
        }

    # -----------------------------------------------------
    # Draw every tracked vehicle
    # -----------------------------------------------------
    def draw(self, frame, tracks, speeds):

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            name = self.names.get(track.class_id, "Vehicle")
            color = self.colors.get(track.class_id, (255, 255, 255))

            # Current speed
            speed = speeds.get(track.id, 0)

            # Label
            label = f"{name} #{track.id} | {speed:.0f} km/h"

            # Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Label background
            cv2.rectangle(
                frame,
                (x1, y1 - 24),
                (x1 + 150, y1),
                color,
                -1
            )

            # Label text
            cv2.putText(
                frame,
                label,
                (x1 + 3, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 0, 0),
                1
            )

            # Trajectory
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