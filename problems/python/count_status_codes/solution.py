def count_status_codes(lines: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in lines:
        parts = line.split('"')
        if len(parts) < 3:
            continue  # no quoted request section
        after = parts[2].split()
        if not after:
            continue
        status = after[0]
        if len(status) != 3 or not status.isdigit():
            continue
        counts[status] = counts.get(status, 0) + 1
    return counts
