from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Optional

class User(Document):
  google_id: str = Field(..., unique=True)
  email: EmailStr = Field(..., unique=True)
  full_name: str
  avatar: Optional[str] = None
  role: str = Field(default="user")
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  class Settings:
    name = "users"