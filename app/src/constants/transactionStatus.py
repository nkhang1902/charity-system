from enum import Enum

class TransactionStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    COMMITTED = "committed"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
