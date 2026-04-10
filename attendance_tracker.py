from datetime import datetime, timedelta
from models.shift import Shift
from models.employee import Employee
from pandas.core.internals.construction import to_arrays


class AttendanceTracker:
    """Manages employee clock in/out and attendance records"""

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.active_shifts = {} #emp_id -> Shift object
        self._load_shifts()

    def _load_shifts(self):
        shifts_data = self.file_handler.load_shifts()
        for shift_dict in shifts_data:
            shift = Shift.from_dict(shift_dict)
            # Don't load active shifts (they should have clock_out_time)
            if shift.is_complete():
                # We'll store completed shifts seperately if needed
                pass

    def _save_shifts(self, shifts_list):
        """Save shifts to file"""
        shifts_data = [shift.to_dict() for shift in shifts_list if shift.is_complete()]
        self.file_handler.save_shifts(shifts_data)

    def clock_in(self, employee: Employee) -> Shift:
        """Clock in an employee and create new shift"""
        if employee.is_clocked_in:
            raise Exception(f"Employee {employee.name} is already clocked in")

        #check for any active shift for this employee
        if employee.emp_id not in self.active_shifts:
            raise Exceptions(f"No active shift found for {employee.name}")

        shift = self.active_shifts[employee.emp_id]
        shift.clock_out()
        employee.clock_out()

        # Save completed shift
        all_shifts = self._get_all_shifts()
        all_shifts.append(shift)
        self._save_shifts(all_shifts)

        #Remove from active shifts
        del self.active_shifts[employee.emp_id]

        duration = shift.get_duration_hours()
        print(f"{employee.name} clocked out at {shift.clock_out_time.strftime('%H:%M:%S')}")
        print(f" Duration: {duartion:.2f} hours")
        return shift

    def get_employee_shifts(self, emp_id: str, days_back: int = 7) -> list:
        """Get shifts for an employee from last N days"""
        all_shifts = self._get_all_shifts()
        cutoff_date = datetime.now() - timedelta(days=days_back)

        employee_shifts = []
        for shift in all_shifts:
            if shift.emp_id == emp_id and shift.clock_in_time >= cutoff_date:
                employee_shifts.append(shift)

        return employee_shifts

    def calculate_hours_worked(self, emp_id: str, days_back: int = 7) -> float:
        """Calculate total hours worked in last N days"""
        shifts = self.get_employee_shifts(emp_id, days_back)
        total_hours = sum(shift.get_duration_hours() for shift in shifts if shift.is_complete())
        return total_hours

    def get_active_employees(self) -> list:
        """Get list of currently clocked in employee IDs"""
        return list(self.active_shifts.keys())
    
