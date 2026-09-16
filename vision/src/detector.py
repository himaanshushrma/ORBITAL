"""
=========================================================
ORBITAL AI
Vehicle Detection Engine
Sprint 7.0 (Production)

Author : Himanshu Sharma
=========================================================
"""

import os
from ultralytics import YOLO


class VehicleDetector:

    def __init__(self):

        base = os.path.dirname(os.path.abspath(__file__))

        model_path = os.path.join(
            base,
            "../models/yolo11s.pt"
        )

        tracker_path = os.path.join(
            base,
            "../configs/bytetrack.yaml"
        )

        self.tracker = tracker_path

        self.model = YOLO(model_path)

        # COCO Vehicle Classes
        self.vehicle_classes = [2, 3, 5, 7]

    # ------------------------------------------------------
    # Detect vehicles
    # ------------------------------------------------------
    def detect(self, frame):

        result = self.model.track(
            source=frame,
            persist=True,
            tracker=self.tracker,
            classes=self.vehicle_classes,
            imgsz=1280,
            conf=0.20,
            iou=0.45,
            verbose=False
        )[0]

        detections = []

        if result.boxes.id is None:
            return detections

        boxes = result.boxes.xyxy.cpu().numpy()
        ids = result.boxes.id.int().cpu().tolist()
        classes = result.boxes.cls.int().cpu().tolist()
        confs = result.boxes.conf.cpu().tolist()

        for box, track_id, cls, conf in zip(
            boxes,
            ids,
            classes,
            confs
        ):

            x1, y1, x2, y2 = map(int, box)

            detections.append({
                "id": track_id,
                "bbox": (x1, y1, x2, y2),
                "class_id": cls,
                "confidence": float(conf)
            })

        return detections