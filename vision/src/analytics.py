"""
=========================================================
ORBITAL AI
Traffic Analytics Engine
Sprint 5.1

Purpose:
Count every vehicle exactly once when it crosses
the virtual counting line.
=========================================================
"""


class TrafficAnalytics:

    def __init__(self, line_y=540):
        """
        line_y : Vertical position of counting line
        """
        self.line_y = line_y

        # Total vehicles counted
        self.total_count = 0

        # IDs that have already been counted
        self.counted_ids = set()

        # Per-class statistics
        self.class_counts = {
            2: 0,   # Car
            3: 0,   # Bike
            5: 0,   # Bus
            7: 0    # Truck
        }

    # --------------------------------------------------
    # Update counts using tracked vehicles
    # --------------------------------------------------
    def update(self, tracks):

        for track in tracks:

            # Need at least two points to know direction
            if len(track.history) < 2:
                continue

            # Current vehicle ID
            tid = track.id

            # Skip if already counted
            if tid in self.counted_ids:
                continue

            # Previous and current center positions
            prev_x, prev_y = track.history[-2]
            curr_x, curr_y = track.history[-1]

            # Vehicle crossed the line moving downward
            crossed = (
                prev_y < self.line_y and
                curr_y >= self.line_y
            )

            if crossed:

                self.total_count += 1
                self.counted_ids.add(tid)

                # Increase class counter
                if track.class_id in self.class_counts:
                    self.class_counts[track.class_id] += 1

        return self.total_count