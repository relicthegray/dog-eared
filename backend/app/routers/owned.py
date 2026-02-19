from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models import OwnedItem, User
from app.models import IntakeItem  # add to imports at top if not present

router = APIRouter()


class OwnedCreateIn(BaseModel):
    title: str
    author: str | None = None
    format: str = "hardcover"
    is_favorite: bool = False
    acquired_at: datetime | None = None
    notes: str | None = None


class OwnedOut(BaseModel):
    id: str
    title: str
    author: str | None
    format: str
    is_favorite: bool
    acquired_at: datetime | None
    notes: str | None
    created_at: datetime


@router.get("", response_model=list[OwnedOut])
def list_owned(
    format: str | None = None,
    favorite: bool | None = None,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = select(OwnedItem).where(OwnedItem.user_id == user.id)

    if format:
        stmt = stmt.where(OwnedItem.format == format)
    if favorite is not None:
        stmt = stmt.where(OwnedItem.is_favorite == favorite)

    stmt = stmt.order_by(OwnedItem.created_at.desc())
    rows = session.exec(stmt).all()

    return [
        OwnedOut(
            id=str(o.id),
            title=o.title,
            author=o.author,
            format=o.format,
            is_favorite=o.is_favorite,
            acquired_at=o.acquired_at,
            notes=o.notes,
            created_at=o.created_at,
        )
        for o in rows
    ]


@router.post("/from-intake/{intake_id}", response_model=OwnedOut)
def create_owned_from_intake(
    intake_id: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    intake = session.exec(
        select(IntakeItem).where(IntakeItem.id == intake_id, IntakeItem.user_id == user.id)
    ).first()
    if not intake:
        raise HTTPException(status_code=404, detail="Intake item not found")

    # naive parse: "Title by Author" if present; else whole text is title
    raw = (intake.raw_text or "").strip()
    title = raw
    author = None
    if " by " in raw:
        parts = raw.split(" by ", 1)
        if parts[0].strip():
            title = parts[0].strip()
        if parts[1].strip():
            author = parts[1].strip()

    o = OwnedItem(
        user_id=user.id,
        title=title,
        author=author,
        format="hardcover",
        is_favorite=False,
        notes=f"Imported from Inbox: {intake.id}",
    )
    session.add(o)

    # Mark the intake item as processed (optional but recommended)
    intake.status = "owned"
    session.add(intake)

    session.commit()
    session.refresh(o)

    return OwnedOut(
        id=str(o.id),
        title=o.title,
        author=o.author,
        format=o.format,
        is_favorite=o.is_favorite,
        acquired_at=o.acquired_at,
        notes=o.notes,
        created_at=o.created_at,
    )

@router.post("", response_model=OwnedOut)
def create_owned(
    payload: OwnedCreateIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title is required")

    fmt = (payload.format or "other").strip().lower()
    allowed = {"hardcover", "paperback", "ebook", "audiobook", "other"}
    if fmt not in allowed:
        fmt = "other"

    o = OwnedItem(
        user_id=user.id,
        title=title,
        author=payload.author.strip() if payload.author else None,
        format=fmt,
        is_favorite=bool(payload.is_favorite),
        acquired_at=payload.acquired_at,
        notes=payload.notes.strip() if payload.notes else None,
    )
    session.add(o)
    session.commit()
    session.refresh(o)

    return OwnedOut(
        id=str(o.id),
        title=o.title,
        author=o.author,
        format=o.format,
        is_favorite=o.is_favorite,
        acquired_at=o.acquired_at,
        notes=o.notes,
        created_at=o.created_at,
    )


@router.delete("/{owned_id}")
def delete_owned(
    owned_id: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    o = session.exec(
        select(OwnedItem).where(OwnedItem.id == owned_id, OwnedItem.user_id == user.id)
    ).first()
    if not o:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(o)
    session.commit()
    return {"ok": True}
