def hash_join(left: list[dict], right: list[dict], on: str, how: str = "inner") -> list[dict]:
    if how not in ("inner", "left"):
        raise ValueError(f"unsupported how={how!r}")

    # Build phase: index the right side; also collect the right-side column set.
    index: dict = {}
    right_cols: list[str] = []
    seen_cols: set[str] = set()
    for row in right:
        for col in row:
            if col != on and col not in seen_cols:
                seen_cols.add(col)
                right_cols.append(col)
        key = row.get(on)
        if key is None:
            continue  # NULL never matches
        index.setdefault(key, []).append(row)

    # Probe phase: stream the left side in order.
    out: list[dict] = []
    for lrow in left:
        key = lrow.get(on)
        matches = index.get(key, []) if key is not None else []
        if matches:
            for rrow in matches:
                merged = dict(lrow)
                merged.update({c: v for c, v in rrow.items() if c != on})
                out.append(merged)
        elif how == "left":
            merged = dict(lrow)
            merged.update({c: None for c in right_cols})
            out.append(merged)
    return out
