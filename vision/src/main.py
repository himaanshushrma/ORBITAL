import cv2

from detector import VehicleDetector
from tracker import VehicleTracker
from visualizer import Visualizer

# ---------------------------------------
# Initialize modules
# ---------------------------------------
detector = VehicleDetector()
tracker = VehicleTracker()
visualizer = Visualizer()

# ---------------------------------------
# Input / Output
# ---------------------------------------
INPUT_VIDEO = "../data/traffic.mp4"
OUTPUT_VIDEO = "../output/detection.mp4"

cap = cv2.VideoCapture(INPUT_VIDEO)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

# ---------------------------------------
# Main Processing Loop
# ---------------------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    # STEP 1 : Object Detection
    detections = detector.detect(frame)

    # STEP 2 : Multi Object Tracking
    tracks = tracker.update(detections)

    # STEP 3 : Visualization
    frame = visualizer.draw(frame, tracks)

    # STEP 4 : Save frame
    writer.write(frame)

# ---------------------------------------
# Cleanup
# ---------------------------------------
cap.release()
writer.release()

print("Sprint 2 completed successfully.")
print(f"Output saved to: {OUTPUT_VIDEO}")