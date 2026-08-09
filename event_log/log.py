from event_log import Event, EventSeverity


class EventLog:
    def __init__(self, events):
        self._events = events

    def filter_by_severity(self, min_severity: EventSeverity) -> list[Event]:
        return [event for event in self._events if event.severity >= min_severity]

    def count_by_object(self):
        pass  # TODO

    @property
    def error_rate(self):
        pass  # TODO
