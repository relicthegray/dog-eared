from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models import IntakeItem, User

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
    item = IntakeItem(
        user_id=user.id,
        raw_text=payload.raw_text.strip(),
        source_id=payload.source_id,
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
