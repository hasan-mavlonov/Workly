# Workly/queries/employeequeries.py

CREATE_EMPLOYEE = """
INSERT INTO employees (employee_name, department_name, password, start_of_the_day, end_of_the_day)
VALUES (%s, %s, %s, %s, %s)
RETURNING id;
"""

READ_EMPLOYEE_BY_ID = """
SELECT employee_name, department_name, start_of_the_day, end_of_the_day, password
FROM employees
WHERE id = %s;
"""

READ_ALL_EMPLOYEES = """
SELECT id, employee_name, department_name, start_of_the_day, end_of_the_day
FROM employees;
"""

READ_EMPLOYEES_BY_DEPARTMENT_NAME = """
SELECT id, employee_name, department_name, start_of_the_day, end_of_the_day
FROM employees
WHERE department_name = %s;
"""

UPDATE_EMPLOYEE = """
UPDATE employees 
SET employee_name = %s, department_name = %s, start_of_the_day = %s, end_of_the_day = %s, password = %s 
WHERE id = %s;
"""

DELETE_EMPLOYEE = """
DELETE FROM employees 
WHERE id = %s;
"""
