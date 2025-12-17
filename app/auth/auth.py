from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Header

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _extract_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split("Bearer ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


class AuthManager:
    """
    v2-hardened Auth Manager:
    - JWT identifies user only (sub), NOT authorization/roles.
    - get_current_user fetches user from DB and enforces active/token_version if present.
    """

    def __init__(self, db):
        self.db = db

        from config import settings  # expects config.py at project root

        self.secret_key = getattr(settings, "SECRET_KEY", None)
        self.algorithm = getattr(settings, "ALGORITHM", "HS256")
        self.access_token_expire = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30))

        # Optional hardening: issuer/audience. If not defined, enforcement is skipped.
        self.issuer = getattr(settings, "JWT_ISSUER", None)
        self.audience = getattr(settings, "JWT_AUDIENCE", None)

        # Basic secret hygiene
        if not self.secret_key or len(str(self.secret_key)) < 32:
            # Fail fast: weak/missing secret
            raise RuntimeError("SECRET_KEY missing or too short (min 32 chars recommended)")

        # Algorithm allow-list (prevent 'none'/weird alg configs)
        allowed_algs = {"HS256", "HS384", "HS512"}
        if self.algorithm not in allowed_algs:
            raise RuntimeError(f"Unsupported JWT algorithm: {self.algorithm}")

        # Guardrails on expiry
        if self.access_token_expire <= 0 or self.access_token_expire > 60 * 24 * 7:
            # 1 week max by default; adjust if you truly need longer-lived access tokens
            raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 1 and 10080")

    # -----------------------------
    # Passwords
    # -----------------------------
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # -----------------------------
    # API Keys (only keep if enforced server-side)
    # -----------------------------
    def generate_api_key(self) -> str:
        return secrets.token_urlsafe(32)

    # -----------------------------
    # JWT
    # -----------------------------
    def create_access_token(self, *, subject: str, token_version: Optional[int] = None) -> str:
        """
        subject: user id as string (sub)
        token_version: optional integer for revocation (user.token_version)
        """
        now = _utcnow()
        exp = now + timedelta(minutes=self.access_token_expire)

        payload: Dict[str, Any] = {
            "sub": str(subject),
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }

        # Optional issuer/audience hardening
        if self.issuer:
            payload["iss"] = self.issuer
        if self.audience:
            payload["aud"] = self.audience

        # Optional revocation support
        if token_version is not None:
            payload["ver"] = int(token_version)

        return jwt.encode(payload, str(self.secret_key), algorithm=self.algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            decode_kwargs: Dict[str, Any] = {
                "key": str(self.secret_key),
                "algorithms": [self.algorithm],
                "options": {
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "require_exp": True,
                    "require_sub": True,
                },
            }

            # Enforce aud/iss only if configured
            if self.audience:
                decode_kwargs["audience"] = self.audience
            if self.issuer:
                decode_kwargs["issuer"] = self.issuer

            payload = jwt.decode(token, **decode_kwargs)
            if not isinstance(payload, dict):
                raise HTTPException(status_code=401, detail="Unauthorized")
            return payload

        except JWTError:
            raise HTTPException(status_code=401, detail="Unauthorized")

    # -----------------------------
    # DB Operations
    # -----------------------------
    def register_user(self, username: str, email: str, password: str, organization: str):
        from database import User  # expects database.py exports User model

        session = self.db.get_session()
        try:
            existing = (
                session.query(User)
                .filter((User.email == email) | (User.username == username))
                .first()
            )
            if existing:
                # Don’t leak which field matched
                raise HTTPException(status_code=400, detail="User already exists")

            user = User(
                username=username,
                email=email,
                hashed_password=self.hash_password(password),
                organization=organization,
                api_key=self.generate_api_key(),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()

    def authenticate(self, email: str, password: str) -> str:
        """
        Returns a JWT access token.
        JWT contains ONLY identity (sub) + optional token version,
        NOT roles/is_admin flags.
        """
        from database import User

        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.email == email).first()

            # Generic unauthorized on failures
            if not user or not self.verify_password(password, user.hashed_password):
                raise HTTPException(status_code=401, detail="Unauthorized")

            # Optional: active check if model supports it
            if hasattr(user, "active") and user.active is False:
                raise HTTPException(status_code=401, detail="Unauthorized")

            token_version = getattr(user, "token_version", None)
            return self.create_access_token(subject=str(user.id), token_version=token_version)

        finally:
            session.close()


def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Hardened dependency:
    - Parses Bearer token
    - Verifies JWT
    - Fetches user from DB
    - Enforces user.active + token_version if present
    - Returns the *User object*, not token payload
    """
    token = _extract_bearer_token(authorization)

    from database import get_db, User  # expects database.py exports get_db + User
    db = get_db()
    auth = AuthManager(db)

    payload = auth.verify_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = db.get_session()
    try:
        user = session.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Optional: enforce active flag
        if hasattr(user, "active") and user.active is False:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Optional: enforce token revocation via token_version
        token_ver = payload.get("ver", None)
        if token_ver is not None and hasattr(user, "token_version"):
            if int(token_ver) != int(getattr(user, "token_version", 0)):
                raise HTTPException(status_code=401, detail="Unauthorized")

        return user

    finally:
        session.close()
