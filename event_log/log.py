class EventLog:
    def __init__(self, events):
        self._events = events

    def filter_by_severity(self, min_severity):
        pass  # TODO

    def count_by_object(self):
        pass  # TODO

    @property
    def error_rate(self):
        pass  # TODO
