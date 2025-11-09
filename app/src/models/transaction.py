from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.src.constants.transactionStatus import TransactionStatus

@dataclass
class Transaction:
    user_id: int
    campaign_id: int
    amount: int
    status: TransactionStatus = TransactionStatus.NEW
    id: Optional[int] = None
    blockchain_hash: Optional[str] = None
    message: Optional[str] = None
    receipt_url: Optional[str] = None
    timestamp: Optional[datetime] = None

    def viewDict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "campaign_id": self.campaign_id,
            "amount": self.amount,
            "status": self.status,
            "message": self.message,
            "timestamp": self.timestamp,
        }

@dataclass
class TransactionQueryParams:
    user_id: Optional[list[int]]
    campaign_id: Optional[list[int]]
    status: Optional[list[str]]
    min_amount: Optional[int]
    max_amount: Optional[int]
    from_timestamp: Optional[datetime]
    to_timestamp: Optional[datetime]
    timestamp: Optional[datetime] = None
