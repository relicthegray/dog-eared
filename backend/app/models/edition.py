from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Column, JSON


class Edition(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    book_id: UUID = Field(index=True)
    format: str = Field(default="unknown", index=True)  # hardcover/paperback/ebook/audiobook
    isbn13: Optional[str] = Field(default=None, index=True)
    isbn10: Optional[str] = Field(default=None, index=True)
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    cover_url: Optional[str] = None
    identifiers_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Copy(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    edition_id: UUID = Field(index=True)
    owner_user_id: UUID = Field(index=True)
    acquired_date: Optional[str] = None
    condition: Optional[str] = None
    signed: bool = False
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
