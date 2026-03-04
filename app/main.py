"""
Canonical application entry point.

Usage:
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from unified_intelligence_api import app  # noqa: F401

__all__ = ["app"]
