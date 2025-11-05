from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class Campaign:
    id: Optional[int] = None
    title: Optional[str] = None
    organization_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None
    goal_ammount: Optional[float] = None
    current_ammount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    media_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None