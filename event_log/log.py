from event_log import Event, EventSeverity
from collections import Counter


class EventLog:
    def __init__(self, events):
        self._events = events

    def filter_by_severity(self, min_severity: EventSeverity) -> list[Event]:
        return [event for event in self._events if event.severity >= min_severity]

    def count_by_object(self) -> Counter[str]:
        return Counter(event.object_name for event in self._events)

    @property
    def error_rate(self) -> float:
        if not self._events:
            return 0.0
        error_count = sum(1 for e in self._events if e.severity == EventSeverity.ERROR)
        return error_count / len(self._events)
