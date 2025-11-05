from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserInteraction:
    id: int
    user_id: int
    target_type: str
    target_id: int
    action_type: str
    weight: Optional[int] = None
    timestamp: Optional[datetime] = None
