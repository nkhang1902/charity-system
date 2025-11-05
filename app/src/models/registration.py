from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class Registration:
    id: int
    type: Optional[str] = None
    org_id: Optional[int] = None
    payload: Optional[Dict[str, str]] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None