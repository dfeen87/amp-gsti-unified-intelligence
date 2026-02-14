"""
Global Observability Node - FastAPI Application
================================================

A standalone, read-only observability service for AMP-GSTI.
Exposes system state, intelligence engine diagnostics, and audit summaries.

SECURITY NOTES:
- All endpoints are GET-only
- No state modifications permitted
- No scoring, matching, or forecasting triggered
- No secrets or credentials exposed
- Graceful degradation when services unavailable
"""

import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

# Import observability modules
from observability_node import __version__
from observability_node.metrics import (
    get_system_metrics,
    get_uptime,
    get_database_metrics,
    get_redis_metrics,
    get_request_metrics,
)
from observability_node.state_extractors import (
    get_gsti_state,
    get_amp_state,
    get_forecast_state,
    get_audit_summary,
)


# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="AMP-GSTI Global Observability Node",
    description="Read-only observability service for AMP-GSTI Unified Intelligence Platform",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================================
# GLOBAL STATE (Lazy-loaded for graceful degradation)
# ============================================================================

_db_instance = None
_redis_instance = None


def get_db():
    """Lazy-load database connection."""
    global _db_instance
    if _db_instance is None:
        try:
            from app.database import get_db as get_database
            _db_instance = get_database()
        except Exception as e:
            print(f"Warning: Could not initialize database: {e}")
            _db_instance = None
    return _db_instance


def get_redis():
    """Lazy-load Redis connection if configured."""
    global _redis_instance
    if _redis_instance is None:
        try:
            from app.config import settings
            if settings.REDIS_URL:
                import redis
                _redis_instance = redis.from_url(settings.REDIS_URL)
            else:
                return None
        except Exception as e:
            print(f"Warning: Could not initialize Redis: {e}")
            _redis_instance = None
    return _redis_instance


# ============================================================================
# MIDDLEWARE - Reject Non-GET Requests
# ============================================================================

@app.middleware("http")
async def enforce_readonly(request: Request, call_next):
    """
    Middleware to enforce read-only behavior.
    Rejects all POST, PUT, PATCH, DELETE requests with 405.
    """
    if request.method not in ["GET", "HEAD", "OPTIONS"]:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "error": "Method not allowed",
                "message": "This is a read-only observability node. Only GET requests are permitted.",
                "allowed_methods": ["GET"]
            }
        )
    response = await call_next(request)
    return response


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint - API information."""
    return {
        "service": "AMP-GSTI Global Observability Node",
        "version": __version__,
        "status": "operational",
        "mode": "read-only",
        "endpoints": {
            "health": "/health",
            "system_state": "/api/system_state",
            "gsti_state": "/api/gsti_state",
            "amp_state": "/api/amp_state",
            "forecast_state": "/api/forecast_state",
            "audit_summary": "/api/audit_summary"
        },
        "documentation": {
            "openapi": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        - uptime
        - version
        - DB connectivity
        - Redis connectivity (if enabled)
        - environment mode
    """
    db = get_db()
    redis_client = get_redis()
    
    # Get uptime
    uptime_info = get_uptime()
    
    # Check DB connectivity
    db_status = "unknown"
    if db:
        try:
            db_check = db.check_connection()
            db_status = "connected" if db_check == "connected" else "disconnected"
        except Exception:
            db_status = "error"
    else:
        db_status = "not_configured"
    
    # Check Redis connectivity
    redis_status = "disabled"
    if redis_client:
        try:
            redis_client.ping()
            redis_status = "connected"
        except Exception:
            redis_status = "error"
    
    # Get environment mode
    environment = os.getenv("ENVIRONMENT", "unknown")
    
    return {
        "status": "healthy",
        "version": __version__,
        "uptime": uptime_info,
        "connectivity": {
            "database": db_status,
            "redis": redis_status
        },
        "environment": environment,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/system_state")
def system_state():
    """
    Get comprehensive system state.
    
    Returns:
        - CPU, memory, disk usage
        - Load averages
        - DB query rate (if available)
        - Redis cache hit/miss rate (if enabled)
        - Active JWT sessions (count only)
        - Request throughput (rolling window)
    """
    db = get_db()
    redis_client = get_redis()
    
    # Collect system metrics
    sys_metrics = get_system_metrics()
    
    # Database metrics
    db_metrics = {"status": "not_configured"}
    if db:
        db_metrics = get_database_metrics(db)
    
    # Redis metrics
    redis_metrics = get_redis_metrics(redis_client)
    
    # Request metrics (placeholder)
    request_metrics = get_request_metrics()
    
    # JWT sessions (placeholder - would need tracking)
    jwt_sessions = {
        "active_sessions": "N/A",
        "note": "JWT session tracking not yet implemented"
    }
    
    return {
        "status": "operational",
        "system_resources": sys_metrics,
        "database": db_metrics,
        "redis": redis_metrics,
        "jwt_sessions": jwt_sessions,
        "request_throughput": request_metrics,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/gsti_state")
def gsti_state():
    """
    Get current GSTI (Gold-Silver Trust Index) state.
    
    Returns:
        - Current gold-silver ratio
        - Volatility index
        - Detected economic regime
        - Confidence score
        - Last update timestamp
    """
    db = get_db()
    
    if not db:
        raise HTTPException(
            status_code=503,
            detail="Database not available. Cannot retrieve GSTI state."
        )
    
    state = get_gsti_state(db)
    
    if state.get("status") == "error":
        raise HTTPException(status_code=500, detail=state.get("error"))
    
    return state


@app.get("/api/amp_state")
def amp_state():
    """
    Get current AMP (Anonymous Merit Protocol) state.
    
    Returns:
        - Number of candidates evaluated
        - Distribution of merit scores (aggregated, anonymized)
        - Credential-weighting statistics
        - Last evaluation timestamp
    """
    db = get_db()
    
    if not db:
        raise HTTPException(
            status_code=503,
            detail="Database not available. Cannot retrieve AMP state."
        )
    
    state = get_amp_state(db)
    
    if state.get("status") == "error":
        raise HTTPException(status_code=500, detail=state.get("error"))
    
    return state


@app.get("/api/forecast_state")
def forecast_state():
    """
    Get forecast engine state.
    
    Returns:
        - Hiring outlook
        - Talent-flow indicators
        - Macroeconomic signals used by forecast engine
        - Model confidence or uncertainty metrics
    """
    db = get_db()
    
    if not db:
        raise HTTPException(
            status_code=503,
            detail="Database not available. Cannot retrieve forecast state."
        )
    
    state = get_forecast_state(db)
    
    if state.get("status") == "error":
        raise HTTPException(status_code=500, detail=state.get("error"))
    
    return state


@app.get("/api/audit_summary")
def audit_summary(limit: int = 50):
    """
    Get audit log summaries (anonymized, no PII).
    
    Args:
        limit: Number of recent audit entries to return (default: 50, max: 200)
        
    Returns:
        - Last N audit log entries
        - Mutation summaries
        - Permission-gated events (summaries only)
        - Timestamps and actor roles (no PII)
    """
    # Validate limit
    if limit < 1 or limit > 200:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 200"
        )
    
    db = get_db()
    
    if not db:
        raise HTTPException(
            status_code=503,
            detail="Database not available. Cannot retrieve audit summary."
        )
    
    summary = get_audit_summary(db, limit=limit)
    
    if summary.get("status") == "error":
        raise HTTPException(status_code=500, detail=summary.get("error"))
    
    return summary


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": f"Endpoint {request.url.path} does not exist",
            "available_endpoints": [
                "/health",
                "/api/system_state",
                "/api/gsti_state",
                "/api/amp_state",
                "/api/forecast_state",
                "/api/audit_summary"
            ]
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup."""
    print("=" * 70)
    print(f"AMP-GSTI Global Observability Node v{__version__}")
    print("=" * 70)
    print("Status: Operational")
    print("Mode: Read-Only")
    print("Security: All write operations disabled")
    print("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown."""
    print("=" * 70)
    print("AMP-GSTI Global Observability Node - Shutting down")
    print("=" * 70)
