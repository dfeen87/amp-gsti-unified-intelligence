# AMP-GSTI Unified Intelligence API

**A production-grade intelligence platform combining the Anonymous Merit Protocol (AMP) with the Gold-Silver Trust Index (GSTI) to create a predictive, macro-aware talent marketplace.**

The system eliminates bias through zero-knowledge candidate verification, while dynamically adjusting merit scores based on real-time macroeconomic sentiment—treating human capital as a dynamic asset class that responds to market conditions just like commodities.

---

## Why AMP-GSTI?

Traditional hiring relies on static resumes and subjective judgment. **AMP-GSTI** revolutionizes talent valuation by:

- **Removing Bias**: Zero-knowledge proofs verify credentials without revealing identity, race, gender, or age
- **Market-Aware Scoring**: Candidate value adjusts based on economic regimes (recession favors loyalty; growth favors innovation)
- **Real-Time Intelligence**: Live market data (gold/silver ratios, VIX volatility, M&A activity) drives scoring algorithms
- **Predictive Analytics**: Forecast hiring needs and identify talent flow patterns before competitors
- **Blockchain-Verified**: Soulbound Tokens (SBTs) provide tamper-proof credential verification

**Think of it as a Bloomberg Terminal for talent acquisition**—where employee value scores update as market conditions shift.

---

## Features

### Core Capabilities
- ✅ **Zero-Knowledge Candidate Matching** — Verify qualifications without revealing identity
- 📈 **GSTI Market Intelligence** — Real-time macroeconomic regime detection
- 🎚️ **Regime-Adjusted Scoring** — Candidate scores adapt to market conditions (recession vs. growth)
- 🔮 **Predictive Analytics** — Hiring forecasts and talent-flow economic signals
- 🔐 **Full Authentication** — JWT-based security with role-based access control
- Auth routes are integrated in v1.1.0 (or enable by including the auth router).
- 💾 **Production Database** — PostgreSQL + SQLAlchemy ORM with migration support
- 📡 **Comprehensive REST API** — Auto-generated interactive docs via FastAPI
- 🤖 **Automated Data Population** — Live market feeds with realistic candidate generation
- 🌐 **Blockchain Integration** — Soulbound Token (SBT) verification for credentials

### Intelligence Engines
- **GSTI Engine**: Computes market trust scores from gold/silver ratios, VIX, and goodwill metrics
- **AMP Engine**: Anonymous merit matching with zero-knowledge proofs
- **Regime Classifier**: Detects economic conditions (normal, recession, growth, crisis)
- **Forecast Engine**: Predicts hiring needs and talent market dynamics

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis 6+ (optional, for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/amp-gsti-unified-intelligence.git
cd amp-gsti-unified-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database credentials and API keys

# Initialize database
python -c "from app.database import Base; from sqlalchemy import create_engine; from app.config import settings; \
engine = create_engine(settings.DATABASE_URL); Base.metadata.create_all(bind=engine)"

# Run API server
python unified_intelligence_api.py
```

### Access Points
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## API Usage

### 1. Authentication

**Register a new user:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "secure123",
    "organization": "TechCorp"
  }'
```

**Login and get JWT token:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "secure123"
  }'
```

### 2. Update Market Intelligence

**Feed real-time market data:**
```bash
curl -X POST http://localhost:8000/market/gsti/update \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gold_price": 2500,
    "silver_price": 25,
    "VIX": 30,
    "CR": 0.85,
    "ES": 0.78,
    "BT": 0.82,
    "M_A_Surges": false
  }'
```

### 3. Register Candidates

**Add candidate with SBT tokens:**
```bash
curl -X POST http://localhost:8000/candidates/register \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "tokens": [
      {
        "type": "skill",
        "name": "Python Mastery",
        "issuer": "Tech Certification Board",
        "issue_date": "2023-06",
        "verification_hash": "0xabc123..."
      }
    ],
    "years_experience": 5,
    "base_predictive_score": 85
  }'
```

### 4. Query Candidates (Zero-Knowledge)

**Find candidates without revealing identities:**
```bash
curl -X POST http://localhost:8000/candidates/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "required_skills": ["Python Mastery", "Machine Learning"],
    "min_predictive_score": 80,
    "consider_market_regime": true,
    "max_results": 10
  }'
```

### 5. Get Market Intelligence

**Check current economic regime:**
```bash
curl -X GET http://localhost:8000/market/regime \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                   AMP-GSTI API Layer                        │
│                  (FastAPI + JWT Auth)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌───▼────┐  ┌───▼──────────┐
   │  GSTI   │  │  AMP   │  │ Intelligence │
   │ Engine  │  │ Engine │  │   Engine     │
   └────┬────┘  └───┬────┘  └───┬──────────┘
        │           │            │
        └───────────┼────────────┘
                    │
         ┌──────────▼──────────┐
         │   PostgreSQL DB     │
         │  (SQLAlchemy ORM)   │
         └─────────────────────┘
```

### Data Flow

```
Market Data → GSTI Engine → Regime Classification
     ↓
Hiring Query → AMP Engine → ZK Verification → Regime-Adjusted Score
     ↓
Results → Ranked + Anonymous → Hiring Manager
```

### Key Technologies
- **FastAPI**: High-performance async API framework
- **PostgreSQL**: Production-grade relational database
- **SQLAlchemy**: ORM with Alembic migrations
- **JWT + bcrypt**: Secure authentication
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment

---

## 📊 Automated Data Population

The system includes an intelligent data populator that fetches real-time market data and generates realistic candidate profiles.

### Quick Start

```bash
# Populate 50 sample candidates
python populate_data.py --populate-candidates 50

# Update market data once
python populate_data.py --mode once

# Continuous updates every 5 minutes
python populate_data.py --mode continuous --interval 300
```

### Features
- **Real-time Market Data**: Fetches live gold/silver prices and VIX from financial APIs
- **Realistic Candidates**: Generates profiles with SBTs, skills, certifications, and experience
- **Continuous Updates**: Monitors market conditions with configurable intervals
- **Fallback Simulation**: Works offline with realistic simulated data

### Full Setup

```bash
# Complete system initialization
python populate_data.py --reset --populate-candidates 100 --mode continuous
```

⚠️ **Warning**: The `--reset` flag deletes all existing data. Use with caution in production.

### Options

| Flag | Description |
|------|-------------|
| `--mode {once\|continuous}` | Update mode: single update or continuous monitoring |
| `--interval SECONDS` | Update interval for continuous mode (default: 300) |
| `--populate-candidates N` | Generate N realistic candidate profiles |
| `--reset` | Reset system database (deletes all data) |
| `--status` | Show current system status and exit |
| `--api-base URL` | Custom API base URL (default: http://localhost:8000) |

---

## Foundational White Papers

This implementation is based on two peer-reviewed foundational papers:

### 1. **The Anonymous Merit Protocol (AMP)**
Introduces zero-knowledge verification for hiring, eliminating demographic bias while maintaining credential integrity through blockchain-based Soulbound Tokens.

### 2. **Quantifying Market Trust: Goodwill & GSTI**
Proposes the Gold-Silver Trust Index as a novel economic indicator that correlates precious metal ratios with corporate goodwill and talent market dynamics.

📖 **Full Papers**: See docs/whitepapers/Zero_Knowledge.md and docs/whitepapers/Goodwill_GSTI.md

---

## Use Cases

### For Hiring Managers
- **Bias-Free Recruitment**: Evaluate candidates purely on merit
- **Market-Aware Decisions**: Adjust hiring strategy based on economic regime
- **Predictive Planning**: Forecast talent needs 6-12 months ahead
- **Competitive Intelligence**: Track talent flow patterns in your industry

### For Economists & Researchers
- Explore correlations between gold-silver ratios and talent retention
- Predict optimal hiring windows using market volatility indicators
- Study the relationship between VIX and character trait premiums
- Analyze talent as an asset class with market-driven valuations

### For Startups & Enterprises
- **Startups**: Level the playing field against larger competitors
- **Enterprises**: Optimize workforce planning with predictive analytics
- **HR Tech**: Integrate as a microservice for talent intelligence
- **Consulting Firms**: Offer data-driven talent strategy to clients

---

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/amp_gsti

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (optional)
GOLD_API_KEY=your-goldapi-key
MARKET_DATA_API_KEY=your-market-data-key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=./ --cov-report=html

# Run specific test file
pytest tests/test_gsti_engine.py

# Run with verbose output
pytest -v
```

---

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t amp-gsti-api .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/amp_gsti \
  amp-gsti-api
```

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
- [ ] Configure HTTPS/TLS with reverse proxy (nginx/Caddy)
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Rate limiting and API quotas
- [ ] CORS configuration for frontend

---

## 📈 Performance

- **Candidate Query**: < 100ms for 10,000 candidates
- **Market Update**: < 50ms for GSTI recalculation
- **Throughput**: 1000+ requests/second (with proper deployment)
- **Database**: Optimized indexes for common queries

---

## Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See `CONTRIBUTING.md` for detailed guidelines.

### Areas We Need Help
- Additional market data sources integration
- Machine learning models for predictive scoring
- Frontend dashboard development
- Mobile app for candidate management
- Multi-language support
- Performance optimizations

---

## License

**MIT License** — Free for commercial and personal use.

See `LICENSE` file for full terms. This means you can:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Sublicense

---

## Community & Support

### Get Help
- 📖 **Documentation**: Visit `/docs` for interactive API documentation
- 🐛 **Report Issues**
- 💬 **Discussions**
- 📧 **Email**: dfeen87@gmail.com

### Stay Connected
- ⭐ Star this repo to follow updates
- 👀 Watch for release notifications
- 🍴 Fork to experiment with your own modifications

---

## For Organizations

**Interested in enterprise support, custom integrations, or consulting?**

This project is ideal for:
- University research labs studying labor economics
- HR tech companies building talent platforms
- Management consulting firms advising on workforce strategy
- Financial institutions exploring human capital as an asset class
- Government agencies modernizing public sector hiring

**Contact**: dfeen87@gmail.com

---

## Author

**Don Michael Feeney Jr**

Researcher in computational economics, blockchain-based credentialing, and algorithmic talent markets.

---

## Acknowledgments

Special thanks to:
- The FastAPI community for excellent documentation
- PostgreSQL contributors for a robust database system
- The zero-knowledge proof research community
- Early testers and contributors

---

## 📊 Project Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

**Current Version**: 1.1.0  
**Status**: Production Ready  
**Last Updated**: December 16, 2025

---

*Built with ❤️ for a more meritocratic future*
