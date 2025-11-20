from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class UpdateCampaign:
    id: int
    title:  Optional[str] = None
    description: Optional[str] = None
    goal_amount: Optional[float] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    media_url: Optional[str] = None

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
