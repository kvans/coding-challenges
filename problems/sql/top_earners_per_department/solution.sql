SELECT department, name, salary
FROM employees
WHERE salary IS NOT NULL
QUALIFY DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) <= 2
