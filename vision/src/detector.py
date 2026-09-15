from ultralytics import YOLO


class DroneDetector:

    def __init__(self, model_path="yolo11n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):

        result = self.model(frame, verbose=False)[0]

        detections = []

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            class_id = int(box.cls[0])

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "confidence": confidence,
                "class_id": class_id
            })

        return detections