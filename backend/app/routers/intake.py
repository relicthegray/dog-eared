from datetime import datetime
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
    source_post_url: str | None


def _is_tiktok_url(url: str | None) -> bool:
    if not url:
        return False
    return "tiktok.com" in url.lower()


def _ensure_tiktok_source(session: Session, user_id: UUID) -> UUID:
    """
    Find or create the user's canonical TikTok source and return its id.
    Keeps this intentionally simple (no scraping / enrichment).
    """
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
        created_at=datetime.utcnow(),
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s.id


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

    return [
        IntakeOut(
            id=str(i.id),
            raw_text=i.raw_text,
            status=i.status,
            captured_at=i.captured_at,
            source_id=str(i.source_id) if i.source_id else None,
            source_post_url=i.source_post_url,
        )
        for i in items
    ]


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
        captured_at=datetime.utcnow(),
        status="new",
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return IntakeOut(
        id=str(item.id),
        raw_text=item.raw_text,
        status=item.status,
        captured_at=item.captured_at,
        source_id=str(item.source_id) if item.source_id else None,
        source_post_url=item.source_post_url,
    )
