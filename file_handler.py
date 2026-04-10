import csv
import json
import os
from datetime import datetime


class FileHandler:
    """Handles all file operations for the system"""

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    # Employee CSV Operations
    def save_employees(self, employees: list):
        """Save list of employee dicts to CSV"""
        filepath = os.path.join(self.data_dir, 'employees.csv')

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            if employees:
                fieldnames = ['emp_id', 'name', 'role', 'hourly_rate']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(employees)

    def load_employees(self) -> list:
        """Load employees from CSV, return list of dicts"""
        filepath = os.path.join(self.data_dir, 'employees.csv')

        if not os.path.exists(filepath):
            return []

        employees = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employees.append(row)
        except Exception as e:
            print(f"Error loading employees: {e}")
            return []

        return employees

    # Shift JSON Operations
    def save_shifts(self, shifts: list):
        """Save shifts list to JSON file"""
        filepath = os.path.join(self.data_dir, 'shifts.json')

        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(shifts, file, indent=2)
        except Exception as e:
            print(f"Error saving shifts: {e}")

    def load_shifts(self) -> list:
        """Load shifts from JSON file"""
        filepath = os.path.join(self.data_dir, 'shifts.json')

        if not os.path.exists(filepath):
            return []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:  # Fixed: Changed from JSONDecoderError
            return []
        except Exception as e:
            print(f"Error loading shifts: {e}")
            return []

    # Payroll Log Operations
    def append_payroll_log(self, log_entry: str):
        """Append a log entry to payroll_logs.txt"""
        filepath = os.path.join(self.data_dir, 'payroll_logs.txt')

        try:
            with open(filepath, 'a', encoding='utf-8') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"[{timestamp}] {log_entry}\n")
        except Exception as e:
            print(f"Error writing to log: {e}")

    def read_payroll_logs(self) -> str:
        """Read all payroll logs"""
        filepath = os.path.join(self.data_dir, 'payroll_logs.txt')

        if not os.path.exists(filepath):
            return "No payroll logs found."

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading logs: {e}"