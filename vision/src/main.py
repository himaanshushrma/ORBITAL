import cv2
import os

from detector import DroneDetector
from visualizer import Visualizer

INPUT_VIDEO = "../data/traffic.mp4"
OUTPUT_DIR = "../output"
OUTPUT_VIDEO = "../output/detection.mp4"

os.makedirs(OUTPUT_DIR, exist_ok=True)

detector = DroneDetector()
visualizer = Visualizer()

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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect(frame)
    frame = visualizer.draw(frame, detections)

    writer.write(frame)

cap.release()
writer.release()

print(f"Saved: {OUTPUT_VIDEO}")