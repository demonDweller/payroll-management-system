from abc import ABC, abstractmethod


class Person(ABC):
    """Abstract base class for all persons in the system"""

    def __init__(self, name: str, emp_id: str):
        self._name = name
        self._emp_id = emp_id

    @property
    def name(self):
        return self._name

    @property
    def emp_id(self):
        return self._emp_id

    @abstractmethod
    def get_info(self) -> str:
        """Abstract method to get person information"""
        pass

    def __str__(self):
        return f"{self._name} (ID: {self._emp_id})"