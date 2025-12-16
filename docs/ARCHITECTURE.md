# AMP-GSTI Unified Intelligence API  
## System Architecture Overview

AMP-GSTI is a production-grade intelligence system designed to evaluate human capital as a dynamic, trust-sensitive asset class. The system integrates anonymous merit verification with macroeconomic signal intelligence while maintaining determinism, explainability, and modularity.

This document describes the architectural structure of the v1.0.0 system.

---

## High-Level Design Principles

- **Deterministic intelligence** — identical inputs yield identical outputs
- **Explainability by construction** — no opaque model layers
- **Separation of concerns** — intelligence logic is isolated from infrastructure
- **Bias resistance** — identity and demographics are excluded by design
- **Research-first clarity** — simulation and production paths are explicitly separated

---

## Core Intelligence Components

### 1. GSTI Engine (Macroeconomic Trust Signals)

The GSTI engine computes macro-level trust and confidence signals using:

- Gold / silver ratios
- Volatility and regime stress indicators
- Aggregate goodwill dynamics

Outputs are normalized trust indices used downstream for regime classification and score modulation.

---

### 2. Regime Classifier

The regime classifier categorizes prevailing macro conditions into:

- **Bullish**
- **Neutral**
- **Bearish**

Classification is deterministic and based solely on macro inputs. No candidate-level data influences regime detection.

---

### 3. AMP Matching Engine

The AMP engine performs anonymous candidate evaluation and matching:

- No identity attributes
- No demographic data
- No resume parsing

Candidates are represented via anonymized skill vectors and Soulbound-style tokens. Scores adapt dynamically to the detected macro regime.

---

### Intelligence Flow

Macroeconomic Signals  
↓  
GSTI Engine  
↓  
Regime Classifier  
↓  
Regime-Adjusted Scoring  
↓  
AMP Matching Engine  
↓  
API Output


Each stage is independently testable and auditable.

---

## API Layer

- Implemented using **FastAPI**
- Stateless request handling
- Deterministic response generation
- Health check endpoint for operational readiness

The API layer contains **no intelligence logic**.

---

## Execution Model

- In-memory execution by default
- Designed for clarity, experimentation, and validation
- Persistence is architecture-ready but disabled in v1.0.0

---

## Explicit Non-Goals (v1.0.0)

- Machine learning or black-box inference
- Identity verification
- Demographic or behavioral profiling
- Automated hiring decisions
- Persistence-backed historical scoring

These are intentional exclusions to preserve transparency and auditability.

---

## Forward Compatibility

Authentication, persistence, and extended data sources are architecturally prepared and scheduled for later minor releases without modification to core intelligence logic.

