"""
=========================================================
ORBITAL AI
Traffic Analytics Engine
Sprint 4.2

Author : Himanshu Sharma

Purpose:
Count each vehicle exactly ONCE using ByteTrack IDs.
=========================================================
"""


class TrafficAnalytics:

    def __init__(self, line_y=760):
        """
        line_y : Horizontal counting line
        For 1920x1080 video -> 760 works well
        """

        self.line_y = line_y

        # Vehicles already counted
        self.counted_ids = set()

        # Previous Y coordinate of every vehicle
        self.previous_y = {}

        # Total vehicles
        self.total_count = 0

    # ------------------------------------------------------
    # Update Counter
    # ------------------------------------------------------
    def update(self, tracks):

        for track in tracks:

            tid = track.id

            # Need at least 2 points to detect movement
            if len(track.history) < 2:
                continue

            prev_y = track.history[-2][1]
            curr_y = track.history[-1][1]

            self.previous_y[tid] = curr_y

            # Count only once
            if tid in self.counted_ids:
                continue

            # Vehicle crossed downward
            if prev_y < self.line_y and curr_y >= self.line_y:

                self.total_count += 1
                self.counted_ids.add(tid)

        return self.total_count