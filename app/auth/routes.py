from __future__ import annotations

from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, EmailStr, constr

from app.auth.auth import AuthManager, get_current_user
from database import get_db, User  # your database.py exports these


router = APIRouter(prefix="/auth", tags=["auth"])


# -----------------------------
# Request / Response Schemas
# -----------------------------
class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=1, max_length=64)
    password: constr(min_length=1, max_length=256)


class LoginResponse(BaseModel):
    token: str
    username: str
    role: str


class RegisterRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=64)
    email: EmailStr
    password: constr(min_length=8, max_length=256)
    organization: constr(strip_whitespace=True, min_length=1, max_length=128) = "unknown"


class PublicUser(BaseModel):
    id: int
    username: str
    email: str
    organization: Optional[str] = None
    role: str
    is_active: bool


def _role_from_user(user: User) -> str:
    # Keep roles server-authoritative (DB). JWT should NOT carry role.
    return "admin" if getattr(user, "is_admin", False) else "viewer"


def _client_ip(request: Request) -> str:
    # Respect reverse proxy headers if present (you can harden further with trusted proxies).
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# -----------------------------
# Endpoints
# -----------------------------
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request):
    """
    Authenticates using username + password.
    Returns a JWT access token and basic identity fields for the frontend.
    """
    db = get_db()
    auth = AuthManager(db)

    try:
        token = auth.authenticate(payload.username, payload.password)
    except HTTPException:
        # Best-effort audit log without leaking details
        try:
            db.log_activity(
                user_id=0,
                action="auth_login_failed",
                details={"username": payload.username, "ip": _client_ip(request)},
            )
        except Exception:
            pass
        raise

    # Fetch user (for role/username response)
    session = db.get_session()
    try:
        user = session.query(User).filter(User.username == payload.username).first()
        if not user or not getattr(user, "is_active", True):
            raise HTTPException(status_code=401, detail="Unauthorized")

        role = _role_from_user(user)

        try:
            db.log_activity(
                user_id=user.id,
                action="auth_login_success",
                details={"ip": _client_ip(request), "role": role},
            )
        except Exception:
            pass

        return LoginResponse(token=token, username=user.username, role=role)
    finally:
        session.close()


@router.post("/register", response_model=PublicUser)
def register(payload: RegisterRequest, request: Request):
    """
    Creates a new user record.
    Hardened: does not leak whether email vs username existed.
    """
    db = get_db()
    auth = AuthManager(db)

    try:
        user = auth.register_user(
            username=payload.username,
            email=str(payload.email),
            password=payload.password,
            organization=payload.organization,
        )
    except HTTPException:
        # propagate explicit HTTP errors from AuthManager
        raise
    except Exception:
        # Normalize to a safe response shape
        raise HTTPException(status_code=400, detail="User already exists")

    role = _role_from_user(user)

    try:
        db.log_activity(
            user_id=user.id,
            action="auth_register_success",
            details={"ip": _client_ip(request), "role": role},
        )
    except Exception:
        pass

    return PublicUser(
        id=user.id,
        username=user.username,
        email=user.email,
        organization=getattr(user, "organization", None),
        role=role,
        is_active=getattr(user, "is_active", True),
    )


@router.get("/me", response_model=PublicUser)
def me(user: User = Depends(get_current_user)):
    role = _role_from_user(user)
    return PublicUser(
        id=user.id,
        username=user.username,
        email=user.email,
        organization=getattr(user, "organization", None),
        role=role,
        is_active=getattr(user, "is_active", True),
    )


@router.post("/logout")
def logout(request: Request, user: User = Depends(get_current_user)):
    """
    v2 logout = token revocation (server-side) by bumping token_version.
    Requires User.token_version integer column to be present.

    If token_version is missing, it will still return 200, but *cannot* revoke
    already-issued JWTs (you should add token_version for true v2 hardening).
    """
    db = get_db()
    session = db.get_session()
    try:
        db_user = session.query(User).filter(User.id == user.id).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if hasattr(db_user, "token_version"):
            db_user.token_version = int(getattr(db_user, "token_version", 0)) + 1
            session.add(db_user)
            session.commit()

        try:
            db.log_activity(
                user_id=db_user.id,
                action="auth_logout",
                details={"ip": _client_ip(request)},
            )
        except Exception:
            pass

        return {"ok": True}
    finally:
        session.close()
