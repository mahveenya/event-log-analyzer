# Event Log Analyzer

A small, dependency-free Python library for loading and analyzing event-log exports
from a hardware device. It parses the device's tab-separated log, models each row as a
typed `Event`, and exposes an `EventLog` for basic data collection: filtering by
severity, counting events per object, and computing the device error rate.

## Requirements

- Python 3.12+ (uses `typing.Self` and PEP 604 `X | None` syntax)
- No third-party dependencies — standard library only (`csv`, `enum`, `dataclasses`, `collections`)

## Project structure

```
event_log/
    __init__.py     # public API: EventSeverity, Event, load_events, EventLog
    severity.py     # EventSeverity — ordered enum with string parsing
    event.py        # Event — frozen dataclass for one log row
    loader.py       # load_events — reads the TSV file into Event objects
    log.py          # EventLog — analysis over a list of events
main.py             # example entry point
tests/              # unittest suite (no pytest required)
event_log_sample.csv
```

## Usage

Run the example against the bundled sample file:

```bash
python main.py
```

```
Loaded 280 events
```

Or use the API directly:

```python
from pathlib import Path
from event_log import EventLog, EventSeverity, load_events

events = load_events(Path("event_log_sample.csv"))
log = EventLog(events)

# Events at or above a severity (returns a new EventLog)
warnings_and_errors = log.filter_by_severity(EventSeverity.WARNING)

# How many events each object produced -> Counter{object_name: count}
per_object = log.count_by_object()

# Fraction of events that are errors, in [0.0, 1.0]
print(f"error rate: {log.error_rate:.2%}")
```

## API

### `EventSeverity`

An ordered `IntEnum`: `INFO < WARNING < ERROR`. Because it is ordered, severities can be
compared directly (`event.severity >= EventSeverity.WARNING`). It also parses the
severity strings found in the log — `EventSeverity("Error")` returns `EventSeverity.ERROR`
(case-insensitive); an unknown value raises `ValueError`.

### `Event`

A frozen dataclass representing one log row. Construct one from a raw CSV row dict with
`Event.from_row(row)`. Required fields (`event_number`, `timestamp`, `severity`,
`object_name`, `object_id`, `event_id`) come from the row directly; optional text fields
(`event_name`, `description`, `remedy`, `readable`, `raw`) default to `None` when absent.

### `load_events(path) -> list[Event]`

Reads the log file at `path` and returns a list of `Event` objects. Handles two file
quirks (see below): the optional `sep=` directive line and the tab delimiter.

### `EventLog`

Wraps a list of events and provides the analysis:

| Member | Description |
|--------|-------------|
| `filter_by_severity(min_severity)` | New `EventLog` with events at or above `min_severity`. |
| `count_by_object()` | `Counter` of object name → number of events. |
| `error_rate` | Property: fraction of events with `ERROR` severity (`0.0` for an empty log). |
| `events` | Property: a copy of the underlying events list. |

## The log file format

Despite the `.csv` extension, the export is **tab-separated**, not comma-separated. The
loader accounts for two details of the device's export:

- **`sep=` directive.** The file may begin with a `sep=\t` line (a spreadsheet hint).
  When present it is skipped so the real header row is used; when absent the loader
  rewinds and treats the first line as the header.
- **Tab delimiter.** Fields are split on tabs, so commas inside a field (e.g. a
  description) are preserved.

## Running the tests

The suite uses only the standard-library `unittest` — no pytest needed:

```bash
python -m unittest discover -s tests
```

It covers the loader (well-formed rows, the `sep=` directive, tab-splitting, and
malformed input such as unknown severities, missing columns, and short/long rows) and the
`EventLog` analysis methods.

## Design notes

- **No pandas / third-party CSV libraries**, per the exercise constraints.
- **Severities are ordered** via `IntEnum`, so `filter_by_severity` is a simple comparison.
- **Events are immutable** (`frozen=True`), making an `EventLog` safe to share and filter
  without surprise mutation.
- **Fail loud on structural problems.** A missing required column or an unknown severity
  raises rather than silently producing wrong data.
