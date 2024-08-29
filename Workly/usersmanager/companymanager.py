import hashlib
from Workly.queries.companyqueries import CREATE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY, READ_COMPANY_BY_ID, \
    READ_ALL_COMPANIES, READ_COMPANY_BY_NAME, CHECK_COMPANY_PASSWORD
from Workly.database_config.db_settings import execute_query


class CompanyManager:
    def __init__(self, company_name):
        self.company_name = company_name

    def check_company(self):
        params = (self.company_name,)
        result = execute_query(READ_COMPANY_BY_NAME, params, fetch="one")
        return result[0] if result else False

    def create_company(self, password):
        # Assuming this method creates the company and stores the password
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            params = (self.company_name, password,)
            result = execute_query(CREATE_COMPANY, params, fetch="one")
            return result[0]  # Returns the ID of the newly created company
        except Exception as e:
            print(f"Failed to create company: {e}")
            return False

    def check_company_password(self, input_password):
        """ Check if the input password matches the stored hashed password for the company. """
        # Hash the input password
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()

        # Retrieve the stored hashed password from the database
        params = (self.company_name,)
        result = execute_query(CHECK_COMPANY_PASSWORD, params, fetch="one")

        if result:
            stored_password = result[0]
            return hashed_input_password == stored_password
        else:
            print(f"Company '{self.company_name}' not found or no password stored.")
            return False

    def delete_company(self):
        """ Delete the company by name. """
        try:
            execute_query(DELETE_COMPANY, (self.company_name,))
            # Check if the deletion was successful by counting affected rows
            # Since execute_query does not return affected rows count, this logic assumes success
            return True
        except Exception as e:
            print(f"Failed to delete company: {e}")
            return False
