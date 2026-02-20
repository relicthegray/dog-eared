from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_session, init_db
from app.models import Invite, User

router = APIRouter()


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterIn(BaseModel):
    email: EmailStr
    display_name: str
    password: str
    invite_token: str


class InviteCreateIn(BaseModel):
    email: EmailStr
    expires_hours: int = 72


class InviteOut(BaseModel):
    email: EmailStr
    token: str
    expires_at: datetime


def ensure_bootstrap_admin(session: Session) -> None:
    """Create the first admin user if it doesn't exist."""
    existing = session.exec(select(User).where(User.email == settings.ADMIN_EMAIL)).first()
    if existing:
        return
    admin = User(
        email=settings.ADMIN_EMAIL,
        display_name=settings.ADMIN_DISPLAY_NAME,
        password_hash=hash_password(settings.ADMIN_PASSWORD),
        is_admin=True,
        is_active=True,
    )
    session.add(admin)
    session.commit()


@router.on_event("startup")
def _startup():
    init_db()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, session: Session = Depends(get_session)):
    ensure_bootstrap_admin(session)
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenOut(access_token=create_access_token(str(user.id)))


@router.post("/invite", response_model=InviteOut)
def create_invite(payload: InviteCreateIn, session: Session = Depends(get_session)):
    # V1: keep this simple (admin check will be added when auth middleware lands)
    ensure_bootstrap_admin(session)
    admin = session.exec(select(User).where(User.email == settings.ADMIN_EMAIL)).first()
    token = uuid4().hex + uuid4().hex
    expires_at = datetime.utcnow() + timedelta(hours=payload.expires_hours)
    inv = Invite(
        email=payload.email,
        token=token,
        expires_at=expires_at,
        created_by_user_id=admin.id,
    )
    session.add(inv)
    session.commit()
    return InviteOut(email=payload.email, token=token, expires_at=expires_at)


@router.post("/register")
def register(payload: RegisterIn, session: Session = Depends(get_session)):
    ensure_bootstrap_admin(session)

    if settings.ALLOW_OPEN_REGISTRATION:
        invite = None
    else:
        invite = session.exec(select(Invite).where(Invite.token == payload.invite_token)).first()
        if not invite or invite.used_at is not None:
            raise HTTPException(status_code=400, detail="Invalid invite token")
        if invite.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invite token expired")

    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=False,
    )
    session.add(user)
    if invite:
        invite.used_at = datetime.utcnow()
        session.add(invite)
    session.commit()
    return {"ok": True}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "display_name": user.display_name,
        "is_admin": user.is_admin,
    }