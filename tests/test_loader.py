import tempfile
import unittest
from pathlib import Path

from event_log import EventSeverity, load_events

COLUMNS = [
    "Event number",
    "Timestamp",
    "Severity",
    "Object name",
    "Object ID",
    "Event ID",
    "Event name",
    "Description",
    "Remedy",
    "Readable",
    "Raw",
]
HEADER = "\t".join(COLUMNS)


def tsv_row(**values: str) -> str:
    row = {column: "" for column in COLUMNS}
    row.update(
        {
            "Event number": "1",
            "Timestamp": "2026-01-01 00:00:00",
            "Severity": "Info",
            "Object name": "sensor",
            "Object ID": "10",
            "Event ID": "100",
        }
    )
    row.update(values)
    return "\t".join(row[column] for column in COLUMNS)


class LoadEventsTests(unittest.TestCase):
    def _write(self, content: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "events.csv"
        path.write_text(content, newline="", encoding="utf-8")
        return path

    def test_loads_rows_as_events(self):
        content = "\n".join(
            [
                HEADER,
                tsv_row(**{"Event number": "1", "Object name": "sensor"}),
                tsv_row(**{"Event number": "2", "Object name": "radio"}),
            ]
        )

        events = load_events(self._write(content))

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_number, "1")
        self.assertEqual(events[0].object_name, "sensor")
        self.assertEqual(events[1].object_name, "radio")

    def test_parses_severity_string_into_enum(self):
        content = "\n".join([HEADER, tsv_row(Severity="Warning")])

        events = load_events(self._write(content))

        self.assertEqual(events[0].severity, EventSeverity.WARNING)

    def test_populated_optional_fields_load_correctly(self):
        content = "\n".join(
            [HEADER, tsv_row(Description="disk full", Remedy="free up space")]
        )

        events = load_events(self._write(content))

        self.assertEqual(events[0].description, "disk full")
        self.assertEqual(events[0].remedy, "free up space")

    def test_skips_sep_line(self):
        content = "\n".join(["sep=\t", HEADER, tsv_row(**{"Object name": "sensor"})])

        events = load_events(self._write(content))

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].object_name, "sensor")

    def test_without_sep_line_first_row_is_header(self):
        content = "\n".join([HEADER, tsv_row(**{"Object name": "sensor"})])

        events = load_events(self._write(content))

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].object_name, "sensor")

    def test_splits_on_tab_keeping_commas_in_fields(self):
        content = "\n".join([HEADER, tsv_row(Description="a, b, c")])

        events = load_events(self._write(content))

        self.assertEqual(events[0].description, "a, b, c")

    def test_header_only_returns_empty_list(self):
        events = load_events(self._write(HEADER + "\n"))

        self.assertEqual(events, [])

    def test_short_row_yields_none_for_unreached_columns(self):
        short_row = "\t".join(["7", "2026-01-01 00:00:00", "Info", "sensor"])
        content = "\n".join([HEADER, short_row])

        events = load_events(self._write(content))

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_number, "7")
        self.assertEqual(events[0].object_name, "sensor")
        self.assertIsNone(events[0].object_id)
        self.assertIsNone(events[0].raw)

    def test_row_too_short_to_reach_severity_raises(self):
        content = "\n".join([HEADER, "1\t2026-01-01 00:00:00"])

        with self.assertRaises(ValueError):
            load_events(self._write(content))

    def test_invalid_severity_value_raises(self):
        content = "\n".join([HEADER, tsv_row(Severity="Critical")])

        with self.assertRaises(ValueError):
            load_events(self._write(content))

    def test_missing_required_column_raises(self):
        columns_without_object_name = [c for c in COLUMNS if c != "Object name"]
        header = "\t".join(columns_without_object_name)

        full_row = tsv_row(Severity="Info")
        values = dict(zip(COLUMNS, full_row.split("\t")))
        row = "\t".join(values[c] for c in columns_without_object_name)

        content = "\n".join([header, row])

        with self.assertRaises(KeyError):
            load_events(self._write(content))


if __name__ == "__main__":
    unittest.main()
