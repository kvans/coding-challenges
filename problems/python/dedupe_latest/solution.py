def dedupe_latest(records: list[dict], key: str, ts_field: str) -> list[dict]:
    latest: dict = {}
    for record in records:
        k = record[key]
        current = latest.get(k)
        if current is None or record[ts_field] >= current[ts_field]:
            latest[k] = record
    return [latest[k] for k in sorted(latest)]
