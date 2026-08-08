from enum import IntEnum


class EventSeverity(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls.__members__.get(value.strip().upper())
        return None
