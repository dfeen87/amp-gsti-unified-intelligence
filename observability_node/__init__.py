"""
Global Observability Node for AMP-GSTI Unified Intelligence Platform
=====================================================================

A standalone, read-only FastAPI microservice that exposes internal system state,
intelligence engine diagnostics, and audit summaries without exposing any control surfaces.

This node is designed to be:
- Safe: read-only, no state modifications
- Transparent: exposes system internals for monitoring
- Production-ready: graceful degradation, proper error handling
- Independent: runs separately from main API

Version: 3.1.1
"""

__version__ = "3.1.1"
