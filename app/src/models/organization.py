from dataclasses import dataclass, asdict
from typing import Optional
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

    def viewDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "logo_url": self.logo_url,
            "website_url": self.website_url,
            "contact_email": self.contact_email,
            "category": self.category,
            "rating": self.rating,
            "vote_count": self.vote_count,
            "created_at": self.created_at
        }

@dataclass
class OrganizationQueryParams:
    q: Optional[str]
    id: Optional[list[int]]
    category: Optional[list[str]]
