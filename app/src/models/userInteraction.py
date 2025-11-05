from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserInteraction:
    id: Optional[int] = None
    user_id: Optional[int] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    action_type: Optional[str] = None
    weight: Optional[int] = None
    timestamp: Optional[datetime] = None
