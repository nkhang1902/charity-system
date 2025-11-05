from dataclasses import dataclass, fields
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Organization:
    id: int
    name: int
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    contact_email: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    vote_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None