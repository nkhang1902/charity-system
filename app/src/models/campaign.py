from dataclasses import dataclass, asdict
from typing import Optional
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

    def viewDict(self):
        fields = ["id", "title", "org_id", "description", "goal_amount", "current_amount", "start_date", "end_date", "status", "media_url", "created_at"]
        data = asdict(self)
        return {k: data[k] for k in fields if k in data}

@dataclass
class CampaignQueryParams:
    q: Optional[str]
    id: Optional[list[int]]
    org_id: Optional[list[int]]
    status: Optional[list[str]]
