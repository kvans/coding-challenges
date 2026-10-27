Semi-structured events land as nested JSON, but your warehouse table wants flat columns. Write `flatten_json(obj, sep=".")` that flattens a nested dict into a single-level dict.

Rules:

- Nested dict keys are joined with `sep`: `{"a": {"b": 1}}` becomes `{"a.b": 1}`.
- List elements are addressed by their index: `{"tags": ["x", "y"]}` becomes `{"tags.0": "x", "tags.1": "y"}`.
- Scalars (`str`, `int`, `float`, `bool`, `None`) are leaves.
- An **empty** dict or list is also a leaf and is kept as-is (`{"meta": {}}` stays `{"meta": {}}`), so no information is lost.
- Key order in the result does not matter. An empty input dict returns an empty dict.

### Example

```
Input:  {"id": 1, "user": {"name": "Ana", "address": {"city": "Lisbon"}}, "tags": ["a", "b"]}
Output: {"id": 1, "user.name": "Ana", "user.address.city": "Lisbon", "tags.0": "a", "tags.1": "b"}
```

### Why interviewers ask this

Flattening is step one of schema inference for JSON ingestion (think `json_normalize`). It checks recursion, handling of lists vs dicts, and whether you think about edge cases such as empty containers and `None`.
