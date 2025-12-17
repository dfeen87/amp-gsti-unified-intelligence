# AMP-GSTI Unified Intelligence Platform

## Security Posture & Disclosure Policy

### Overview

This repository implements AMP-GSTI, a production-grade intelligence platform designed around explicit trust boundaries, server-authoritative decisioning, and defensive authentication.

**Security in this project is not treated as an afterthought or checklist item.**  
Instead, it is enforced through architecture, constraints, and assumption transparency.

This document explains:

- What is secured by design
- What is intentionally not guaranteed
- How to responsibly disclose security issues

---

## What Is Secure

### Authentication & Identity

- **JWT-based authentication** with identity-only tokens
- **No roles, permissions, or authority embedded in JWT claims**
- Tokens contain:
  - `sub` (user id)
  - `exp`, `iat`
  - optional `token_version` for revocation
- **Server-side token revocation** via `token_version`
- **Passwords hashed using bcrypt** (passlib)
- **Generic authentication errors** to prevent oracle attacks

### Authorization

- **All authorization decisions are server-side**
- User roles (admin, viewer, etc.) are **stored and enforced in the database**
- Frontend role indicators are **informational only**
- **Mutating endpoints are explicitly gated**

### Session & Token Handling

- **Stateless access tokens**
- **No client-trusted session state**
- **No long-lived refresh tokens**
- **Logout invalidates all issued tokens** via version bump

### Database Safety

- **Explicit SQLAlchemy sessions**
- **No global mutable session reuse**
- **Defensive JSON handling** for token metadata
- **Activity logging** for sensitive operations

### Input Validation

- **Numeric bounds enforced server-side**
- **Wallet address validation**
- **Structured request schemas**
- **No reliance on frontend validation** for security

### Auditability

- **Authentication events logged:**
  - login success
  - login failure
  - logout
- **Candidate registration and queries logged**
- **Market mutation events logged**
- **Audit mode supported** (read-only operation)

### Transport Security

- **Designed for HTTPS-only deployment**
- **Production mode rejects insecure origins**
- **Explicit CORS configuration**

---

## What Is Intentionally Not Guaranteed

The following are **out of scope by design**, not oversights:

### Client-Side Security

- The **frontend is not trusted**
- **Client-side code integrity is not guaranteed**
- **All security enforcement occurs server-side**

### Credential Recovery

- **No password reset or email verification flow**
- **No MFA enforcement**
- These may be added in future versions if required

### Denial-of-Service Protection

- **Application-level rate limiting** is present for sensitive endpoints
- **Infrastructure-level DDoS protection** is assumed to be handled upstream (CDN, WAF, reverse proxy)

### Data Confidentiality Beyond Platform Scope

- This platform does **not encrypt application-level payloads beyond TLS**
- **Database encryption at rest** is deployment-dependent
- **No client-side encryption** of candidate metadata

### Formal Cryptographic Proofs

- **ZK-matching terminology** refers to privacy-preserving inference concepts
- This repository does **not implement full cryptographic zero-knowledge proofs**
- **Claims are descriptive, not cryptographically formal**

---

## Threat Model Summary

### This system is designed to resist:

- Token forgery
- Role escalation
- Replay after logout
- Frontend manipulation
- Unauthorized mutation of market or candidate data

### This system does not attempt to resist:

- Malicious infrastructure operators
- Compromised host OS
- Physical access to servers
- Advanced side-channel attacks

---

## Reporting a Vulnerability

If you discover a security issue:

1. **Do not open a public GitHub issue**
2. **Provide a minimal reproduction**
3. **Include:**
   - Affected endpoint or file
   - Impact assessment
   - Suggested mitigation (if known)

**Responsible disclosure is appreciated and respected.**

---

## Security Philosophy

Security in AMP-GSTI follows these principles:

- **Trust nothing that can be forged**
- **Enforce authority where state lives**
- **Prefer explicit denial over silent failure**
- **Document assumptions instead of hiding them**

This repository favors **clarity and correctness** over buzzwords or inflated claims.

---

## Versioning

- This security posture applies to **v2.0.0**
- Future versions may expand authentication, authorization, or cryptographic guarantees
- **Breaking security changes will be documented explicitly**
