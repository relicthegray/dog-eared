from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models import IntakeItem, Source, User

router = APIRouter()


class IntakeCreateIn(BaseModel):
    raw_text: str
    source_id: UUID | None = None
    source_post_url: str | None = None


class IntakeOut(BaseModel):
    id: str
    raw_text: str
    status: str
    captured_at: datetime
    source_id: str | None
    source_name: str | None
    source_type: str | None
    source_post_url: str | None


def _as_utc(dt: datetime) -> datetime:
    # If DB returns naive datetime (common with SQLite), treat it as UTC.
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _is_tiktok_url(url: str | None) -> bool:
    if not url:
        return False
    return "tiktok.com" in url.lower()


def _ensure_tiktok_source(session: Session, user_id: UUID) -> UUID:
    """Find or create the user's canonical TikTok Source and return its id."""
    existing = session.exec(
        select(Source).where(Source.user_id == user_id, Source.type == "tiktok")
    ).first()
    if existing:
        return existing.id

    s = Source(
        user_id=user_id,
        type="tiktok",
        name="TikTok",
        url=None,
        notes=None,
        created_at=datetime.now(timezone.utc),
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s.id


def _sources_by_id(session: Session, user_id: UUID, ids: set[UUID]) -> dict[UUID, Source]:
    if not ids:
        return {}
    rows = session.exec(
        select(Source).where(Source.user_id == user_id, Source.id.in_(ids))
    ).all()
    return {s.id: s for s in rows}


@router.get("", response_model=list[IntakeOut])
def list_intake(
    status: str | None = None,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = select(IntakeItem).where(IntakeItem.user_id == user.id)
    if status:
        stmt = stmt.where(IntakeItem.status == status)
    stmt = stmt.order_by(IntakeItem.captured_at.desc())
    items = session.exec(stmt).all()

    src_ids: set[UUID] = {i.source_id for i in items if i.source_id is not None}
    src_map = _sources_by_id(session=session, user_id=user.id, ids=src_ids)

    out: list[IntakeOut] = []
    for i in items:
        src = src_map.get(i.source_id) if i.source_id else None
        out.append(
            IntakeOut(
                id=str(i.id),
                raw_text=i.raw_text,
                status=i.status,
                captured_at=_as_utc(i.captured_at),
                source_id=str(i.source_id) if i.source_id else None,
                source_name=src.name if src else None,
                source_type=src.type if src else None,
                source_post_url=i.source_post_url,
            )
        )
    return out


@router.post("", response_model=IntakeOut)
def create_intake(
    payload: IntakeCreateIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # Auto-attach a TikTok Source when a TikTok URL is provided and source_id isn't.
    source_id = payload.source_id
    if source_id is None and _is_tiktok_url(payload.source_post_url):
        source_id = _ensure_tiktok_source(session=session, user_id=user.id)

    item = IntakeItem(
        user_id=user.id,
        raw_text=payload.raw_text.strip(),
        source_id=source_id,
        source_post_url=payload.source_post_url,
        captured_at=datetime.now(timezone.utc),
        status="new",
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    src = None
    if item.source_id:
        src = session.exec(
            select(Source).where(Source.user_id == user.id, Source.id == item.source_id)
        ).first()

    return IntakeOut(
        id=str(item.id),
        raw_text=item.raw_text,
        status=item.status,
        captured_at=_as_utc(item.captured_at),
        source_id=str(item.source_id) if item.source_id else None,
        source_name=src.name if src else None,
        source_type=src.type if src else None,
        source_post_url=item.source_post_url,
    )