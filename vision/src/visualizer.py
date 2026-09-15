import cv2

# Vehicle names (COCO classes)
CLASS_NAMES = {
    2: "Car",
    3: "Bike",
    5: "Bus",
    7: "Truck"
}

# Different color for each vehicle
CLASS_COLORS = {
    2: (0, 255, 0),      # Green
    3: (255, 255, 0),    # Cyan
    5: (0, 165, 255),    # Orange
    7: (255, 0, 255)     # Purple
}


class Visualizer:

    def draw(self, frame, tracks):

        for track in tracks:

            # Bounding box coordinates
            x1, y1, x2, y2 = map(int, track.bbox)

            # Vehicle information
            vehicle_name = CLASS_NAMES.get(track.class_id, "Vehicle")
            color = CLASS_COLORS.get(track.class_id, (255, 255, 255))

            # Create label
            label = f"{vehicle_name} #{track.id}"

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Calculate label size
            (w, h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                2
            )

            # Label background
            cv2.rectangle(
                frame,
                (x1, y1 - 25),
                (x1 + w + 8, y1),
                color,
                -1
            )

            # Label text
            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

        return frame