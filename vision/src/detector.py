"""
=========================================================
ORBITAL AI
Vehicle Detection Engine
Sprint 4.1

Author : Himanshu Sharma

Purpose:
Detect Cars, Bikes, Buses and Trucks using YOLO11 + ByteTrack
=========================================================
"""

from ultralytics import YOLO


class VehicleDetector:

    def __init__(self, model_path="../weights/yolo11s.pt"):
        """
        Initialize YOLO11 Small model
        """
        self.model = YOLO(model_path)

        # COCO vehicle classes
        # 2 = Car
        # 3 = Motorcycle
        # 5 = Bus
        # 7 = Truck
        self.vehicle_classes = [2, 3, 5, 7]

    # ------------------------------------------------------
    # Detect vehicles in one frame
    # ------------------------------------------------------
    def detect(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            tracker="../configs/bytetrack.yaml",
            imgsz=1280,
            conf=0.20,
            iou=0.45,
            verbose=False
        )[0]

        detections = []

        # No detections
        if results.boxes.id is None:
            return detections

        boxes = results.boxes.xyxy.cpu().numpy()
        ids = results.boxes.id.int().cpu().tolist()
        classes = results.boxes.cls.int().cpu().tolist()
        confs = results.boxes.conf.cpu().tolist()

        # Create detection dictionary
        for box, track_id, cls, conf in zip(boxes, ids, classes, confs):

            # Ignore non-vehicle objects
            if cls not in self.vehicle_classes:
                continue

            x1, y1, x2, y2 = map(int, box)

            detections.append({
                "id": track_id,
                "bbox": (x1, y1, x2, y2),
                "class_id": cls,
                "confidence": float(conf)
            })

        return detections