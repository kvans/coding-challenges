def flatten_json(obj: dict, sep: str = ".") -> dict:
    out: dict = {}

    def walk(value, prefix: str) -> None:
        if isinstance(value, dict) and value:
            for k, v in value.items():
                walk(v, f"{prefix}{sep}{k}" if prefix else str(k))
        elif isinstance(value, list) and value:
            for i, v in enumerate(value):
                walk(v, f"{prefix}{sep}{i}" if prefix else str(i))
        else:
            out[prefix] = value

    if not obj:
        return {}
    walk(obj, "")
    return out
