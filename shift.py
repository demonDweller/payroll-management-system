from datetime import datetime
import json

class Shift:
    """Represents a single work shift"""
    def __init__(self, emp_id: str, clock_in_time: datetime = None):
        self._emp_id = emp_id
        self._clock_in_time = clock_in_time or datetime.now()
        self._clock_out_time = None

    @property
    def emp_id(self):
        return self._emp_id

    @property
    def clock_in_time(self):
        return self._clock_in_time

    @property
    def clock_out(self):
        """Record clock out time"""
        if self._clock_out_time:
            raise Exception("Shift already clocked out")
        self._clock_out_time = datetime.now()

        #validate that clock out is after clock in
        if self._clock_out_time <= self._clock_in_time:
            raise Exception("Clock out time must be after clock in time")

    def get_duration_hours(self) -> float:
        """Calculate shift duration in hours"""
        if not self._clock_out_time:
            return 0
        duration = self._clock_out_time - self._clock_in_time
        return duration.total_seconds() / 3600.0

    def is_complete(self) -> bool:
        """check if shift is completed"""
        return self._clock_in_time is not None

    def to_dict(self) -> dict:
        """Convert shift to dictionary for JSON storage"""
        return{
            'emp_id': self._emp_id,
            'clock_in_time': self._clock_in_time.isoformat(),
            'clock_out_time': self._clock_out_time.isoformat() if self._clock_out_time else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create shift from dictionary"""
        shift = cls(
            emp_id=data['emp_id'],
            clock_in_time = datetime.fromisoformat(data['clock_in_time'])
        )
        if data.get('clock_out_time'):
            shift._clock_out_time = datetime.fromisoformat(data['clock_out_time'])
        return shift

    def __str__(self):
        status = "Active" if not self._clock_out_time else "completed"
        duration = self.get_duration_hours() if self._clock_out_time else 0
        return f"Shift {self._emp_id}: {self._clock_in_time.strftime('%Y-%m-%d %H:%M')} - Duration: {duartion:.2f}h [{status}]"