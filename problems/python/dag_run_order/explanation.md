**Idea:** Kahn's algorithm. Count each task's unfinished dependencies (in-degree), seed a min-heap with tasks whose count is zero, and repeatedly pop the smallest name, append it, and decrement its downstream tasks, pushing any that reach zero. If the output is shorter than the number of tasks, the remainder is a cycle.

**Complexity:** O((V + E) log V) because of the heap; O(V + E) with a plain queue when tie-breaking is not required.

**Talking points**
- The heap is what makes the schedule deterministic; real orchestrators use priority weights the same way.
- The DFS alternative (three-colour marking) also finds cycles and can report *which* tasks form it, which is nicer for error messages.
- Extensions interviewers like: maximum parallelism per "level" (BFS layers), critical path length (longest path in a DAG via DP over the topological order), and what to do when one task fails (prune its downstream subtree).
