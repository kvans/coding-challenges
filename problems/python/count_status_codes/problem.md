You are given raw web-server access log lines in the common log format:

```
203.0.113.5 - - [10/Oct/2024:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 2326
```

Write `count_status_codes(lines)` that returns a dict mapping each **HTTP status code (as a string)** to the number of lines with that status.

Rules:

- The request is always enclosed in double quotes. The status code is the first token after the closing quote.
- A status code is valid only if it is exactly three digits. Lines that are malformed (no quoted request, missing or non-numeric status) must be skipped, not raised on.
- Return an empty dict for an empty input.

### Example

```
Input:
  '10.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET / HTTP/1.1" 200 512'
  '10.0.0.2 - - [10/Oct/2024:13:55:40 +0000] "GET /missing HTTP/1.1" 404 0'
  '10.0.0.1 - - [10/Oct/2024:13:56:01 +0000] "POST /login HTTP/1.1" 200 88'
  'garbage line'
Output: {"200": 2, "404": 1}
```

### Why interviewers ask this

Log parsing is the bread and butter of ingestion work. They want to see defensive parsing, a frequency map, and awareness that paths can contain spaces (so splitting the whole line on whitespace is fragile).
