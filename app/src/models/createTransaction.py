from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateTransaction:
    user_id: int
    campaign_id: int
    amount: float
    message: Optional[str] = None
