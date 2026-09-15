import cv2

CLASS_NAMES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}

class Visualizer:

    def draw(self, frame, detections):

        for det in detections:

            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            cls = det["class_id"]

            if cls not in CLASS_NAMES:
                continue

            label = f"{CLASS_NAMES[cls]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return frame