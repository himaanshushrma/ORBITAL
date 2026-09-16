"""
=========================================================
ORBITAL AI
Congestion Classification Module
Sprint 6.4
=========================================================
"""

class CongestionAnalyzer:

    def __init__(self):
        self.level = "LOW"
        self.color = (0, 255, 0)

    def update(self, visible_count):

        if visible_count <= 8:
            self.level = "LOW"
            self.color = (0, 255, 0)

        elif visible_count <= 16:
            self.level = "MEDIUM"
            self.color = (0, 255, 255)

        else:
            self.level = "HIGH"
            self.color = (0, 0, 255)

        return self.level, self.color