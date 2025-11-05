from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    id: Optional[int] = None
    user_id: Optional[int] = None
    campaign_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    blockchain_hash: Optional[str] = None
    message: Optional[str] = None
    receipient: Optional[str] = None
    timestamp: Optional[datetime] = None
