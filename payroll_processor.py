from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class PayrollProcessor(ABC):
    """Abstract interface for payroll processing"""

    @abstractmethod
    def process(self, employees, attendance_tracker, week_start_date=None):
        pass

    @abstractmethod
    def generate_report(self, payroll_data):
        pass

class WeeklyPayroll(PayrollProcessor):
    """Concrete implementation for weekly payroll processing"""

    def __init__(self, file_handler):
        self.file_handler = file_handler

    def process(self, employees, attendance_tracker, week_start_date=None):
        """
        Process payroll for all employees for a given week
        Returns dictionary of employee_id -> payroll details
        """
        if week_start_date is None:
            # Default to current week (Monday to Sunday)
            today = datetime.now()
            week_start_date = today - timedelta(days=today.weekday())

        week_end_date = week_start_date + timedelta(days=6)

        payroll_data = {}

        for emp_id, employee in employees.items():
            # Get shifts for this week
            shifts = attendance_tracker.get_employee_shifts(emp_id, days_back=7)

            #filter shifts withtin the week
            week_shifts = [
                shift for shift in shifts
                if shift .is_complete() and
                week_start_date <= shift.clock_in_time <= week_end_date + timedelta(days=1)
            ]

            # Calculate total hours
            total_hours = sum(shift.get_duration_hours() for shift in week_shifts)

            if total_hours > 0:
                # Calculate pay using employee's method (Polymorphism)
                gross_pay = employee.calculate_pay(total_hours)

                # Simple tac calculation (20%)
                tax = gross_pay * 0.20
                net_pay = gross_pay - tax

                payroll_data[emp_id] = {
                    'employee': employee,
                    'hours': total_hours,
                    'gross_pay': gross_pay,
                    'tax': tax,
                    'net_pay': net_pay,
                    'week_start': week_start_date.strftime('%Y-%m-%d'),
                    'week_end': week_end_date.strftime('%Y-%m-%d')
                }

        # Generate and save report
        self.generate_report(payroll_data)

        return payroll_data

    def generate_report(self, payroll_data):
        """Generate formatted payroll report and save to log"""
        if not payroll_data:
            log_entry = "No payroll data to process"
            self.file_handler.append_payroll_log(log_entry)
            print(log_entry)
            return

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("PAYROLL REPORT")
        report_lines.append("="*80)

        total_payroll = 0
        total_tax = 0

        for emp_id, data in payroll_data.items():
            emp = data['employee']
            report_lines.append(f"\nEmployee: {emp.name} (ID: {emp_id})")
            report_lines.append(f"  Role: {emp.role}")
            report_lines.append(f"  Hours Worked: {data['hours']:.2f}")
            report_lines.append(f"  Hourly Rate: ${emp.hourly_rate:.2f}")
            report_lines.append(f"  Gross Pay: ${data['gross_pay']:.2f}")
            report_lines.append(f"  Tax (20%): ${data['tax']:.2f}")
            report_lines.append(f"  Net Pay: ${data['net_pay']:.2f}")
            report_lines.append(f"  Period: {data['week_start']} to {data['week_end']}")

            total_payroll += data['net_pay']
            total_tax += data['tax']

        report_lines.append("\n" + "=" * 80)
        report_lines.append(f"SUMMARY")
        report_lines.append(f"  Total Net Payroll: ${total_payroll:.2f}")
        report_lines.append(f"  Total Tax Collected: ${total_tax:.2f}")
        report_lines.append("=" * 80)

        report = "\n".join(report_lines)

        # Save to log file
        self.file_handler.append_payroll_log(report)

        # Print to console
        print(report)