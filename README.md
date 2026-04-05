<div align="center">

# 🎯 AMP-GSTI Unified Intelligence Platform

### Market-Aware, Merit-Based Talent Evaluation

[![Version](https://img.shields.io/badge/version-v3.1.1-blue.svg)](https://github.com/dfeen87/amp-gsti-unified-intelligence/releases)
[![Status](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/dfeen87/amp-gsti-unified-intelligence)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Security](https://img.shields.io/badge/security-hardened-red.svg)](docs/SECURITY.md)

[Features](#-core-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture-summary) • [Documentation](#-documentation) • [License](#-license)

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Why AMP-GSTI?](#-why-amp-gsti)
- [Core Features](#-core-features)
- [Architecture Summary](#-architecture-summary)
- [Security Model](#-security-model)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Data Population](#-data-population-utilities)
- [Testing & Validation](#-testing--validation)
- [Deployment](#-deployment-notes)
- [Global Observability Node](#-global-observability-node)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Support](#-support)
- [Acknowledgements](#acknowledgements)
- [License](#-license)

---

## 📖 Overview

AMP-GSTI is a production-grade intelligence platform that combines the **Anonymous Merit Protocol (AMP)** with the **Gold-Silver Trust Index (GSTI)** to enable macro-aware, merit-based talent evaluation.

The system evaluates candidates using credential-based, identity-minimized inputs, while dynamically adjusting merit scores based on macroeconomic regime signals. Talent is treated as a dynamic economic asset, responsive to market conditions in the same way commodities and capital flows are.

The platform is designed to be **auditable**, **server-authoritative**, and **defensively engineered**, prioritizing correctness, transparency, and operational safety over speculative automation.

---

## 🎯 Why AMP-GSTI?

Traditional hiring systems rely on static resumes, subjective judgment, and identity-linked bias. AMP-GSTI replaces this model with:

<table>
<tr>
<td width="50%">

### 🔒 Identity-Minimized Evaluation
Credentials and attributes are processed without exposing unnecessary personal identifiers.

</td>
<td width="50%">

### 📊 Market-Aware Scoring
Candidate scores are adjusted based on explicit economic regimes (e.g., recession vs. growth).

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Deterministic Intelligence
All scoring and classification logic is server-side, logged, and inspectable.

</td>
<td width="50%">

### 🔮 Predictive Signals
The system exposes forward-looking hiring and talent-flow indicators derived from macro inputs.

</td>
</tr>
</table>

> **💡 Key Insight:** AMP-GSTI functions like a market intelligence terminal for talent strategy — not an automated hiring oracle.

---

## ✨ Core Features

### 🚀 Platform Capabilities

| Feature | Description |
|---------|-------------|
| **🎭 Anonymous Merit Matching** | Credential-based evaluation with minimized identity exposure |
| **📈 GSTI Market Intelligence Engine** | Regime detection driven by gold-silver ratios, volatility indices, and goodwill metrics |
| **🎚️ Regime-Adjusted Scoring** | Candidate scores are recalculated in response to macro conditions |
| **🔮 Predictive Analytics** | Talent-flow trends and hiring outlooks derived from system telemetry |
| **🔐 Hardened Authentication** | JWT-based authentication with server-authoritative role enforcement |
| **💾 Production Database Layer** | PostgreSQL + SQLAlchemy with explicit session control and audit logging |
| **📡 Comprehensive REST API** | Fully documented via FastAPI with OpenAPI support |
| **🤖 Automated Data Population** | Deterministic population tools for testing, demos, and research use |

> **⚠️ Note:** Blockchain-based credential verification is architecturally supported. Production enforcement depends on external attestation sources.

### 🧠 Intelligence Engines

<table>
<tr>
<td width="50%">

#### GSTI Engine
Computes market trust and regime signals from macroeconomic inputs.

#### AMP Engine
Performs anonymous, credential-weighted candidate matching.

</td>
<td width="50%">

#### Regime Classifier
Explicitly categorizes economic conditions (bullish / neutral / bearish).

#### Forecast Engine
Generates hiring and talent-flow outlooks from historical and current data.

</td>
</tr>
</table>

---

## 🏗️ Architecture Summary

### 🔐 Architectural Principles

<div align="center">

```
┌──────────────────────────────┐
│  Client / Dashboard          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Auth & Access Control       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  AMP Matching Engine         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  GSTI Market Intelligence    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  PostgreSQL + Audit Logs     │
└──────────────────────────────┘
```

</div>

**Core Principles:**

- ✅ Server-authoritative decisions
- ✅ Stateless authentication (JWT)
- ✅ Explicit trust boundaries
- ✅ Logged mutations and queries
- ✅ No client-trusted scoring or permissions

📖 Detailed assumptions and limits are documented in [`docs/ASSUMPTIONS_LIMITS.md`](docs/ASSUMPTIONS_LIMITS.md).

---

## 🔒 Security Model

AMP-GSTI follows a **defense-in-depth** approach:

| Security Layer | Implementation |
|----------------|----------------|
| **🔑 Authentication** | JWTs identify users, not permissions |
| **👥 Authorization** | Roles and access checks enforced server-side |
| **⏱️ Token Management** | Tokens are short-lived and verifiable |
| **🔐 Mutation Control** | All mutations are permission-gated |
| **💽 Database Security** | Sessions are explicitly scoped |
| **🖥️ Frontend Trust** | Controls are treated as advisory only |

📖 A full security posture statement is provided in [`SECURITY.md`](docs/SECURITY.md).

---

## 🚀 Quick Start

### 📋 Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| PostgreSQL | 13+ |
| Redis | Latest (optional, for caching) |

### ⚡ Installation

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/dfeen87/amp-gsti-unified-intelligence.git
cd amp-gsti-unified-intelligence
```

2️⃣ **Set up virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

4️⃣ **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your database credentials and secrets
```

5️⃣ **Start the API server** (initializes database schema on first run):

```bash
python unified_intelligence_api.py
```

### 🌐 API Access

Once running, access the platform at:

| Endpoint | URL | Description |
|----------|-----|-------------|
| **API Server** | http://localhost:8000 | Main application |
| **API Documentation** | http://localhost:8000/docs | Interactive OpenAPI docs |
| **Health Check** | http://localhost:8000/health | Service status |

> **🔐 Note:** Authentication is required for all non-public endpoints.

---

## ⚙️ Configuration

Environment variables are documented in [`.env.example`](.env.example).

> **⚠️ Security Warning:** Never commit real secrets to version control.

### 🔑 Key Configuration Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` |
| `SECRET_KEY` | JWT signing key (≥ 32 chars) | Auto-generated secure string |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token validity duration | `60` |
| `DEBUG` | Debug mode flag | `False` (production) |

---

## 🗃️ Data Population Utilities

The included `populate_data.py` script supports:

- ✅ Deterministic candidate generation
- ✅ Controlled market data updates
- ✅ Offline simulation modes
- ✅ Safe reset flags (explicitly destructive)

> **⚠️ Warning:** Use `--reset` only in non-production environments.

---

## 🧪 Testing & Validation

Run the test suite with:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov
```

> **💡 Philosophy:** The platform favors **explicit validation** over hidden heuristics.

---

## 🚢 Deployment Notes

### Production Checklist

| Item | Requirement |
|------|-------------|
| **🔒 HTTPS** | Termination required (reverse proxy) |
| **🔑 JWT Secrets** | Must be rotated periodically |
| **💾 Database Backups** | Recommended for data safety |
| **🚦 Rate Limits** | Should be enforced at ingress |

---

## 📊 Global Observability Node

A standalone **Global Observability Node** provides production monitoring and transparency without exposing any control surfaces.

### 🎯 What is the Observability Node?

A read-only FastAPI microservice that exposes:

- 📈 System resource metrics (CPU, memory, disk, load)
- 🔌 Database and Redis connectivity status
- 📊 GSTI market intelligence state
- 🎯 AMP candidate evaluation metrics (anonymized)
- 🔮 Hiring forecast indicators
- 📝 Audit log summaries (no PII)

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| **🔒 Read-Only by Design** | All write operations rejected with HTTP 405 |
| **🚫 No State Modifications** | Never triggers scoring, matching, or forecasting |
| **💪 Graceful Degradation** | Works even when Redis or optional services are unavailable |
| **🔌 Independent Service** | Runs on port 8081 (configurable via `OBS_NODE_PORT`) |
| **🔐 Production-Safe** | No secrets, credentials, or PII exposed |
| **🌐 No Authentication Required** | Safe because it's read-only |

### ⚡ Quick Start

1️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

2️⃣ **Run observability node:**

```bash
# Default: localhost:8081
python -m observability_node.run

# Or with custom port
export OBS_NODE_PORT=8082
python -m observability_node.run
```

### 📡 Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check with uptime, DB/Redis connectivity |
| `GET /api/system_state` | CPU, memory, disk, load, DB query rate, Redis hit rate |
| `GET /api/gsti_state` | Gold-silver ratio, market regime, confidence score |
| `GET /api/amp_state` | Candidate count, merit score distribution, credential stats |
| `GET /api/forecast_state` | Hiring outlook, talent flow, macro signals, model confidence |
| `GET /api/audit_summary` | Recent audit logs (anonymized, no PII) |

### 📚 Documentation

📖 **Complete Guide:** [`observability_node/QUICKSTART.md`](observability_node/QUICKSTART.md)

**Includes:**
- Endpoint examples with response formats
- Docker deployment guide
- Kubernetes deployment YAML
- Security model explanation
- Monitoring and alerting setup

### 💻 Example Usage

```bash
# Check system health
curl http://localhost:8081/health

# Get GSTI market intelligence
curl http://localhost:8081/api/gsti_state

# View system resource usage
curl http://localhost:8081/api/system_state

# Get hiring forecast
curl http://localhost:8081/api/forecast_state
```

### 🐳 Docker Deployment

```bash
# Build image
docker build -f Dockerfile.observability -t amp-gsti-obs:latest .

# Run container
docker run -d -p 8081:8081 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/amp_gsti \
  amp-gsti-obs:latest
```

### 🎯 Why a Separate Observability Node?

<table>
<tr>
<td width="50%">

#### 🎨 Separation of Concerns
Monitoring doesn't interfere with core API

#### 🔒 Security Isolation
Read-only guarantees prevent accidental mutations

</td>
<td width="50%">

#### 📈 Independent Scaling
Observability can scale separately from workload APIs

#### 🔍 Audit Transparency
Exposes system state without exposing control surfaces

</td>
</tr>
</table>

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

| Document | Description |
|----------|-------------|
| [`API_CONTRACT.md`](docs/API_CONTRACT.md) | Complete API specification |
| [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System architecture details |
| [`SECURITY.md`](docs/SECURITY.md) | Security model and best practices |
| [`ASSUMPTIONS_LIMITS.md`](docs/ASSUMPTIONS_LIMITS.md) | System assumptions and limitations |

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow the existing code style** and conventions
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

> **💡 Philosophy:** This repository is intentionally conservative in scope. Features are added only when they can be defended, tested, and explained.

---

## 💬 Support

### 📞 Getting Help

- 📖 Check the [documentation](docs/)
- 🐛 Report bugs via [GitHub Issues](https://github.com/dfeen87/amp-gsti-unified-intelligence/issues)
- 💡 Request features via [GitHub Discussions](https://github.com/dfeen87/amp-gsti-unified-intelligence/discussions)

### 📊 Project Status

| Metric | Value |
|--------|-------|
| **Current Version** | v3.1.1 |
| **Stability** | Production-ready |
| **Focus** | Correctness, auditability, and extensibility |

---

## Acknowledgements

This project was developed with a combination of original ideas, hands‑on coding, and support from advanced AI systems. I would like to acknowledge **Microsoft Copilot**, **Anthropic Claude**, and **OpenAI ChatGPT** for their meaningful assistance in refining concepts, improving clarity, and strengthening the overall quality of this work.

---

## License

This project is available for **non‑commercial use only** under the terms of the included LICENSE file.  
Commercial use requires a separate paid license. To inquire, contact: dfeen87@gmail.com

---

## 👤 Author

**Don Michael Feeney Jr**

---

<div align="center">

Made with ❤️ by the AMP-GSTI team

[⬆ Back to Top](#-amp-gsti-unified-intelligence-platform)

</div>
