"""
=========================================================
ORBITAL AI
Main Vision Pipeline
Sprint 5.0 (Final)

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
Vehicle Tracker
   │
   ▼
Speed Estimation
   │
   ▼
Traffic Analytics
   │
   ▼
HUD + CSV + MP4 Output
=========================================================
"""

import cv2

from detector import VehicleDetector
from tracker import VehicleTracker
from analytics import TrafficAnalytics
from visualizer import Visualizer
from logger import TrafficLogger
from speed import SpeedEstimator
from lane import LaneDetector
from density import LaneDensity
from congestion import CongestionAnalyzer
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
# Initialize Modules
# =========================================================

detector = VehicleDetector()
tracker = VehicleTracker()
analytics = TrafficAnalytics(line_y=540)
visualizer = Visualizer()
logger = TrafficLogger()
lane_detector = LaneDetector()
density = LaneDensity()
congestion = CongestionAnalyzer()

# Speed Estimator
speed_estimator = SpeedEstimator(
    fps=fps,
    pixels_per_meter=8.5
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
    # STEP 2 : Create Stable Tracks
    # -----------------------------------------------------
    tracks = tracker.update(detections)

    # -----------------------------------------------------
    # STEP 3 : Assign Lane Number
    # -----------------------------------------------------
    for track in tracks:
        track.lane = lane_detector.get_lane(track)
    lane_counts = density.update(tracks)    
    level, level_color = congestion.update(
    density.total_visible()
)
    # -----------------------------------------------------
    # STEP 4 : Calculate Speed
    # -----------------------------------------------------
    speeds = speed_estimator.update(tracks)

    # -----------------------------------------------------
    # STEP 5 : Count Vehicles
    # -----------------------------------------------------
    analytics.update(tracks)

    # -----------------------------------------------------
    # STEP 6 : CSV Logger
    # -----------------------------------------------------
    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    for track in tracks:

        if (
            track.id in analytics.counted_ids
            and track.id not in logged_ids
        ):

            logger.log(
                vehicle_id=track.id,
                vehicle_type=VEHICLE_NAMES.get(
                    track.class_id,
                    "Vehicle"
                ),
                timestamp=timestamp
            )

            logged_ids.add(track.id)

    # -----------------------------------------------------
    # STEP 7 : Draw Vehicles
    # -----------------------------------------------------
    frame = visualizer.draw(frame, tracks, speeds)

    # -----------------------------------------------------
    # STEP 8 : Draw Counting Line
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
    # STEP 9 : HUD Panel
   # Background
    cv2.rectangle(frame, (15, 15), (310, 215), (35, 35, 35), -1)

    cv2.putText(frame, "ORBITAL AI", (25, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255), 2)

    cv2.putText(frame,
                f"TOTAL COUNT : {analytics.total_count}",
                (25, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"VISIBLE : {density.total_visible()}",
                (25, 82),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (200,255,200),
                2)

    cv2.putText(frame,
                f"Lane 1 : {lane_counts[1]}",
                (25, 112),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0,255,0),
                2)

    cv2.putText(frame,
                f"Lane 2 : {lane_counts[2]}",
                (25, 137),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,0),
                2)

    cv2.putText(frame,
                f"Lane 3 : {lane_counts[3]}",
                (25, 162),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0,165,255),
                2)

    cv2.putText(frame,
                f"Lane 4 : {lane_counts[4]}",
                (25, 187),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,0,255),
                2)
    cv2.putText(
    frame,
    "CONGESTION",
    (25, 105),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.50,
    (200, 200, 200),
    1
)
    cv2.putText(
        frame,
        level,
        (155, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        level_color,
        2
    )    
        # -----------------------------------------------------
        # STEP 10 : Save Frame
        # -----------------------------------------------------
        writer.write(frame)

cap.release()
writer.release()

print("=" * 55)
print("ORBITAL AI - Sprint 5 Completed Successfully")
print(f"Vehicles Counted : {analytics.total_count}")
print(f"CSV Entries      : {len(logged_ids)}")
print(f"Output Video     : {OUTPUT_VIDEO}")
print("=" * 55)