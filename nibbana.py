class NibbanaTracker:
    def calc(self, karma_total: int, meditation_minutes: int):
        progress = (karma_total * 0.3) + (meditation_minutes * 0.7)
        return min(progress / 1000, 1.0)

tracker = NibbanaTracker()