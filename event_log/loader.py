import csv
from event_log import Event


def load_events(path):
    with open(path, newline="", encoding="utf-8") as f:
        first = f.readline()
        if not first.lower().startswith("sep="):
            f.seek(0)
        reader = csv.DictReader(f, delimiter="\t")
        return [Event.from_row(row) for row in reader]
