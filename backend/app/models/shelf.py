from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Shelf(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, unique=True)


class BookShelf(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True)
    book_id: UUID = Field(primary_key=True)
    shelf_id: UUID
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BookShelfHistory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID
    book_id: UUID
    from_shelf_id: UUID | None = None
    to_shelf_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    note: str | None = None
