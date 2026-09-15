from ultralytics import YOLO

class VehicleDetector:

    def __init__(self, model_path="../weights/yolo11n.pt"):
        self.model = YOLO(model_path)

        # COCO vehicle classes
        self.vehicle_classes = {
            2: "Car",
            3: "Motorcycle",
            5: "Bus",
            7: "Truck"
        }

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
                    "class_id": class_id,
                    "class_name": self.vehicle_classes[class_id]
                })

        return detections