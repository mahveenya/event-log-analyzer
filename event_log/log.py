from collections import Counter

from event_log.event import Event
from event_log.severity import EventSeverity


class EventLog:
    def __init__(self, events: list[Event]):
        self._events = events

    def filter_by_severity(self, min_severity: EventSeverity) -> "EventLog":
        filtered_events = [
            event for event in self._events if event.severity >= min_severity
        ]
        return EventLog(filtered_events)

    def count_by_object(self) -> Counter[str]:
        return Counter(event.object_name for event in self._events)

    @property
    def error_rate(self) -> float:
        if not self._events:
            return 0.0
        error_count = sum(
            1 for event in self._events if event.severity == EventSeverity.ERROR
        )
        return error_count / len(self._events)

    @property
    def events(self) -> list[Event]:
        return list(self._events)
