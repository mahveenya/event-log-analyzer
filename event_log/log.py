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
    def error_rate(self):
        pass  # TODO
