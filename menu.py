import sys
from models.employee import Employee
from services.attendance_tracker import AttendanceTracker
from services.payroll_processor import WeeklyPayroll
from services.file_handler import FileHandler
from exceptions.payroll_errors import *


class CLIMenu:
    """Command-line interface menu system"""

    def __init__(self):
        self.file_handler = FileHandler()
        self.attendance_tracker = AttendanceTracker(self.file_handler)
        self.payroll_processor = WeeklyPayroll(self.file_handler)
        self.employees = {}  # emp_id -> Employee object
        self._load_employees()

    def _load_employees(self):
        """Load employees from file"""
        employees_data = self.file_handler.load_employees()

        # Update ID counter to avoid collisions
        max_id = 1000
        for emp_data in employees_data:
            emp_id = int(emp_data['emp_id'])
            if emp_id >= max_id:
                max_id = emp_id + 1
            employee = Employee.from_dict(emp_data)
            self.employees[emp_data['emp_id']] = employee

        Employee._id_counter = max_id

    def _save_employees(self):
        """Save employees to file"""
        employees_data = [emp.to_dict() for emp in self.employees.values()]
        self.file_handler.save_employees(employees_data)

    def _get_employee_by_id(self, emp_id):
        """Get employee object by ID with error handling"""
        if emp_id not in self.employees:
            raise EmployeeNotFoundError(f"Employee ID {emp_id} not found")
        return self.employees[emp_id]

    def display_main_menu(self):
        """Display main menu and handle user input"""
        while True:
            print("\n" + "=" * 50)
            print("   EMPLOYEE PAYROLL MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. Employee Management")
            print("2. Clock In/Out")
            print("3. Process Payroll")
            print("4. View Reports")
            print("5. Exit")
            print("=" * 50)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                self.employee_management_menu()
            elif choice == '2':
                self.clock_menu()
            elif choice == '3':
                self.process_payroll_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                print("\n✅ Saving data and exiting...")
                self._save_employees()
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please try again.")

    def employee_management_menu(self):
        """Employee management submenu"""
        while True:
            print("\n--- Employee Management ---")
            print("1. Add Employee")
            print("2. List All Employees")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. Back to Main Menu")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.list_employees()
            elif choice == '3':
                self.update_employee()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice")

    def add_employee(self):
        """Add a new employee"""
        print("\n--- Add New Employee ---")
        name = input("Name: ").strip()
        if not name:
            print("❌ Name cannot be empty")
            return

        role = input("Role (Manager/Cashier/Cleaner/Stocker): ").strip().capitalize()
        valid_roles = ['Manager', 'Cashier', 'Cleaner', 'Stocker']
        if role not in valid_roles:
            print(f"❌ Invalid role. Choose from: {', '.join(valid_roles)}")
            return

        try:
            hourly_rate = float(input("Hourly Rate ($): ").strip())
            if hourly_rate <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid hourly rate. Must be a positive number.")
            return

        employee = Employee(name, role, hourly_rate)
        self.employees[employee.emp_id] = employee
        self._save_employees()

        print(f"\n✅ Employee added successfully!")
        print(f"   ID: {employee.emp_id}")
        print(f"   Name: {employee.name}")
        print(f"   Role: {employee.role}")
        print(f"   Rate: ${employee.hourly_rate:.2f}/hr")

    def list_employees(self):
        """List all employees"""
        if not self.employees:
            print("\n📋 No employees found.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<8} {'Name':<20} {'Role':<15} {'Hourly Rate':<12} {'Status':<10}")
        print("=" * 70)

        for emp_id, emp in self.employees.items():
            status = "🟢 Clocked In" if emp.is_clocked_in else "⚪ Clocked Out"
            print(f"{emp_id:<8} {emp.name:<20} {emp.role:<15} ${emp.hourly_rate:<11.2f} {status:<10}")

        print("=" * 70)
        print(f"Total Employees: {len(self.employees)}")

    def update_employee(self):
        """Update employee information"""
        self.list_employees()
        emp_id = input("\nEnter Employee ID to update: ").strip()

        try:
            employee = self._get_employee_by_id(emp_id)
        except EmployeeNotFoundError as e:
            print(f"❌ {e}")
            return

        print(f"\nUpdating employee: {employee.name}")
        print(f"Current Role: {employee.role}")
        print(f"Current Rate: ${employee.hourly_rate:.2f}")

        new_role = input("New Role (press Enter to keep current): ").strip()
        if new_role:
            employee._role = new_role.capitalize()

        try:
            new_rate = input("New Hourly Rate (press Enter to keep current): ").strip()
            if new_rate:
                employee.hourly_rate = float(new_rate)
        except ValueError:
            print("❌ Invalid rate. Keeping current rate.")

        self._save_employees()
        print(f"\n✅ Employee {employee.name} updated successfully!")

    def delete_employee(self):
        """Delete an employee"""
        self.list_employees()
        emp_id = input("\nEnter Employee ID to delete: ").strip()

        try:
            employee = self._get_employee_by_id(emp_id)
        except EmployeeNotFoundError as e:
            print(f"❌ {e}")
            return

        confirm = input(f"\n⚠️  Delete {employee.name} (ID: {emp_id})? (y/N): ").strip().lower()
        if confirm == 'y':
            del self.employees[emp_id]
            self._save_employees()
            print(f"✅ Employee {employee.name} deleted successfully!")
        else:
            print("❌ Deletion cancelled.")

    def clock_menu(self):
        """Clock in/out menu"""
        while True:
            print("\n--- Clock In/Out ---")
            print("1. Clock In")
            print("2. Clock Out")
            print("3. View Active Employees")
            print("4. Back to Main Menu")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                self.clock_in()
            elif choice == '2':
                self.clock_out()
            elif choice == '3':
                self.view_active_employees()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice")

    def clock_in(self):
        """Clock in an employee"""
        emp_id = input("Enter Employee ID: ").strip()

        try:
            employee = self._get_employee_by_id(emp_id)
            self.attendance_tracker.clock_in(employee)
            self._save_employees()
        except (EmployeeNotFoundError, ClockInError, Exception) as e:
            print(f"❌ {e}")

    def clock_out(self):
        """Clock out an employee"""
        emp_id = input("Enter Employee ID: ").strip()

        try:
            employee = self._get_employee_by_id(emp_id)
            self.attendance_tracker.clock_out(employee)
            self._save_employees()
        except (EmployeeNotFoundError, ClockOutError, Exception) as e:
            print(f"❌ {e}")

    def view_active_employees(self):
        """View all currently clocked in employees"""
        active_ids = self.attendance_tracker.get_active_employees()

        if not active_ids:
            print("\n📋 No employees currently clocked in.")
            return

        print("\n🟢 Currently Clocked In:")
        print("-" * 40)
        for emp_id in active_ids:
            if emp_id in self.employees:
                emp = self.employees[emp_id]
                print(f"  {emp_id}: {emp.name} ({emp.role})")

    def process_payroll_menu(self):
        """Process payroll for the week"""
        print("\n--- Process Payroll ---")
        print("Processing payroll for current week (Monday - Sunday)...")

        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Payroll cancelled.")
            return

        try:
            payroll_data = self.payroll_processor.process(self.employees, self.attendance_tracker)

            if not payroll_data:
                print("\n⚠️  No hours recorded for this week.")
            else:
                print("\n✅ Payroll processed and saved to payroll_logs.txt")
        except PayrollError as e:
            print(f"❌ Payroll error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def reports_menu(self):
        """View reports menu"""
        while True:
            print("\n--- Reports ---")
            print("1. View Payroll Logs")
            print("2. Employee Hours Summary")
            print("3. Back to Main Menu")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                self.view_payroll_logs()
            elif choice == '2':
                self.view_hours_summary()
            elif choice == '3':
                break
            else:
                print("❌ Invalid choice")

    def view_payroll_logs(self):
        """Display payroll logs"""
        logs = self.file_handler.read_payroll_logs()
        print("\n" + "=" * 80)
        print("PAYROLL LOGS")
        print("=" * 80)
        print(logs)
        input("\nPress Enter to continue...")

    def view_hours_summary(self):
        """Display hours worked summary for all employees"""
        print("\n--- Hours Summary (Last 7 Days) ---")
        print("=" * 60)
        print(f"{'ID':<8} {'Name':<20} {'Hours Worked':<15}")
        print("=" * 60)

        for emp_id, employee in self.employees.items():
            hours = self.attendance_tracker.calculate_hours_worked(emp_id, days_back=7)
            print(f"{emp_id:<8} {employee.name:<20} {hours:<15.2f}")

        print("=" * 60)
        input("\nPress Enter to continue...")