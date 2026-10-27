import heapq
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    # heapq.nsmallest with key (-count, value) is O(m log k) and keeps the tie rule.
    return heapq.nsmallest(k, counts, key=lambda v: (-counts[v], v))
