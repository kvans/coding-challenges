import heapq


def pipeline_run_order(tasks: dict[str, list[str]]) -> list[str] | None:
    # Normalise: every mentioned task gets an entry.
    deps: dict[str, set[str]] = {}
    for task, upstream in tasks.items():
        deps.setdefault(task, set()).update(upstream)
        for u in upstream:
            deps.setdefault(u, set())

    downstream: dict[str, list[str]] = {t: [] for t in deps}
    indegree: dict[str, int] = {t: len(up) for t, up in deps.items()}
    for task, upstream in deps.items():
        for u in upstream:
            downstream[u].append(task)

    ready = [t for t, d in indegree.items() if d == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in downstream[task]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)

    return order if len(order) == len(deps) else None
