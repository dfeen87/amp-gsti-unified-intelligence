from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Header
from typing import Optional
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    def __init__(self, db):
        self.db = db
        from config import settings
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def generate_api_key(self) -> str:
        return secrets.token_urlsafe(32)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def register_user(self, username: str, email: str, password: str, organization: str):
        from database import User
        session = self.db.get_session()
        try:
            # Check if user exists
            existing = session.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            if existing:
                raise ValueError("User already exists")
            
            # Create new user
            user = User(
                username=username,
                email=email,
                hashed_password=self.hash_password(password),
                organization=organization,
                api_key=self.generate_api_key()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def authenticate(self, email: str, password: str) -> str:
        from database import User
        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.email == email).first()
            if not user or not self.verify_password(password, user.hashed_password):
                raise ValueError("Invalid credentials")
            
            # Create JWT token
            token_data = {
                "user_id": user.id,
                "email": user.email,
                "is_admin": user.is_admin
            }
            return self.create_access_token(token_data)
        finally:
            session.close()
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.split("Bearer ")[1]
    from database import get_db
    db = get_db()
    auth = AuthManager(db)
    
    try:
        payload = auth.verify_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
