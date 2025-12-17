from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Generator

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from config import settings

Base = declarative_base()

# -----------------------------
# Models (Hardened)
# -----------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)
    organization = Column(String(128), nullable=True)

    api_key = Column(String(128), unique=True, index=True, nullable=False)

    # Prefer roles over boolean admin flags, but keep your field for compatibility.
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))

    # Token revocation lever: bump to invalidate prior JWTs if you include it in JWT claims.
    token_version = Column(Integer, nullable=False, server_default=text("0"))

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class CandidateDB(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    wallet_address = Column(String(64), unique=True, index=True, nullable=False)

    # Store SBT tokens as JSON (always list-like)
    tokens = Column(JSON, nullable=False, server_default=text("'[]'::json"))

    years_experience = Column(Integer, nullable=False)
    base_predictive_score = Column(Float, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


class GSTIMetricDB(Base):
    __tablename__ = "gsti_metrics"

    id = Column(Integer, primary_key=True, index=True)

    gold_price = Column(Float, nullable=False)
    silver_price = Column(Float, nullable=False)

    gsr = Column(Float, nullable=False)
    goodwill_momentum = Column(Float, nullable=False)

    gsti_score = Column(Float, nullable=False)
    market_regime = Column(String(32), nullable=False, index=True)

    general_goodwill = Column(Float, nullable=True)
    consumer_goodwill = Column(Float, nullable=True)
    unified_goodwill_score = Column(Float, nullable=True)
    vix = Column(Float, nullable=True)

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    action = Column(String(128), nullable=False, index=True)
    details = Column(JSON, nullable=False, server_default=text("'{}'::json"))

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


# Helpful composite indexes
Index("ix_activity_user_action_time", ActivityLog.user_id, ActivityLog.action, ActivityLog.timestamp)
Index("ix_gsti_time_regime", GSTIMetricDB.timestamp, GSTIMetricDB.market_regime)


# -----------------------------
# Engine + Session (Hardened)
# -----------------------------

def _make_engine():
    # NOTE: add SSL params in DATABASE_URL for prod if needed (recommended).
    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
        future=True,
    )


ENGINE = _make_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE, expire_on_commit=False)

# Create tables once at import-time (OK for small deploys). For bigger prod, use migrations (Alembic).
Base.metadata.create_all(bind=ENGINE)


# -----------------------------
# FastAPI Dependency (Correct)
# -----------------------------

def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency:
      - yields a DB session per request
      - ensures close() always happens
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Database Service Layer
# -----------------------------

class Database:
    """
    Thin wrapper around a Session factory. This keeps your calling style similar,
    but with hardened engine/session underneath.
    """

    def get_session(self) -> Session:
        return SessionLocal()

    def check_connection(self) -> str:
        try:
            with ENGINE.connect() as conn:
                conn.execute(text("SELECT 1"))
            return "connected"
        except Exception as e:
            return f"error: {str(e)}"

    # -------------------------
    # Candidate Operations
    # -------------------------

    def save_candidate(self, candidate) -> int:
        session = self.get_session()
        try:
            tokens_list = [token.dict() for token in getattr(candidate, "tokens", [])] or []

            db_candidate = CandidateDB(
                wallet_address=candidate.wallet_address,
                tokens=tokens_list,
                years_experience=int(candidate.years_experience),
                base_predictive_score=float(candidate.base_predictive_score),
            )
            session.add(db_candidate)
            session.commit()
            session.refresh(db_candidate)
            return db_candidate.id
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def candidate_exists(self, wallet_address: str) -> bool:
        session = self.get_session()
        try:
            return (
                session.query(CandidateDB.id)
                .filter(CandidateDB.wallet_address == wallet_address)
                .first()
                is not None
            )
        finally:
            session.close()

    def get_all_candidates(self) -> List[CandidateDB]:
        session = self.get_session()
        try:
            return session.query(CandidateDB).all()
        finally:
            session.close()

    def get_candidate_by_wallet(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        session = self.get_session()
        try:
            candidate = (
                session.query(CandidateDB)
                .filter(CandidateDB.wallet_address == wallet_address)
                .first()
            )
            if not candidate:
                return None

            tokens = candidate.tokens or []
            if not isinstance(tokens, list):
                tokens = []

            return {
                "wallet_address": candidate.wallet_address,
                "tokens": tokens,
                "years_experience": candidate.years_experience,
                "base_predictive_score": candidate.base_predictive_score,
            }
        finally:
            session.close()

    def delete_candidate(self, wallet_address: str) -> bool:
        session = self.get_session()
        try:
            candidate = (
                session.query(CandidateDB)
                .filter(CandidateDB.wallet_address == wallet_address)
                .first()
            )
            if not candidate:
                return False
            session.delete(candidate)
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_candidate_statistics(self) -> Dict[str, Any]:
        session = self.get_session()
        try:
            candidates = session.query(CandidateDB).all()
            if not candidates:
                return {"total_candidates": 0, "average_experience": 0.0, "average_predictive_score": 0.0}

            total = len(candidates)
            avg_exp = sum(c.years_experience for c in candidates) / total
            avg_score = sum(c.base_predictive_score for c in candidates) / total

            return {
                "total_candidates": total,
                "average_experience": round(float(avg_exp), 2),
                "average_predictive_score": round(float(avg_score), 2),
            }
        finally:
            session.close()

    # -------------------------
    # GSTI Operations
    # -------------------------

    def save_gsti_metrics(self, metrics: Dict[str, Any]) -> int:
        session = self.get_session()
        try:
            db_metrics = GSTIMetricDB(**metrics)
            session.add(db_metrics)
            session.commit()
            session.refresh(db_metrics)
            return db_metrics.id
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_latest_gsti_metrics(self) -> Optional[Dict[str, Any]]:
        session = self.get_session()
        try:
            metric = session.query(GSTIMetricDB).order_by(GSTIMetricDB.timestamp.desc()).first()
            if not metric:
                return None

            return {
                "gsr": metric.gsr,
                "goodwill_momentum": metric.goodwill_momentum,
                "gsti_score": metric.gsti_score,
                "market_regime": metric.market_regime,
                "timestamp": metric.timestamp.isoformat(),
            }
        finally:
            session.close()

    def get_gsti_history(self, days: int) -> List[Dict[str, Any]]:
        session = self.get_session()
        try:
            cutoff = datetime.utcnow() - timedelta(days=int(days))
            metrics = (
                session.query(GSTIMetricDB)
                .filter(GSTIMetricDB.timestamp >= cutoff)
                .order_by(GSTIMetricDB.timestamp.desc())
                .all()
            )

            return [
                {"gsti_score": m.gsti_score, "market_regime": m.market_regime, "timestamp": m.timestamp.isoformat()}
                for m in metrics
            ]
        finally:
            session.close()

    # -------------------------
    # Activity Logging
    # -------------------------

    def log_activity(self, user_id: Optional[int], action: str, details: Dict[str, Any]):
        session = self.get_session()
        try:
            log = ActivityLog(user_id=user_id, action=action, details=details or {})
            session.add(log)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_activity_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        session = self.get_session()
        try:
            logs = (
                session.query(ActivityLog)
                .order_by(ActivityLog.timestamp.desc())
                .limit(int(limit))
                .all()
            )
            return [
                {
                    "user_id": log.user_id,
                    "action": log.action,
                    "details": log.details,
                    "timestamp": log.timestamp.isoformat(),
                }
                for log in logs
            ]
        finally:
            session.close()

    # -------------------------
    # System Stats
    # -------------------------

    def get_system_stats(self) -> Dict[str, Any]:
        session = self.get_session()
        try:
            total_candidates = session.query(CandidateDB).count()
            total_queries = session.query(ActivityLog).filter(ActivityLog.action == "candidate_query").count()
            active_users = session.query(User).filter(User.is_active.is_(True)).count()
            gsti_records = session.query(GSTIMetricDB).count()

            latest_gsti = session.query(GSTIMetricDB).order_by(GSTIMetricDB.timestamp.desc()).first()

            return {
                "total_candidates": total_candidates,
                "total_queries": total_queries,
                "active_users": active_users,
                "gsti_records": gsti_records,
                "latest_gsti_update": latest_gsti.timestamp.isoformat() if latest_gsti else None,
            }
        finally:
            session.close()

    def get_talent_flow_metrics(self) -> Dict[str, Any]:
        session = self.get_session()
        try:
            candidates = session.query(CandidateDB).all()
            if not candidates:
                return {"total_candidates": 0, "token_distribution": {}}

            from collections import defaultdict
            token_counts = defaultdict(int)

            for c in candidates:
                tokens = c.tokens or []
                if not isinstance(tokens, list):
                    continue
                for token in tokens:
                    ttype = token.get("type", "unknown")
                    name = token.get("name", "unknown")
                    token_counts[f"{ttype}:{name}"] += 1

            return {"total_candidates": len(candidates), "token_distribution": dict(token_counts)}
        finally:
            session.close()

    def create_backup(self) -> str:
        # Stub: implement with your cloud/db provider tooling (pg_dump, snapshots, etc.)
        import uuid
        return str(uuid.uuid4())


def get_db() -> Database:
    """
    Keep your existing import pattern:
        from database import get_db
        db = get_db()
    but without a global engine/session anti-pattern.
    """
    return Database()
