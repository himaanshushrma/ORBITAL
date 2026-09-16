"""
=========================================================
ORBITAL AI
Visualizer Module
Sprint 6.2

Author : Himanshu Sharma

Purpose
---------------------------------------------------------
Draws:
1. Bounding Boxes
2. Vehicle Labels
3. Lane Number
4. Live Speed
5. Trajectory Trails
=========================================================
"""

import cv2


class Visualizer:

    def __init__(self):

        # Vehicle class names
        self.names = {
            2: "Car",
            3: "Bike",
            5: "Bus",
            7: "Truck"
        }

        # BGR Colors
        self.colors = {
            2: (0, 255, 0),        # Car
            3: (255, 255, 0),      # Bike
            5: (0, 165, 255),      # Bus
            7: (255, 0, 255)       # Truck
        }

    # -----------------------------------------------------
    # Draw all tracked vehicles
    # -----------------------------------------------------
    def draw(self, frame, tracks, speeds):

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            name = self.names.get(track.class_id, "Vehicle")
            color = self.colors.get(track.class_id, (255, 255, 255))

            # ----------------------------
            # Speed & Lane
            # ----------------------------
            speed = speeds.get(track.id, 0)

            lane = getattr(track, "lane", 0)

            # Label
            label = (
                f"{name} #{track.id} | "
                f"L{lane} | "
                f"{speed:.0f} km/h"
            )

            # ----------------------------
            # Bounding Box
            # ----------------------------
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Label Background
            cv2.rectangle(
                frame,
                (x1, y1 - 24),
                (x1 + 190, y1),
                color,
                -1
            )

            # Label Text
            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 0, 0),
                1,
                cv2.LINE_AA
            )

            # ----------------------------
            # Trajectory Trail
            # ----------------------------
            if len(track.history) > 1:

                for i in range(1, len(track.history)):

                    cv2.line(
                        frame,
                        track.history[i - 1],
                        track.history[i],
                        (255, 0, 0),
                        2
                    )

            # Center Point
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.circle(
                frame,
                (cx, cy),
                3,
                (0, 0, 255),
                -1
            )

        return frame