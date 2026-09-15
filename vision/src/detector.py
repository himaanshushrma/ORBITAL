from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="../weights/yolo11n.pt"):
        self.model = YOLO(model_path)

        # COCO vehicle classes
        self.vehicle_classes = [2, 3, 5, 7]

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        detections = []

        for box in results.boxes:
            class_id = int(box.cls[0])

            if class_id in self.vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": float(box.conf[0]),
                    "class_id": class_id
                })

        return detections