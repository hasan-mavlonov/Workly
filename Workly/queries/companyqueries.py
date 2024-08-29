# queries/company_queries.py

CREATE_COMPANY = """
INSERT INTO companies (company_name, password) VALUES (%s, %s) RETURNING 1;
"""

READ_COMPANY_BY_ID = """
SELECT * FROM companies WHERE id = %s ;
"""

READ_COMPANY_BY_NAME = """
SELECT * FROM companies WHERE company_name = %s;
"""

READ_ALL_COMPANIES = """
SELECT * FROM companies;
"""

UPDATE_COMPANY = """
UPDATE companies SET company_name = %s WHERE id = %s;
"""

DELETE_COMPANY = """
DELETE FROM companies WHERE company_name = %s;
"""

CHECK_COMPANY_PASSWORD = """
SELECT password FROM companies WHERE company_name = %s;
"""