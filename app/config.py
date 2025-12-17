from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Hardened application configuration (v2)
    """

    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False

    # -------------------------------------------------
    # Server
    # -------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -------------------------------------------------
    # Database
    # -------------------------------------------------
    DATABASE_URL: str

    # -------------------------------------------------
    # Redis (optional but explicit)
    # -------------------------------------------------
    REDIS_URL: str | None = None

    # -------------------------------------------------
    # Security / JWT
    # -------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # short-lived access tokens

    JWT_ISSUER: str = "amp-gsti"
    JWT_AUDIENCE: str = "amp-gsti-api"

    # -------------------------------------------------
    # CORS
    # -------------------------------------------------
    CORS_ORIGINS: List[str] = []

    # -------------------------------------------------
    # Rate Limiting
    # -------------------------------------------------
    RATE_LIMIT_PER_MINUTE: int = 60

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

    # -------------------------------------------------
    # Post-init validation (HARDENING)
    # -------------------------------------------------
    def validate(self):
        # Environment sanity
        if self.ENVIRONMENT not in {"development", "staging", "production"}:
            raise RuntimeError("Invalid ENVIRONMENT value")

        # Debug safety
        if self.ENVIRONMENT == "production" and self.DEBUG:
            raise RuntimeError("DEBUG must be False in production")

        # Secret hygiene
        if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY must be set and at least 32 characters long")

        # JWT algorithm allow-list
        if self.ALGORITHM not in {"HS256", "HS384", "HS512"}:
            raise RuntimeError("Unsupported JWT algorithm")

        # Token lifetime guardrails
        if not (5 <= self.ACCESS_TOKEN_EXPIRE_MINUTES <= 1440):
            raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 5 and 1440")

        # CORS enforcement
        if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
            raise RuntimeError("CORS_ORIGINS must be explicitly set in production")

        return self


settings = Settings().validate()
