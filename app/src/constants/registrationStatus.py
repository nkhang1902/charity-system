from enum import Enum

class RegistrationStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    COMMITTED = "committed"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
