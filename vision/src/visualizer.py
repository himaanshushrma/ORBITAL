import cv2

class Visualizer:

    def draw(self, frame, tracks):

        for track in tracks:

            x1, y1, x2, y2 = track.bbox

            # Green bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # ID label
            label = f"ID {track.id}"

            (w, h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            cv2.rectangle(
                frame,
                (x1, y1 - 25),
                (x1 + w + 8, y1),
                (0, 255, 0),
                -1
            )

            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

        return frame