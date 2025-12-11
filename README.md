# AMP-GSTI Unified Intelligence API

Production API combining the Anonymous Merit Protocol (AMP) with the Gold-Silver Trust Index (GSTI) to create a predictive talent marketplace that adjusts hiring decisions based on real-time macroeconomic sentiment. Eliminates bias through zero-knowledge proofs while dynamically weighting candidate merit scores according to market regime signals.

## Features

- **Zero-Knowledge Candidate Matching**: Verify qualifications without revealing identity
- **GSTI Market Intelligence**: Real-time macroeconomic regime detection
- **Regime-Adjusted Scoring**: Candidate scores adapt to market conditions
- **Predictive Analytics**: AI-driven hiring forecasts and talent flow analysis
- **Full Authentication**: JWT-based security with role-based access
- **Production Database**: PostgreSQL with SQLAlchemy ORM
- **Comprehensive API**: RESTful design with automatic documentation

## Quick Start

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from database import Base, create_engine; from config import settings; engine = create_engine(settings.DATABASE_URL); Base.metadata.create_all(bind=engine)"

# Run API
python unified_intelligence_api.py
```

### Access

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage

### 1. Authentication

Register a new user:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"secure123","organization":"TechCorp"}'
```

Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secure123"}'
```

### 2. Update Market Intelligence

```bash
curl -X POST http://localhost:8000/market/gsti/update \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"gold_price":2500,"silver_price":25,"VIX":30}'
```

### 3. Register Candidates

```bash
curl -X POST http://localhost:8000/candidates/register \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"wallet_address":"0x123...","tokens":[...],"years_experience":5,"base_predictive_score":85}'
```

### 4. Query Candidates

```bash
curl -X POST http://localhost:8000/candidates/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"required_skills":["Python Mastery"],"min_predictive_score":80,"consider_market_regime":true}'
```

## Architecture

### Components

- **GSTI Engine**: Calculates Gold-Silver Trust Index from market data
- **AMP Engine**: Matches candidates using zero-knowledge proofs
- **Intelligence Engine**: Generates forecasts and analyzes talent flows
- **Database Layer**: PostgreSQL with SQLAlchemy ORM
- **Auth Layer**: JWT-based authentication with bcrypt password hashing

### Data Flow

1. Market data → GSTI Engine → Market regime classification
2. Hiring query → AMP Engine → ZK-proof verification → Regime-adjusted scoring
3. Results ranked and returned anonymously

## 📊 Data Population

The system includes an automated data populator that fetches real-time market data and generates realistic candidate profiles.

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

⚠️ **Warning**: The `--reset` flag deletes all existing data. Use with caution.

### Options

| Flag | Description |
|------|-------------|
| `--mode {once\|continuous}` | Update mode |
| `--interval SECONDS` | Update interval for continuous mode (default: 300) |
| `--populate-candidates N` | Generate N candidate profiles |
| `--reset` | Reset system (deletes all data) |
| `--status` | Show system status |

## White Papers

This implementation is based on two foundational white papers:

The Anonymous Merit Protocol: A Predictive, Zero-Knowledge Framework for High-Performing Talent

Quantifying Market Trust: How Goodwill and GSTI Create a Smarter Forecasting Model

These two white papers can be read in the files Zero-Knowledge.md and Goodwill_GSTI.md

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## Support

- Documentation: /docs
- Issues: GitHub Issues
- Email: dfeen87@gmail.com

## Authors

Don Michael Feeney Jr
