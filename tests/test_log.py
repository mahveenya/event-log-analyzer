import unittest

from event_log import Event, EventLog, EventSeverity


def make_event(severity: EventSeverity, object_name: str) -> Event:
    return Event(
        event_number="1",
        timestamp="2026-01-01 00:00:00",
        severity=severity,
        object_name=object_name,
        object_id="0",
        event_id="0",
        event_name=None,
        description=None,
        remedy=None,
        readable=None,
        raw=None,
    )


class FilterBySeverityTests(unittest.TestCase):
    def test_returns_events_at_or_above_min_severity(self):
        events = [
            make_event(EventSeverity.INFO, "a"),
            make_event(EventSeverity.WARNING, "b"),
            make_event(EventSeverity.ERROR, "c"),
        ]
        log = EventLog(events)

        result = log.filter_by_severity(EventSeverity.WARNING)

        self.assertIsInstance(result, EventLog)
        self.assertEqual(
            [e.severity for e in result.events],
            [EventSeverity.WARNING, EventSeverity.ERROR],
        )

    def test_info_min_returns_all(self):
        events = [
            make_event(EventSeverity.INFO, "a"),
            make_event(EventSeverity.ERROR, "b"),
        ]
        log = EventLog(events)

        self.assertEqual(len(log.filter_by_severity(EventSeverity.INFO).events), 2)

    def test_empty_log_returns_empty(self):
        result = EventLog([]).filter_by_severity(EventSeverity.INFO)

        self.assertEqual(result.events, [])


class CountByObjectTests(unittest.TestCase):
    def test_counts_events_per_object_name(self):
        events = [
            make_event(EventSeverity.INFO, "sensor"),
            make_event(EventSeverity.WARNING, "sensor"),
            make_event(EventSeverity.ERROR, "bluetooth"),
        ]
        log = EventLog(events)

        self.assertEqual(log.count_by_object(), {"sensor": 2, "bluetooth": 1})

    def test_empty_log_returns_empty_dict(self):
        self.assertEqual(EventLog([]).count_by_object(), {})


class ErrorRateTests(unittest.TestCase):
    def test_fraction_of_error_events(self):
        events = [
            make_event(EventSeverity.INFO, "a"),
            make_event(EventSeverity.ERROR, "b"),
            make_event(EventSeverity.WARNING, "c"),
            make_event(EventSeverity.ERROR, "d"),
        ]
        log = EventLog(events)

        self.assertEqual(log.error_rate, 0.5)

    def test_no_errors_is_zero(self):
        log = EventLog([make_event(EventSeverity.INFO, "a")])
        self.assertEqual(log.error_rate, 0)

    def test_empty_log_is_zero(self):
        self.assertEqual(EventLog([]).error_rate, 0)


if __name__ == "__main__":
    unittest.main()
