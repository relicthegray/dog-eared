from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Column, JSON


class Source(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    type: str = Field(default="other", index=True)  # tiktok/family/friend/etc.
    name: str
    url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class IntakeItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    raw_text: str
    source_id: Optional[UUID] = Field(default=None, index=True)
    source_post_url: Optional[str] = None
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new", index=True)  # new/parsed/matched/needs_review/archived
    matched_book_id: Optional[UUID] = Field(default=None, index=True)
    match_confidence: Optional[float] = None
    parse_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
