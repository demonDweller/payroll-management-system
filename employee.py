from models.person import Person

class Employee(Person):
    """Employee calss with role-based pay calculation"""

    #class variable for auto-generating IDs
    _id_counter = 1000

    def __init__(self, name: str, role: str, hourly_rate: float, emp_id: str = None):
        if emp_id is None:
            emp_id = str(Employee._id_counter)
            Employee._id_counter += 1
        super().__init__(name, emp_id)
        self.role = role
        self.hourly_rate =  hourly_rate
        self._is_clocked_in = False
        self._current_shift = None

    @property
    def role(self):
        return self._role

    @property
    def hourly_rate(self):
        return self.hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        if value <= 0:
            raise ValueError("Hourly rate must be positive")
        self.hourly_rate = value

    @property
    def is_clocked_in(self):
        return self._is_clocked_in

    def clock_in(self):
        """Mark employee as clocked in"""
        if self._is_clocked_in:
            raise Exception(f"Employee {self._name} is already clocked in")
        self._is_clocked_in = True

    def clock_out(self):
        """Mark employee as clocked out"""
        if not self._is_clocked_in:
            raise Exception(f"Employee {self._name} is not clocked in")
        self._is_clocked_in = False

    def calculate_pay(self, hours_worked: float) -> float:
        """
        calculate pay with overtime(1.5x afters 40 hours)
        can be overridden by subclasses for different role rules
        """
        if hours_worked <= 40:
            return hours_worked * self._hourly_rate
        else:
            regular_pay = 40 * self._hourly_rate
            overtime_hours = hours_worked - 40
            overtime_pay = overtime_hours * self._hourly_rate * 1.5
            return regular_pay + overtime_pay

    def get_info(self):
        return f"Employee : {self._name} | Role: {self._role} | Rate: ${self._hourly_rate}/hr"

    def to_dict(self) -> dict:
        """Convert employee to dictionary for csv storage"""
        return{
            'emp_id':self._emp_id,
            'name': self._name,
            'role':self._role,
            'hourly_rate': self._hourly_rate
        }

    @classmethod
    def from_dict (cls, data: dict):
        """Create employee from dictionary"""
        return cls(
            name=data['name'],
            role=data['role'],
            hourly_rate=float(data['hourly_rate']),
            emp_id=data['emp_id']
        )
