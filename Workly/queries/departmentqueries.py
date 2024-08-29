CREATE_DEPARTMENT = """
INSERT INTO departments (department_name, password) 
VALUES (%s, %s) RETURNING id;
"""


READ_DEPARTMENT_BY_NAME = """
SELECT * FROM departments WHERE department_name = %s;
"""

READ_ALL_DEPARTMENTS = """
SELECT * FROM departments;
"""

UPDATE_DEPARTMENT = """
UPDATE departments 
SET department_name = %s 
WHERE id = %s;
"""

DELETE_DEPARTMENT = """
DELETE FROM departments 
WHERE department_name = %s;
"""

CHECK_DEPARTMENT_PASSWORD = """
SELECT password 
FROM departments 
WHERE department_name = %s;
"""
