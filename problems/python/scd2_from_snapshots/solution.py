META_COLUMNS = {"snapshot_date", "customer_id"}


def build_scd2(snapshots: list[dict]) -> list[dict]:
    ordered = sorted(snapshots, key=lambda r: (r["snapshot_date"], r["customer_id"]))
    history: dict = {}  # customer_id -> list of versions

    for row in ordered:
        cid = row["customer_id"]
        attrs = {k: v for k, v in row.items() if k not in META_COLUMNS}
        versions = history.setdefault(cid, [])
        if versions and versions[-1]["attrs"] == attrs:
            continue  # unchanged: nothing to do
        if versions:
            versions[-1]["valid_to"] = row["snapshot_date"]
            versions[-1]["is_current"] = False
        versions.append({"attrs": attrs, "valid_from": row["snapshot_date"], "valid_to": None, "is_current": True})

    out: list[dict] = []
    for cid in sorted(history):
        for v in history[cid]:
            record = {"customer_id": cid}
            record.update(v["attrs"])
            record.update(valid_from=v["valid_from"], valid_to=v["valid_to"], is_current=v["is_current"])
            out.append(record)
    return out
