"""
=========================================================
ORBITAL AI
Main Vision Pipeline
Sprint 4.5 (Corrected)

Author : Himanshu Sharma

Pipeline
---------------------------------------------------------
Video
   │
   ▼
YOLO11 Detection
   │
   ▼
ByteTrack IDs
   │
   ▼
Traffic Analytics
   │
   ▼
Visualizer + HUD
   │
   ▼
MP4 + CSV Output
=========================================================
"""

import cv2

from detector import VehicleDetector
from tracker import VehicleTracker
from analytics import TrafficAnalytics
from visualizer import Visualizer
from logger import TrafficLogger


# =========================================================
# Initialize Modules
# =========================================================

detector = VehicleDetector()

tracker = VehicleTracker()

# 1080p video → count line at Y = 540
analytics = TrafficAnalytics(line_y=540)

visualizer = Visualizer()

logger = TrafficLogger()


# =========================================================
# Video Paths
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
# Vehicle Class Names
# =========================================================

VEHICLE_NAMES = {
    2: "Car",
    3: "Bike",
    5: "Bus",
    7: "Truck"
}


# Prevent duplicate CSV entries
logged_ids = set()


# =========================================================
# Main Loop
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
    # STEP 2 : Generate Stable Tracks
    # -----------------------------------------------------

    tracks = tracker.update(detections)

    # -----------------------------------------------------
    # STEP 3 : Traffic Analytics
    # IMPORTANT:
    # Count using TRACKS, not detections.
    # -----------------------------------------------------

    total_count = analytics.update(tracks)

    # -----------------------------------------------------
    # STEP 4 : Log Newly Counted Vehicles
    # Each ID is written only once.
    # -----------------------------------------------------

    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    for track in tracks:

        if track.id in analytics.counted_ids and track.id not in logged_ids:

            logger.log(
                vehicle_id=track.id,
                vehicle_type=VEHICLE_NAMES.get(track.class_id, "Vehicle"),
                timestamp=timestamp
            )

            logged_ids.add(track.id)

    # -----------------------------------------------------
    # STEP 5 : Draw Bounding Boxes + Trails
    # -----------------------------------------------------

    frame = visualizer.draw(frame, tracks)

    # -----------------------------------------------------
    # STEP 6 : Draw Counting Line
    # -----------------------------------------------------

    cv2.line(
        frame,
        (0, analytics.line_y),
        (width, analytics.line_y),
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        "COUNT LINE",
        (20, analytics.line_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    # -----------------------------------------------------
    # STEP 7 : Advanced HUD
    # -----------------------------------------------------

    cv2.rectangle(
        frame,
        (15, 15),
        (280, 180),
        (35, 35, 35),
        -1
    )

    cv2.putText(
        frame,
        "ORBITAL AI",
        (25, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"TOTAL : {analytics.total_count}",
        (25, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Cars   : {analytics.class_counts[2]}",
        (25, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Bikes  : {analytics.class_counts[3]}",
        (25, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Buses  : {analytics.class_counts[5]}",
        (25, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (0, 165, 255),
        2
    )

    cv2.putText(
        frame,
        f"Trucks : {analytics.class_counts[7]}",
        (25, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 0, 255),
        2
    )

    # -----------------------------------------------------
    # STEP 8 : Save Frame
    # -----------------------------------------------------

    writer.write(frame)


# =========================================================
# Cleanup
# =========================================================

cap.release()
writer.release()

print("=" * 55)
print("ORBITAL AI - Sprint 4.5 Completed Successfully")
print(f"Vehicles Counted : {analytics.total_count}")
print(f"CSV Entries      : {len(logged_ids)}")
print(f"Output Video     : {OUTPUT_VIDEO}")
print("=" * 55)