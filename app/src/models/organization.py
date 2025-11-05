from dataclasses import dataclass, fields
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Organization:
    id: Optional[int] = None
    name: Optional[str] = None
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

    @classmethod
    def validatePayload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return only valid Organization fields from the payload."""
        valid_fields = {f.name for f in fields(cls)}
        return {k: v for k, v in payload.items() if k in valid_fields}