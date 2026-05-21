from typing import List
from datetime import datetime, timedelta
from backend.app.models.downtime import DowntimeEvent

class MetricCalculator:
    @staticmethod
    def calculate_mttr(events: List[DowntimeEvent]) -> float:
        resolved_events = [e for e in events if e.duration_minutes is not None]
        if not resolved_events:
            return 0.0
        total_time = sum(e.duration_minutes for e in resolved_events)
        return total_time / len(resolved_events)

    @staticmethod
    def calculate_mtbf(events: List[DowntimeEvent], total_period_minutes: int) -> float:
        if not events:
            return float(total_period_minutes)
        return total_period_minutes / len(events)

    @staticmethod
    def calculate_availability(total_period_minutes: int, downtime_minutes: int) -> float:
        if total_period_minutes == 0:
            return 0.0
        return ((total_period_minutes - downtime_minutes) / total_period_minutes) * 100
