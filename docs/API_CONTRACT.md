# AMP-GSTI API Contract  
## Stability & Interface Guarantees

This document defines the logical API contract for AMP-GSTI v3.1.1.  
It is intended as a human-readable stability reference and does not replace OpenAPI specifications.

---

## Design Guarantees

- Deterministic outputs
- Stateless request handling
- No side effects in scoring endpoints
- Backward compatibility across patch versions

---

## Core Endpoints

### Health Check

**GET** `/health`

Returns system readiness status.

**Guarantee:**  
Always available; no dependency on intelligence engines.

---

### Regime Classification

**POST** `/regime/classify`

**Input**
- Macroeconomic signal bundle

**Output**
- Regime label (bullish / neutral / bearish)
- Confidence score

**Guarantee**
- Regime determination is independent of candidate data

---

### Candidate Scoring

**POST** `/candidates/score`

**Input**
- Anonymized candidate profile
- Current macro signal snapshot (or reference)

**Output**
- Regime-adjusted merit score
- Component breakdown

**Guarantees**
- No identity or demographic inputs
- No persistent state modification
- Explainable score components

---

## Determinism Policy

Given identical inputs:
- Scores are reproducible
- Regime classifications are stable
- Output ordering is deterministic

---

## Backward Compatibility Policy

- Patch releases (`v3.1.x`) will not change:
  - Endpoint signatures
  - Score semantics
  - Regime definitions

- Minor releases (`v3.x.0`) may:
  - Enable previously scaffolded features
  - Add new endpoints without breaking existing ones

---

## Implemented Capabilities

The following capabilities are active in v3.1.1:

- Authentication enforcement (JWT, server-authoritative)
- Persistent storage (PostgreSQL + SQLAlchemy)
- Longitudinal audit logging
