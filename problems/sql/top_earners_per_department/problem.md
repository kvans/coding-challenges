**employees**

| column | type |
|---|---|
| employee_id | INTEGER |
| name | VARCHAR |
| department | VARCHAR |
| salary | INTEGER (NULL if unknown) |

For each department return the employees earning one of the **two highest salary values** in that department. Everyone who ties on a qualifying salary is included. Employees with a NULL salary are ignored.

Output columns: `department`, `name`, `salary`. Row order does not matter.

### Example

| department | name | salary |
|---|---|---|
| Eng | A | 200 |
| Eng | B | 180 |
| Sales | D | 90 |
| Sales | E | 90 |
| Sales | F | 80 |

Sales keeps three people: D and E share the top salary (rank 1) and F has the second-highest value (rank 2).

### Why interviewers ask this

"Top N per group" is the second most common window question after "latest row per key". The whole question is which ranking function you pick and whether you can explain the difference between `ROW_NUMBER`, `RANK` and `DENSE_RANK`.
