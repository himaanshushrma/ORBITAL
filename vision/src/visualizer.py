"""
=========================================================
ORBITAL AI
Visualizer Module
Sprint 11.1

Author : Himanshu Sharma

Features
---------------------------------------------------------
• Lane polygon overlay
• Vehicle bounding boxes
• Vehicle IDs
• Speed labels
• Trajectory trails
• Center points
=========================================================
"""

import cv2
import numpy as np


class Visualizer:

    def __init__(self):

        self.colors = {
            1: (0, 255, 0),
            2: (255, 255, 0),
            3: (0, 165, 255),
            4: (255, 0, 255)
        }

        # Reference polygons (1920×1080)
        self.lane_polygons = {

            1: np.array([
                [80,1035],
                [620,430],
                [790,430],
                [560,1035]
            ], np.int32),

            2: np.array([
                [560,1035],
                [790,430],
                [960,430],
                [930,1035]
            ], np.int32),

            3: np.array([
                [930,1035],
                [960,430],
                [1125,430],
                [1300,1035]
            ], np.int32),

            4: np.array([
                [1300,1035],
                [1125,430],
                [1880,1035]
            ], np.int32)
        }

    # --------------------------------------------------
    # Scale polygons to current resolution
    # --------------------------------------------------

    def _scale_polygon(self, polygon, width, height):

        sx = width / 1920
        sy = height / 1080

        pts = polygon.astype(np.float32)

        pts[:,0] *= sx
        pts[:,1] *= sy

        return pts.astype(np.int32)

    # --------------------------------------------------
    # Draw Lane Overlay
    # --------------------------------------------------

    def draw_lanes(self, frame):

        h, w = frame.shape[:2]

        overlay = frame.copy()

        for lane, poly in self.lane_polygons.items():

            scaled = self._scale_polygon(poly, w, h)

            cv2.fillPoly(
                overlay,
                [scaled],
                self.colors[lane]
            )

            cv2.polylines(
                frame,
                [scaled],
                True,
                self.colors[lane],
                2
            )

            M = cv2.moments(scaled)

            if M["m00"] != 0:

                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                cv2.putText(
                    frame,
                    f"L{lane}",
                    (cx-12, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )

        cv2.addWeighted(
            overlay,
            0.18,
            frame,
            0.82,
            0,
            frame
        )

        return frame

    # --------------------------------------------------
    # Draw Vehicles + Trails
    # --------------------------------------------------

    def draw(self, frame, tracks, speeds):

        frame = self.draw_lanes(frame)

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            lane = getattr(track, "lane", 1)

            color = self.colors.get(
                lane,
                (255,255,255)
            )

            # ==========================================
            # TRAJECTORY TRAIL
            # ==========================================

            if hasattr(track, "history"):

                pts = list(track.history)

                for i in range(1, len(pts)):

                    alpha = i / len(pts)

                    thickness = max(
                        1,
                        int(alpha * 4)
                    )

                    cv2.line(
                        frame,
                        pts[i-1],
                        pts[i],
                        color,
                        thickness
                    )

            # ==========================================
            # Bounding Box
            # ==========================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            speed = int(
                speeds.get(track.id, 0)
            )

            label = (
                f"ID {track.id} | "
                f"L{lane} | "
                f"{speed} km/h"
            )

            (tw, th), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                1
            )

            cv2.rectangle(
                frame,
                (x1, y1-24),
                (x1+tw+8, y1),
                color,
                -1
            )

            cv2.putText(
                frame,
                label,
                (x1+4, y1-7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,0,0),
                1
            )

            # ==========================================
            # Center Point
            # ==========================================

            cx = int((x1+x2)/2)
            cy = int((y1+y2)/2)

            cv2.circle(
                frame,
                (cx, cy),
                3,
                (255,255,255),
                -1
            )

        return frame