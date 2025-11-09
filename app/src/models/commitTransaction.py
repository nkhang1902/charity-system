from dataclasses import dataclass
from typing import Optional
from app.src.constants.transactionStatus import TransactionStatus

@dataclass
class CommitTransaction:
    transaction_id: int
    amount: float
    status: TransactionStatus
    payment_ref: Optional[str] = None
    message: Optional[str] = None

