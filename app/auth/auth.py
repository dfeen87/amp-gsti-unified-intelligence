from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Header
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import get_db, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _extract_bearer_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split("Bearer ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


class AuthManager:
    """
    v2-hardened Auth Manager
    """

    def __init__(self, db=None):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.issuer = settings.JWT_ISSUER
        self.audience = settings.JWT_AUDIENCE
        self._db = db

    # -----------------------------
    # Passwords
    # -----------------------------
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # -----------------------------
    # JWT
    # -----------------------------
    def create_access_token(self, *, subject: str, token_version: int) -> str:
        now = _utcnow()
        exp = now + timedelta(minutes=self.access_token_expire)

        payload = {
            "sub": subject,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "iss": self.issuer,
            "aud": self.audience,
            "ver": token_version,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience,
                options={"require": ["exp", "sub"]},
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Unauthorized")

    # -----------------------------
    # Authentication
    # -----------------------------
    def authenticate(self, username: str, password: str) -> str:
        db = self._db or get_db()
        session = db.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user or not self.verify_password(password, user.hashed_password):
                db.log_activity(None, "login_failed", {"username": username})
                raise HTTPException(status_code=401, detail="Unauthorized")

            if not user.is_active:
                raise HTTPException(status_code=401, detail="Unauthorized")

            token = self.create_access_token(
                subject=str(user.id),
                token_version=user.token_version,
            )

            db.log_activity(user.id, "login_success", {})
            return token
        finally:
            session.close()

    def register_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
        organization: str,
    ) -> User:
        db = self._db or get_db()
        session = db.get_session()
        try:
            existing = (
                session.query(User)
                .filter((User.username == username) | (User.email == email))
                .first()
            )
            if existing:
                raise HTTPException(status_code=400, detail="User already exists")

            api_key = secrets.token_hex(32)
            user = User(
                username=username,
                email=email,
                hashed_password=self.hash_password(password),
                organization=organization,
                api_key=api_key,
                is_admin=False,
                is_active=True,
                token_version=0,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    token = _extract_bearer_token(authorization)

    auth = AuthManager()
    payload = auth.verify_token(token)

    user_id = payload.get("sub")
    token_ver = payload.get("ver")

    db = get_db()
    session = db.get_session()
    try:
        user = session.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if user.token_version != token_ver:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return user
    finally:
        session.close()
