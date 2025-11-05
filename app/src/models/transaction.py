from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    id: int
    user_id: int
    campaign_id: int
    amount: int
    status: Optional[str] = None
    blockchain_hash: Optional[str] = None
    message: Optional[str] = None
    receipt_url: Optional[str] = None
    timestamp: Optional[datetime] = None
