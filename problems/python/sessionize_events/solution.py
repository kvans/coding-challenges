from datetime import datetime, timedelta

TS_FORMAT = "%Y-%m-%d %H:%M:%S"


def sessionize(events: list[dict], gap_minutes: int = 30) -> list[dict]:
    gap = timedelta(minutes=gap_minutes)
    by_user: dict[int, list[datetime]] = {}
    for e in events:
        by_user.setdefault(e["user_id"], []).append(datetime.strptime(e["ts"], TS_FORMAT))

    out: list[dict] = []
    for user_id in sorted(by_user):
        times = sorted(by_user[user_id])
        session_id = 0
        start = prev = None
        count = 0
        for t in times:
            if prev is None or t - prev > gap:
                if prev is not None:
                    out.append(_row(user_id, session_id, start, prev, count))
                session_id += 1
                start = t
                count = 0
            count += 1
            prev = t
        out.append(_row(user_id, session_id, start, prev, count))
    return out


def _row(user_id, session_id, start, end, count):
    return {
        "user_id": user_id,
        "session_id": session_id,
        "start": start.strftime(TS_FORMAT),
        "end": end.strftime(TS_FORMAT),
        "events": count,
    }
