from datetime import datetime, timedelta

TS_FORMAT = "%Y-%m-%d %H:%M:%S"


def sessionize(events: list[dict], gap_minutes: int = 30) -> list[dict]:
    """Group each user's events into sessions separated by gaps > gap_minutes."""
    pass
