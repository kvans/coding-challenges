**Idea:** after deduplicating to distinct days, number each user's days in order. For consecutive days both the date and the row number increase by one, so `login_date - row_number` stays constant inside a streak and jumps at every gap. Group by that value.

**Talking points**
- Skipping the `DISTINCT` step is the classic bug: duplicate days get different row numbers, which breaks the arithmetic.
- The alternative formulation uses `LAG`: flag a new island when `login_date - LAG(login_date) <> 1 day`, then a running `SUM` of flags gives the island id. It is the same technique used for sessionization.
- Streak length is `COUNT(*)` of distinct days, which equals `streak_end - streak_start + 1`; computing both is a cheap sanity check.
