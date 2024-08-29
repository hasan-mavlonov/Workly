from usersmanager.departmentmanager import DepartmentManager
from usersmanager.companymanager import CompanyManager
from usersmanager.employeemanager import EmployeeManager


def department_menu() -> None:
    """Department menu"""
    text = """
    1. Create a department
    2. See all departments
    3. Edit a department
    4. Delete a department
    5. Exit
    """
    user_input = input(text)
    if user_input == '1':
        department_name = input('Enter department name: ')
        department = DepartmentManager(department_name)
        if not department.check_department():
            password = input('Enter department password: ')
            verify_password = input('Verify the password: ')
            if password == verify_password:
                if department.create_department(password):
                    print("Successfully created a department")
                else:
                    print("Failed to create a department")
            else:
                print("Passwords do not match")
        else:
            print("The department already exists")
    elif user_input == '2':
        DepartmentManager.print_all_departments()
        department_menu()
    elif user_input == '3':
        department_name = input('Enter department name: ')
        department = DepartmentManager(department_name)
        if department.check_department():
            new_name = input("Enter new department name: ")
            if department.update_department(new_name):
                print("Successfully updated a department")
            else:
                print("Failed to update a department")
        else:
            print("The department does not exist")
    elif user_input == '4':
        department_name = input('Enter department name: ')
        department = DepartmentManager(department_name)
        if department.delete_department():
            print("Successfully deleted a department")
        else:
            print("Failed to delete a department")
    elif user_input == '5':
        company_menu()
    else:
        print("Invalid input")
        department_menu()


def employee_menu() -> None:
    """ Employee Menu """
    while True:
        text = """
        1. Create an employee
        2. See all employees
        3. Edit an employee
        4. Delete an employee
        5. Exit
        """
        user_input = input(text)

        if user_input == '1':
            employee_name = input('Enter employee name: ')
            department_name = input('Enter department name: ')
            password = input('Enter password: ')
            start_of_the_day = input('Enter start of the day (YYYY-MM-DD HH:MM:SS): ')
            end_of_the_day = input('Enter end of the day (YYYY-MM-DD HH:MM:SS): ')

            # Create Employee
            manager = EmployeeManager(
                employee_name=employee_name,
                department_name=department_name,
                password=password
            )
            result = manager.create_employee(start_of_the_day, end_of_the_day)
            if result:
                print(f"Employee created with ID: {result}")
            else:
                print("Failed to create employee.")


        elif user_input == '2':
            # See All Employees
            manager = EmployeeManager()
            employees = manager.read_all_employees()
            if employees:
                for emp in employees:
                    print(
                        f"ID: {emp['id']}, Name: {emp['employee_name']}, Department: {emp['department_name']}, Start: {emp['start_of_the_day']}, End: {emp['end_of_the_day']}")
            else:
                print("No employees found.")

        elif user_input == '3':
            employee_id = input('Enter employee ID: ')
            new_employee_name = input('Enter new employee name (leave blank to keep current): ')
            new_department_name = input('Enter new department name (leave blank to keep current): ')
            new_password = input('Enter new password (leave blank to keep current): ')
            new_start_of_the_day = input('Enter new start of the day (leave blank to keep current): ')
            new_end_of_the_day = input('Enter new end of the day (leave blank to keep current): ')

            # Update Employee
            manager = EmployeeManager()
            success = manager.update_employee(
                employee_id,
                new_employee_name if new_employee_name else None,
                new_department_name if new_department_name else None,
                new_password if new_password else None,
                new_start_of_the_day if new_start_of_the_day else None,
                new_end_of_the_day if new_end_of_the_day else None
            )
            if success:
                print("Employee updated successfully.")
            else:
                print("Failed to update employee.")

        elif user_input == '4':
            employee_id = input('Enter employee ID: ')

            # Delete Employee
            manager = EmployeeManager()
            success = manager.delete_employee(employee_id)
            if success:
                print("Employee deleted successfully.")
            else:
                print("Failed to delete employee.")

        elif user_input == '5':
            print("Exiting...")
            auth_menu()

        else:
            print("Invalid option. Please try again.")
            employee_menu()

def employees_menu(employee_id: int) -> None:
    """ Employee Menu """
    while True:
        text = """
        1. Start work
        2. End work
        3. Show statistics
        4. Show my data
        5. Logout
        """
        user_input = input(text)

        manager = EmployeeManager(employee_id=employee_id)

        if user_input == '1':
            start_time = input('Enter start time (YYYY-MM-DD HH:MM:SS): ')
            manager.start_work(start_time)

        elif user_input == '2':
            end_time = input('Enter end time (YYYY-MM-DD HH:MM:SS): ')
            manager.end_work(end_time)

        elif user_input == '3':
            manager.show_statistics()

        elif user_input == '4':
            manager.show_my_data()

        elif user_input == '5':
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


def company_menu() -> None:
    text = """
    1. Manage departments | CRUD
    2. Manage employees | CRUD
    3. Show statistics
    4. Logout"""
    user_input = input(text)
    if user_input == '1':
        department_menu()
    elif user_input == '2':
        employee_menu()
    elif user_input == '3':
        pass


def super_admin_menu() -> None:
    """ Super Admin Menu """
    text = """
    1. Create a company: 
    2. Delete a company:
    3. Exit.
    """
    user_input = input(text)
    if user_input == '1':
        company_name = input('Enter company name: ')
        if not CompanyManager(company_name).check_company():
            password = input('Enter company password: ')
            verify_password = input('Enter company verify password: ')
            if password == verify_password:
                if CompanyManager(company_name).create_company(password) == 1:
                    print('Company created successfully.')
        else:
            print('Company already exists.')
        super_admin_menu()
    elif user_input == '2':
        company_name = input('Enter company name: ')
        if not CompanyManager(company_name).check_company():
            print("Such company doesn\'t exist!")
        elif CompanyManager(company_name).delete_company():
            print('Company deleted successfully.')
        super_admin_menu()
    elif user_input == '3':
        auth_menu()


def auth_menu() -> None:
    """ Menu where users authorize the application """
    text = """
    1. Login
    2. Exit
    """
    user_input = input(text)
    if user_input == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if the user is a super admin
        if username == 'super' and password == 'super':
            super_admin_menu()

        # Check if the user is a company
        elif CompanyManager(username).check_company_password(password):
            company_menu()

        # Check if the user is an employee
        else:
            employee = EmployeeManager()
            employee_data = employee.read_employee_by_name(username)  # Retrieve employee data by name

            if employee_data:
                employee_id = employee_data['id']
                if EmployeeManager.check_employee_password(employee_id, password):
                    employees_menu(employee_id)
                else:
                    print("Invalid username or password.")
            else:
                print("Employee not found.")

    elif user_input == '2':
        print("Exiting...")
        quit()


if __name__ == '__main__':
    auth_menu()
