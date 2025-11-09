from enum import Enum

class TransactionStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    COMMITTED = "committed"
    UNCOMMITTED = "uncommitted"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
