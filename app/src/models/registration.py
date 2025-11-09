from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
from app.src.constants.registrationStatus import RegistrationStatus

@dataclass
class Registration:
    id: int
    type: Optional[str] = None
    org_id: Optional[int] = None
    payload: Optional[Dict[str, str]] = None
    status: RegistrationStatus = RegistrationStatus.NEW
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None