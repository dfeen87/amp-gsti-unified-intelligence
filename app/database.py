from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    organization = Column(String)
    api_key = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CandidateDB(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    tokens = Column(JSON)  # Store SBT tokens as JSON
    years_experience = Column(Integer)
    base_predictive_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GSTIMetricDB(Base):
    __tablename__ = "gsti_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    gold_price = Column(Float)
    silver_price = Column(Float)
    gsr = Column(Float)
    goodwill_momentum = Column(Float)
    gsti_score = Column(Float)
    market_regime = Column(String)
    general_goodwill = Column(Float, nullable=True)
    consumer_goodwill = Column(Float, nullable=True)
    unified_goodwill_score = Column(Float, nullable=True)
    vix = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    action = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# Database Manager
class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def check_connection(self) -> str:
        try:
            with self.engine.connect() as conn:
                return "connected"
        except Exception as e:
            return f"error: {str(e)}"
    
    # Candidate Operations
    def save_candidate(self, candidate) -> int:
        session = self.get_session()
        try:
            db_candidate = CandidateDB(
                wallet_address=candidate.wallet_address,
                tokens=[token.dict() for token in candidate.tokens],
                years_experience=candidate.years_experience,
                base_predictive_score=candidate.base_predictive_score
            )
            session.add(db_candidate)
            session.commit()
            session.refresh(db_candidate)
            return db_candidate.id
        finally:
            session.close()
    
    def candidate_exists(self, wallet_address: str) -> bool:
        session = self.get_session()
        try:
            return session.query(CandidateDB).filter(
                CandidateDB.wallet_address == wallet_address
            ).first() is not None
        finally:
            session.close()
    
    def get_all_candidates(self) -> List[Any]:
        session = self.get_session()
        try:
            candidates = session.query(CandidateDB).all()
            return candidates
        finally:
            session.close()
    
    def get_candidate_by_wallet(self, wallet_address: str) -> Optional[Dict]:
        session = self.get_session()
        try:
            candidate = session.query(CandidateDB).filter(
                CandidateDB.wallet_address == wallet_address
            ).first()
            if candidate:
                return {
                    "wallet_address": candidate.wallet_address,
                    "tokens": candidate.tokens,
                    "years_experience": candidate.years_experience,
                    "base_predictive_score": candidate.base_predictive_score
                }
            return None
        finally:
            session.close()
    
    def delete_candidate(self, wallet_address: str) -> bool:
        session = self.get_session()
        try:
            candidate = session.query(CandidateDB).filter(
                CandidateDB.wallet_address == wallet_address
            ).first()
            if candidate:
                session.delete(candidate)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_candidate_statistics(self) -> Dict[str, Any]:
        session = self.get_session()
        try:
            candidates = session.query(CandidateDB).all()
            if not candidates:
                return {"total_candidates": 0}
            
            import numpy as np
            avg_exp = np.mean([c.years_experience for c in candidates])
            avg_score = np.mean([c.base_predictive_score for c in candidates])
            
            return {
                "total_candidates": len(candidates),
                "average_experience": round(avg_exp, 2),
                "average_predictive_score": round(avg_score, 2)
            }
        finally:
            session.close()
    
    # GSTI Operations
    def save_gsti_metrics(self, metrics: Dict[str, Any]) -> int:
        session = self.get_session()
        try:
            db_metrics = GSTIMetricDB(**metrics)
            session.add(db_metrics)
            session.commit()
            session.refresh(db_metrics)
            return db_metrics.id
        finally:
            session.close()
    
    def get_latest_gsti_metrics(self) -> Optional[Dict]:
        session = self.get_session()
        try:
            metric = session.query(GSTIMetricDB).order_by(
                GSTIMetricDB.timestamp.desc()
            ).first()
            if metric:
                return {
                    "gsr": metric.gsr,
                    "goodwill_momentum": metric.goodwill_momentum,
                    "gsti_score": metric.gsti_score,
                    "market_regime": metric.market_regime,
                    "timestamp": metric.timestamp.isoformat()
                }
            return None
        finally:
            session.close()
    
    def get_gsti_history(self, days: int) -> List[Dict]:
        session = self.get_session()
        try:
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(days=days)
            metrics = session.query(GSTIMetricDB).filter(
                GSTIMetricDB.timestamp >= cutoff
            ).order_by(GSTIMetricDB.timestamp.desc()).all()
            
            return [{
                "gsti_score": m.gsti_score,
                "market_regime": m.market_regime,
                "timestamp": m.timestamp.isoformat()
            } for m in metrics]
        finally:
            session.close()
    
    # Activity Logging
    def log_activity(self, user_id: int, action: str, details: Dict[str, Any]):
        session = self.get_session()
        try:
            log = ActivityLog(user_id=user_id, action=action, details=details)
            session.add(log)
            session.commit()
        finally:
            session.close()
    
    def get_activity_logs(self, limit: int = 100) -> List[Dict]:
        session = self.get_session()
        try:
            logs = session.query(ActivityLog).order_by(
                ActivityLog.timestamp.desc()
            ).limit(limit).all()
            
            return [{
                "user_id": log.user_id,
                "action": log.action,
                "details": log.details,
                "timestamp": log.timestamp.isoformat()
            } for log in logs]
        finally:
            session.close()
    
    # System Stats
    def get_system_stats(self) -> Dict[str, Any]:
        session = self.get_session()
        try:
            total_candidates = session.query(CandidateDB).count()
            total_queries = session.query(ActivityLog).filter(
                ActivityLog.action == "candidate_query"
            ).count()
            active_users = session.query(User).filter(User.is_active == True).count()
            gsti_records = session.query(GSTIMetricDB).count()
            
            latest_gsti = session.query(GSTIMetricDB).order_by(
                GSTIMetricDB.timestamp.desc()
            ).first()
            
            return {
                "total_candidates": total_candidates,
                "total_queries": total_queries,
                "active_users": active_users,
                "gsti_records": gsti_records,
                "latest_gsti_update": latest_gsti.timestamp.isoformat() if latest_gsti else None
            }
        finally:
            session.close()
    
    def get_talent_flow_metrics(self) -> Dict[str, Any]:
        """Get anonymized talent flow data"""
        session = self.get_session()
        try:
            candidates = session.query(CandidateDB).all()
            if not candidates:
                return {}
            
            from collections import defaultdict
            token_counts = defaultdict(int)
            
            for c in candidates:
                for token in c.tokens:
                    token_counts[f"{token['type']}:{token['name']}"] += 1
            
            return {
                "total_candidates": len(candidates),
                "token_distribution": dict(token_counts)
            }
        finally:
            session.close()
    
    def get_talent_activity_history(self, days: int) -> List[Dict]:
        """Get historical talent activity"""
        session = self.get_session()
        try:
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(days=days)
            
            activities = session.query(ActivityLog).filter(
                ActivityLog.timestamp >= cutoff,
                ActivityLog.action.in_(["candidate_register", "candidate_query"])
            ).all()
            
            return [{
                "action": a.action,
                "timestamp": a.timestamp.isoformat()
            } for a in activities]
        finally:
            session.close()
    
    def create_backup(self) -> str:
        """Create database backup"""
        import uuid
        backup_id = str(uuid.uuid4())
        # Implement actual backup logic here
        return backup_id

# Dependency
_db = None

def get_db() -> Database:
    global _db
    if _db is None:
        from config import settings
        _db = Database(settings.DATABASE_URL)
    return _db
