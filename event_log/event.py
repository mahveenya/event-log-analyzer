from dataclasses import dataclass
from typing import Self

from event_log.severity import EventSeverity


@dataclass(frozen=True)
class Event:
    event_number: str
    timestamp: str
    severity: EventSeverity
    object_name: str
    object_id: str
    event_id: str
    event_name: str | None
    description: str | None
    remedy: str | None
    readable: str | None
    raw: str | None

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Self:
        return cls(
            event_number=row["Event number"],
            timestamp=row["Timestamp"],
            severity=EventSeverity(row["Severity"]),
            object_name=row["Object name"],
            object_id=row["Object ID"],
            event_id=row["Event ID"],
            event_name=row.get("Event name"),
            description=row.get("Description"),
            remedy=row.get("Remedy"),
            readable=row.get("Readable"),
            raw=row.get("Raw"),
        )
