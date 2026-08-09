from pathlib import Path

from event_log import EventLog, load_events

if __name__ == "__main__":
    events = load_events(Path(__file__).parent / "event_log_sample.csv")
    log = EventLog(events)
    print(f"Loaded {len(events)} events")
