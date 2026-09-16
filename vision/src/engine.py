import os
import cv2

from detector import VehicleDetector
from tracker import VehicleTracker
from analytics import TrafficAnalytics
from visualizer import Visualizer
from speed import SpeedEstimator
from lane import LaneDetector
from density import LaneDensity
from congestion import CongestionAnalyzer


def stream_video(video_path):

    # -----------------------------
    # Open Video
    # -----------------------------
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Cannot open video.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # -----------------------------
    # Output Video
    # -----------------------------
    base = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(base, "../output")
    os.makedirs(output_dir, exist_ok=True)

    output_video = os.path.join(output_dir, "detection.mp4")

    writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    # -----------------------------
    # Initialize AI Modules
    # -----------------------------
    detector = VehicleDetector()
    tracker = VehicleTracker()

    analytics = TrafficAnalytics(
        line_y=int(height * 0.5)
    )

    visualizer = Visualizer()

    lane_detector = LaneDetector()
    density = LaneDensity()
    congestion = CongestionAnalyzer()

    speed_estimator = SpeedEstimator(
        fps=fps,
        pixels_per_meter=8.5
    )

    # =============================
    # MAIN LOOP
    # =============================
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Detection
        detections = detector.detect(frame)

        # Tracking
        tracks = tracker.update(detections)

        # Lane Assignment
        for track in tracks:
            track.lane = lane_detector.get_lane(track)

        # Lane Density
        lane_counts = density.update(tracks)

        # Congestion
        level, level_color = congestion.update(
            density.total_visible()
        )

        # Speed Estimation
        speeds = speed_estimator.update(tracks)

        # Vehicle Counting
        analytics.update(tracks)

        # Draw Everything
        frame = visualizer.draw(
            frame,
            tracks,
            speeds
        )

        # Counting Line
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

        # Save Output
        writer.write(frame)

        # Stream to Dashboard
        yield {
            "frame": frame,
            "total": analytics.total_count,
            "visible": density.total_visible(),
            "lanes": lane_counts,
            "congestion": level,
            "fps": fps,
            "output": output_video
        }

    # =============================
    # Cleanup
    # =============================
    cap.release()
    writer.release()