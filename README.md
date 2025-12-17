# AMP-GSTI Unified Intelligence Platform

**Version:** v2.0.0  
**Status:** Production-ready (security-hardened)

---

## Overview

AMP-GSTI is a production-grade intelligence platform that combines the **Anonymous Merit Protocol (AMP)** with the **Gold-Silver Trust Index (GSTI)** to enable macro-aware, merit-based talent evaluation.

The system evaluates candidates using credential-based, identity-minimized inputs, while dynamically adjusting merit scores based on macroeconomic regime signals. Talent is treated as a dynamic economic asset, responsive to market conditions in the same way commodities and capital flows are.

The platform is designed to be **auditable**, **server-authoritative**, and **defensively engineered**, prioritizing correctness, transparency, and operational safety over speculative automation.

---

## Why AMP-GSTI?

Traditional hiring systems rely on static resumes, subjective judgment, and identity-linked bias. AMP-GSTI replaces this model with:

### Identity-Minimized Evaluation
Credentials and attributes are processed without exposing unnecessary personal identifiers.

### Market-Aware Scoring
Candidate scores are adjusted based on explicit economic regimes (e.g., recession vs. growth).

### Deterministic Intelligence
All scoring and classification logic is server-side, logged, and inspectable.

### Predictive Signals
The system exposes forward-looking hiring and talent-flow indicators derived from macro inputs.

**Conceptually, AMP-GSTI functions like a market intelligence terminal for talent strategy — not an automated hiring oracle.**

---

## Core Features

### Platform Capabilities

✅ **Anonymous Merit Matching**  
Credential-based evaluation with minimized identity exposure.

📈 **GSTI Market Intelligence Engine**  
Regime detection driven by gold-silver ratios, volatility indices, and goodwill metrics.

🎚️ **Regime-Adjusted Scoring**  
Candidate scores are recalculated in response to macro conditions.

🔮 **Predictive Analytics**  
Talent-flow trends and hiring outlooks derived from system telemetry.

🔐 **Hardened Authentication**  
JWT-based authentication with server-authoritative role enforcement.

💾 **Production Database Layer**  
PostgreSQL + SQLAlchemy with explicit session control and audit logging.

📡 **Comprehensive REST API**  
Fully documented via FastAPI with OpenAPI support.

🤖 **Automated Data Population**  
Deterministic population tools for testing, demos, and research use.

> **Note:** Blockchain-based credential verification is architecturally supported. Production enforcement depends on external attestation sources.

### Intelligence Engines

**GSTI Engine**  
Computes market trust and regime signals from macroeconomic inputs.

**AMP Engine**  
Performs anonymous, credential-weighted candidate matching.

**Regime Classifier**  
Explicitly categorizes economic conditions (bullish / neutral / bearish).

**Forecast Engine**  
Generates hiring and talent-flow outlooks from historical and current data.

---

## Architecture Summary

```
[ Client / Dashboard ]
          ↓
[ Auth & Access Control ]
          ↓
[ AMP Matching Engine ]
          ↓
[ GSTI Market Intelligence ]
          ↓
[ PostgreSQL + Audit Logs ]
```

### Architectural Principles

- Server-authoritative decisions
- Stateless authentication (JWT)
- Explicit trust boundaries
- Logged mutations and queries
- No client-trusted scoring or permissions

Detailed assumptions and limits are documented in `docs/ASSUMPTIONS_LIMITS.md`.

---

## Security Model (High-Level)

AMP-GSTI follows a **defense-in-depth** approach:

- **JWTs identify users, not permissions**
- **Roles and access checks enforced server-side**
- **Tokens are short-lived and verifiable**
- **All mutations are permission-gated**
- **Database sessions are explicitly scoped**
- **Frontend controls are treated as advisory only**

A full security posture statement is provided in `SECURITY.md`.

---

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis (optional, for caching)

### Installation

```bash
git clone https://github.com/yourusername/amp-gsti-unified-intelligence.git
cd amp-gsti-unified-intelligence

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

**Initialize database:**

```bash
python unified_intelligence_api.py
```

### API Access

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

Authentication is required for all non-public endpoints.

---

## Data Population Utilities

The included `populate_data.py` script supports:

- Deterministic candidate generation
- Controlled market data updates
- Offline simulation modes
- Safe reset flags (explicitly destructive)

⚠️ **Use `--reset` only in non-production environments.**

---

## Configuration

Environment variables are documented in `.env.example`.  
**Never commit real secrets.**

Key variables:

- `DATABASE_URL`
- `SECRET_KEY` (≥ 32 chars)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DEBUG=False` in production

---

## Testing & Validation

```bash
pytest
pytest --cov
```

The platform favors **explicit validation** over hidden heuristics.

---

## Deployment Notes

- **HTTPS termination required** (reverse proxy)
- **JWT secrets must be rotated periodically**
- **Database backups are recommended**
- **Rate limits should be enforced at ingress**

---

## Project Status

- **Current Version:** v2.0.0
- **Stability:** Production-ready
- **Focus:** Correctness, auditability, and extensibility

This repository is intentionally conservative in scope. Features are added only when they can be defended, tested, and explained.

---

## License

**MIT License** — permissive, commercial-friendly.  
See `LICENSE` for full terms.

---

## Author

**Don Michael Feeney Jr**
