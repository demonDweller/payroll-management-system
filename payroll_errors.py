class PayrollSystemError(Exception):
    """Base exception for payroll system"""
    pass

class EmployeeNotFoundError(PayrollSystemError):
    """Raised when employee ID doesn't exist"""
    pass

class ClockInError(PayrollSystemError):
    """Raised when clock in operation fails"""
    pass

class ClockOutError(PayrollSystemError):
    """Raised when clock out operation fails"""
    pass

class PayrollError(PayrollSystemError):
    """Raised when payroll processing fails"""
    pass

class FileOperationError(PayrollSystemError):
    """Raised when file operations fail"""
    pass