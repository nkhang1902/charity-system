from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class Campaign:
    id: int
    title: str
    org_id: int
    description: Optional[str] = None
    goal_amount: Optional[float] = None
    current_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    media_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None