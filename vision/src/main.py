"""
=========================================================
ORBITAL AI
Main Vision Pipeline
Sprint 4.4 (Final)

Author : Himanshu Sharma

Pipeline
---------------------------------------------------------
Video
   │
   ▼
YOLO11 Detection + ByteTrack IDs
   │
   ▼
Tracker (Trajectory History)
   │
   ▼
Traffic Analytics (Line Counting)
   │
   ▼
Visualizer (HUD + Boxes + Trails)
=========================================================
"""

import cv2

from detector import VehicleDetector
from tracker import VehicleTracker
from analytics import TrafficAnalytics
from visualizer import Visualizer


# =========================================================
# Initialize Modules
# =========================================================

detector = VehicleDetector()

tracker = VehicleTracker()

# 1080p video → counting line
analytics = TrafficAnalytics(line_y=760)

visualizer = Visualizer()


# =========================================================
# Input / Output Paths
# =========================================================

INPUT_VIDEO = "../data/traffic.mp4"

OUTPUT_VIDEO = "../output/detection.mp4"


# =========================================================
# Open Video
# =========================================================

cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    raise FileNotFoundError(f"Cannot open video: {INPUT_VIDEO}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)


# =========================================================
# Main Processing Loop
# =========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # -----------------------------------------------------
    # STEP 1 : Detect Vehicles
    # -----------------------------------------------------
    detections = detector.detect(frame)

    # -----------------------------------------------------
    # STEP 2 : Update Track Histories
    # -----------------------------------------------------
    tracks = tracker.update(detections)

    # -----------------------------------------------------
    # STEP 3 : Count Vehicles
    # -----------------------------------------------------
    total_count = analytics.update(tracks)

    # -----------------------------------------------------
    # STEP 4 : Draw Boxes + Labels + Trails
    # -----------------------------------------------------
    frame = visualizer.draw(frame, tracks)

    # -----------------------------------------------------
    # STEP 5 : Draw Counting Line
    # -----------------------------------------------------
    cv2.line(
        frame,
        (0, analytics.line_y),
        (width, analytics.line_y),
        (0, 0, 255),
        3
    )

    # Label for counting line
    cv2.putText(
        frame,
        "COUNT LINE",
        (20, analytics.line_y - 12),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    # -----------------------------------------------------
    # STEP 6 : HUD Panel
    # -----------------------------------------------------
    cv2.rectangle(
        frame,
        (15, 15),
        (250, 90),
        (35, 35, 35),
        -1
    )

    cv2.putText(
        frame,
        "TOTAL VEHICLES",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (220, 220, 220),
        2
    )

    cv2.putText(
        frame,
        str(total_count),
        (30, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    # -----------------------------------------------------
    # STEP 7 : Save Frame
    # -----------------------------------------------------
    writer.write(frame)


# =========================================================
# Cleanup
# =========================================================

cap.release()
writer.release()

print("=" * 55)
print("ORBITAL AI - Sprint 4 Completed Successfully")
print(f"Vehicles Counted : {total_count}")
print(f"Output Saved     : {OUTPUT_VIDEO}")
print("=" * 55)