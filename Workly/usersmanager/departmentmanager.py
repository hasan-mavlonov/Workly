import hashlib
from Workly.queries.departmentqueries import (
    CREATE_DEPARTMENT,
    DELETE_DEPARTMENT,
    UPDATE_DEPARTMENT,
    READ_ALL_DEPARTMENTS,
    READ_DEPARTMENT_BY_NAME,
    CHECK_DEPARTMENT_PASSWORD
)
from Workly.database_config.db_settings import execute_query


class DepartmentManager:
    def __init__(self, department_name):
        self.department_name = department_name

    def check_department(self):
        params = (self.department_name,)
        result = execute_query(READ_DEPARTMENT_BY_NAME, params, fetch="one")
        return result[0] if result else False

    def create_department(self, password):
        """ Create a new department with a hashed password. """
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            params = (self.department_name, password,)
            result = execute_query(CREATE_DEPARTMENT, params, fetch="one")
            return result[0]  # Returns the ID of the newly created department
        except Exception as e:
            print(f"Failed to create department: {e}")
            return False

    def check_department_password(self, input_password):
        """ Check if the input password matches the stored hashed password for the department. """
        # Hash the input password
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()

        # Retrieve the stored hashed password from the database
        params = (self.department_name,)
        result = execute_query(CHECK_DEPARTMENT_PASSWORD, params, fetch="one")

        if result:
            stored_password = result[0]
            return hashed_input_password == stored_password
        else:
            print(f"Department '{self.department_name}' not found or no password stored.")
            return False

    def delete_department(self):
        """ Delete the department by name. """
        try:
            execute_query(DELETE_DEPARTMENT, (self.department_name,))
            # Check if the deletion was successful by counting affected rows
            # Since execute_query does not return affected rows count, this logic assumes success
            return True
        except Exception as e:
            print(f"Failed to delete department: {e}")
            return False

    @staticmethod
    def update_department(new_name):
        """ Edit the department name. """
        try:
            params = (new_name,)
            execute_query(UPDATE_DEPARTMENT, params)
            return True
        except Exception as e:
            print(f"Failed to update department: {e}")
            return False

    @staticmethod
    def print_all_departments():
        try:
            departments = execute_query(READ_ALL_DEPARTMENTS, fetch="all")
            if departments:
                for department in departments:
                    print(f"ID: {department['id']}, Department Name: {department['department_name']}")
            else:
                print("No departments found.")
        except Exception as e:
            print(f"Failed to retrieve departments: {e}")
