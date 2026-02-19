from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select
from uuid import UUID

from app.core.security import decode_token
from app.db.session import get_session
from app.models import User

bearer = HTTPBearer(auto_error=False)

def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_session),
) -> User:
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(creds.credentials)
        sub = payload.get("sub")
        user_id = UUID(sub)  # ✅ convert token subject string -> UUID
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user
