"""
=========================================================
ORBITAL AI
CSV Logger
Sprint 5.2

Logs every counted vehicle into traffic_log.csv
=========================================================
"""

import csv
import os


class TrafficLogger:

    def __init__(self, path="../output/traffic_log.csv"):

        self.path = path

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(self.path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Vehicle_ID",
                "Vehicle_Type",
                "Timestamp",
                "Direction"
            ])

    def log(self, vehicle_id, vehicle_type, timestamp):

        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                vehicle_id,
                vehicle_type,
                round(timestamp, 2),
                "Down"
            ])