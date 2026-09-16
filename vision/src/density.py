"""
=========================================================
ORBITAL AI
Lane Density Module
Sprint 6.3

Author : Himanshu Sharma

Purpose
---------------------------------------------------------
Counts how many vehicles are currently present
inside each lane.

Output:
Lane 1 : 12
Lane 2 : 15
Lane 3 : 11
Lane 4 : 8
=========================================================
"""


class LaneDensity:

    def __init__(self):

        # Vehicles currently visible in each lane
        self.lanes = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

    # -----------------------------------------------------
    # Update lane occupancy
    # -----------------------------------------------------
    def update(self, tracks):

        # Reset every frame
        self.lanes = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        for track in tracks:

            lane = getattr(track, "lane", 4)

            if lane in self.lanes:
                self.lanes[lane] += 1

        return self.lanes

    # -----------------------------------------------------
    # Total visible vehicles
    # -----------------------------------------------------
    def total_visible(self):

        return sum(self.lanes.values())