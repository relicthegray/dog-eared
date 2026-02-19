from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class OwnedItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)

    title: str
    author: Optional[str] = None

    # "hardcover", "paperback", "ebook", "audiobook", "other"
    format: str = Field(default="hardcover", index=True)

    is_favorite: bool = Field(default=False, index=True)
    acquired_at: Optional[datetime] = None

    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
