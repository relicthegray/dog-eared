from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models import Source, User

router = APIRouter()


class SourceCreateIn(BaseModel):
    type: str = "other"          # e.g. tiktok/family/friend/booktube/other
    name: str                    # display name, e.g. "Erin", "TikTok - @fantasyreads"
    url: str | None = None       # profile link if you want
    notes: str | None = None


class SourceOut(BaseModel):
    id: str
    type: str
    name: str
    url: str | None
    notes: str | None
    created_at: datetime


@router.get("", response_model=list[SourceOut])
def list_sources(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = (
        select(Source)
        .where(Source.user_id == user.id)
        .order_by(Source.created_at.desc())
    )
    rows = session.exec(stmt).all()
    return [
        SourceOut(
            id=str(s.id),
            type=s.type,
            name=s.name,
            url=s.url,
            notes=s.notes,
            created_at=s.created_at,
        )
        for s in rows
    ]


@router.post("", response_model=SourceOut)
def create_source(
    payload: SourceCreateIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    s = Source(
        user_id=user.id,
        type=(payload.type or "other").strip().lower(),
        name=payload.name.strip(),
        url=payload.url.strip() if payload.url else None,
        notes=payload.notes.strip() if payload.notes else None,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return SourceOut(
        id=str(s.id),
        type=s.type,
        name=s.name,
        url=s.url,
        notes=s.notes,
        created_at=s.created_at,
    )
