import heapq
from typing import Iterator

_END = object()


def merge_sorted_streams(streams: list[Iterator[int]]) -> list[int]:
    heap: list[tuple[int, int]] = []
    for i, stream in enumerate(streams):
        first = next(stream, _END)
        if first is not _END:
            heap.append((first, i))
    heapq.heapify(heap)

    out: list[int] = []
    while heap:
        value, i = heapq.heappop(heap)
        out.append(value)
        nxt = next(streams[i], _END)
        if nxt is not _END:
            heapq.heappush(heap, (nxt, i))
    return out
