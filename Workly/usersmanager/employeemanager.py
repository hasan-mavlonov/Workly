import hashlib
from Workly.queries.employeequeries import (
    CREATE_EMPLOYEE,
    READ_EMPLOYEE_BY_ID,
    READ_ALL_EMPLOYEES,
    READ_EMPLOYEES_BY_DEPARTMENT_NAME,
    UPDATE_EMPLOYEE,
    DELETE_EMPLOYEE
)
from Workly.database_config.db_settings import execute_query
from datetime import datetime

class EmployeeManager:
    def __init__(self, employee_id=None, employee_name=None, department_name=None, password=None):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.department_name = department_name
        self.password = password

    def _hash_password(self, password):
        """ Hash the password using hashlib. """
        return hashlib.sha256(password.encode()).hexdigest()

    def _check_password(self, hashed_password, input_password):
        """ Check if the input password matches the stored hashed password. """
        return hashed_password == hashlib.sha256(input_password.encode()).hexdigest()

    def create_employee(self, start_of_the_day, end_of_the_day):
        """ Create a new employee with provided details. """
        try:
            if not self.password:
                raise ValueError("Password must be provided to create an employee.")

            hashed_password = self._hash_password(self.password)

            # Convert empty strings to None for timestamps
            start_of_the_day = start_of_the_day if start_of_the_day else None
            end_of_the_day = end_of_the_day if end_of_the_day else None

            params = (self.employee_name, self.department_name, hashed_password, start_of_the_day, end_of_the_day)
            result = execute_query(CREATE_EMPLOYEE, params, fetch="one")
            return result  # Returns the ID of the newly created employee
        except Exception as e:
            print(f"Failed to create employee: {e}")
            return None

    @staticmethod
    def read_employee(employee_id):
        """ Read details of a specific employee by ID. """
        try:
            params = (employee_id,)
            result = execute_query(READ_EMPLOYEE_BY_ID, params, fetch="one")
            return result
        except Exception as e:
            print(f"Failed to read employee: {e}")
            return None

    @staticmethod
    def read_all_employees():
        """ Read details of all employees. """
        try:
            result = execute_query(READ_ALL_EMPLOYEES, fetch="all")
            return result
        except Exception as e:
            print(f"Failed to read all employees: {e}")
            return []

    @staticmethod
    def read_employees_by_department(department_name):
        """ Read details of employees by department name. """
        try:
            params = (department_name,)
            result = execute_query(READ_EMPLOYEES_BY_DEPARTMENT_NAME, params, fetch="all")
            return result
        except Exception as e:
            print(f"Failed to read employees by department: {e}")
            return []

    @staticmethod
    def update_employee(employee_id, new_employee_name, new_department_name, new_password, new_start_of_the_day,
                        new_end_of_the_day):
        """ Update details of an existing employee. """
        try:
            hashed_password = EmployeeManager()._hash_password(new_password) if new_password else None
            params = (
                new_employee_name if new_employee_name else None,
                new_department_name if new_department_name else None,
                hashed_password,
                new_start_of_the_day if new_start_of_the_day else None,
                new_end_of_the_day if new_end_of_the_day else None,
                employee_id
            )
            execute_query(UPDATE_EMPLOYEE, params)
            return True
        except Exception as e:
            print(f"Failed to update employee: {e}")
            return False

    @staticmethod
    def delete_employee(employee_id):
        """ Delete an employee by ID. """
        try:
            params = (employee_id,)
            execute_query(DELETE_EMPLOYEE, params)
            return True
        except Exception as e:
            print(f"Failed to delete employee: {e}")
            return False

    def start_work(self, start_time):
        """ Mark the start time for the employee. """
        if not self.employee_id:
            print("Employee ID is required to start work.")
            return

        try:
            params = (start_time, self.employee_id)
            execute_query("UPDATE employees SET start_of_the_day = %s WHERE id = %s", params)
            print(f"Work started at {start_time}")
        except Exception as e:
            print(f"Failed to start work: {e}")

    def end_work(self, end_time):
        """ Mark the end time for the employee. """
        if not self.employee_id:
            print("Employee ID is required to end work.")
            return

        try:
            params = (end_time, self.employee_id)
            execute_query("UPDATE employees SET end_of_the_day = %s WHERE id = %s", params)
            print(f"Work ended at {end_time}")
        except Exception as e:
            print(f"Failed to end work: {e}")

    def show_statistics(self):
        """ Show statistics for the employee. """
        if not self.employee_id:
            print("Employee ID is required to show statistics.")
            return

        try:
            result = execute_query(
                "SELECT start_of_the_day, end_of_the_day FROM employees WHERE id = %s",
                (self.employee_id,),
                fetch="one"
            )
            if result:
                print(f"Start of the Day: {result['start_of_the_day']}")
                print(f"End of the Day: {result['end_of_the_day']}")
            else:
                print("No statistics found.")
        except Exception as e:
            print(f"Failed to show statistics: {e}")

    def show_my_data(self):
        """ Show employee's personal data. """
        if not self.employee_id:
            print("Employee ID is required to show data.")
            return

        try:
            result = execute_query(
                "SELECT employee_name, department_name, start_of_the_day, end_of_the_day FROM employees WHERE id = %s",
                (self.employee_id,),
                fetch="one"
            )
            if result:
                print(f"Name: {result['employee_name']}")
                print(f"Department: {result['department_name']}")
                print(f"Start of the Day: {result['start_of_the_day']}")
                print(f"End of the Day: {result['end_of_the_day']}")
            else:
                print("No data found.")
        except Exception as e:
            print(f"Failed to show personal data: {e}")

    @staticmethod
    def check_employee_password(employee_id, input_password):
        """ Check if the input password matches the stored hashed password for the employee. """
        try:
            # Ensure employee_id is an integer
            employee_id = int(employee_id)

            result = execute_query(
                "SELECT password FROM employees WHERE id = %s",
                (employee_id,),
                fetch="one"
            )
            if result:
                hashed_password = result['password']
                return EmployeeManager()._check_password(hashed_password, input_password)
            else:
                print(f"Employee with ID '{employee_id}' not found or no password stored.")
                return False
        except Exception as e:
            print(f"Failed to check employee password: {e}")
            return False

    @staticmethod
    def read_employee_by_name(employee_name):
        """ Read details of a specific employee by name. """
        try:
            params = (employee_name,)
            result = execute_query(
                "SELECT id, employee_name, department_name, password FROM employees WHERE employee_name = %s",
                params,
                fetch="one"
            )
            return result
        except Exception as e:
            print(f"Failed to read employee by name: {e}")
            return None

