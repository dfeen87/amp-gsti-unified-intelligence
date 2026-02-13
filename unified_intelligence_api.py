"""
AMP-GSTI Unified Intelligence API
================================

A production-grade intelligence API that unifies the Anonymous Merit Protocol (AMP)
with the Gold-Silver Trust Index (GSTI) to model talent as a dynamic, market-responsive asset.

This system reframes hiring intelligence through a macroeconomic lens:
candidate merit is evaluated anonymously, cryptographically verified,
and adaptively scored based on prevailing economic regimes.

Rather than treating human capital as static, AMP-GSTI models talent valuation
the way markets model commodities — responsive to volatility, confidence, and trust.

-----------------------------------------------------------------------

CORE PRINCIPLES
• Merit without identity — credentials are verified without exposing demographics
• Market awareness — talent valuation adapts to macroeconomic regimes
• Predictive intelligence — hiring signals emerge before competitors react
• Cryptographic trust — Soulbound-style credential modeling
• Systemic clarity — explicit separation between simulation and production concerns

-----------------------------------------------------------------------

ARCHITECTURE OVERVIEW
• FastAPI-based REST interface
• Modular intelligence engines (GSTI + AMP)
• Regime-aware scoring pipeline
• Zero-knowledge verification simulation
• Deterministic, explainable outputs
• Demo-friendly, production-extensible design

-----------------------------------------------------------------------

IMPORTANT IMPLEMENTATION NOTES
• This release intentionally uses in-memory state to enable rapid experimentation,
  research validation, and clean onboarding.
• Persistence layers (PostgreSQL / Redis) are designed to be introduced
  without altering the intelligence logic.
• Zero-knowledge verification is modeled as a cryptographic abstraction
  for clarity and extensibility.

This file serves as both:
1) a runnable intelligence system
2) a reference implementation of AMP-GSTI concepts

Version: 1.0.0
Status: Initial Public Release
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import numpy as np
from collections import defaultdict
import json

# ============================================================================
# CORE DATA MODELS
# ============================================================================

class SBTType(str, Enum):
    SKILL = "skill"
    CHARACTER = "character"
    LOYALTY = "loyalty"
    PROJECT = "project"
    CERTIFICATION = "certification"

class MarketRegime(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class SoulboundToken(BaseModel):
    type: SBTType
    name: str
    issuer: str
    issue_date: str
    verification_hash: str = Field(default="0x0000...0000")

class Candidate(BaseModel):
    wallet_address: str
    tokens: List[SoulboundToken]
    years_experience: int
    base_predictive_score: float = Field(ge=0, le=100)
    
class HiringQuery(BaseModel):
    required_skills: List[str] = []
    required_character: List[str] = []
    required_loyalty: List[str] = []
    min_predictive_score: float = Field(default=70, ge=0, le=100)
    consider_market_regime: bool = Field(default=True)

class GSTIMetrics(BaseModel):
    gold_price: float
    silver_price: float
    gsr: float
    goodwill_momentum: float
    gsti_score: float
    market_regime: MarketRegime
    timestamp: str

# ============================================================================
# GSTI CALCULATOR ENGINE
# Gold-Silver Trust Index — Macroeconomic Intelligence Layer
# ============================================================================

class GSTIEngine:
    """Enhanced GSTI calculator with dynamic weighting"""
    
    def __init__(self):
        self.w1 = 0.6  # General Goodwill weight
        self.w2 = 0.4  # Consumer Goodwill weight
        self.w_goodwill = 1.0
        self.w_gsr = 0.01
        self._historical_ugs = []
        
    def calculate_general_goodwill(
        self, 
        CR: float, ES: float, BT: float, 
        RG: float, w_t: float, NCB: float, T: float
    ) -> float:
        """General Goodwill (G) - Long-term structural trust"""
        if T == 0:
            raise ValueError("Time normalization cannot be zero")
        numerator = CR * ES * BT * (np.power(RG, w_t) - NCB)
        return numerator / T
    
    def calculate_consumer_goodwill(
        self,
        CS: float, BR: float, CA: float, 
        SS: float, NCB_consumer: float
    ) -> float:
        """Consumer Goodwill (CG) - Immediate external perception"""
        if NCB_consumer == 0:
            NCB_consumer = 0.001
        return (CS * BR * CA * SS) / NCB_consumer
    
    def calculate_ugs(self, G: float, CG: float, T: float) -> float:
        """Unified Goodwill Score"""
        if T == 0:
            raise ValueError("Temporal normalization cannot be zero")
        ugs = ((self.w1 * G) + (self.w2 * CG)) / T
        self._historical_ugs.append(ugs)
        return ugs
    
    def calculate_gsr(self, gold_price: float, silver_price: float) -> float:
        """Gold-Silver Ratio"""
        if silver_price == 0:
            raise ValueError("Silver price cannot be zero")
        return gold_price / silver_price
    
    def calculate_goodwill_momentum(self, period: int = 2) -> float:
        """Momentum of Goodwill over time"""
        if len(self._historical_ugs) < period:
            return 0.0
        ugs_current = self._historical_ugs[-1]
        ugs_prior = self._historical_ugs[-period]
        if ugs_prior == 0:
            return 0.0
        return (ugs_current - ugs_prior) / ugs_prior
    
    def dynamic_weighting_adjustment(self, VIX: float, M_A_Surges: bool):
        """Adjust weights based on market volatility"""
        if VIX > 25:
            self.w_gsr = 0.015
            self.w_goodwill = 0.8
        elif M_A_Surges:
            self.w_gsr = 0.005
            self.w_goodwill = 1.2
        else:
            self.w_gsr = 0.01
            self.w_goodwill = 1.0
    
    def calculate_gsti(self, gold_price: float, silver_price: float) -> Dict[str, Any]:
        """Calculate complete GSTI metrics"""
        gsr = self.calculate_gsr(gold_price, silver_price)
        momentum = self.calculate_goodwill_momentum()
        gsti = (self.w_goodwill * momentum) - (self.w_gsr * gsr)
        
        # Determine market regime
        if gsti > 0.05:
            regime = MarketRegime.BULLISH
        elif gsti < -0.05:
            regime = MarketRegime.BEARISH
        else:
            regime = MarketRegime.NEUTRAL
        
        return {
            "gsr": gsr,
            "goodwill_momentum": momentum,
            "gsti_score": gsti,
            "market_regime": regime,
            "timestamp": datetime.utcnow().isoformat()
        }

# ============================================================================
# AMP MATCHING ENGINE
# Anonymous Merit Protocol — Regime-Aware Candidate Evaluation
# ============================================================================

class AMPMatchingEngine:
    """Anonymous Merit Protocol candidate matching with GSTI integration"""
    
    def __init__(self, gsti_engine: GSTIEngine):
        self.gsti_engine = gsti_engine

    def _build_token_profile(self, candidate: Candidate) -> Dict[str, Any]:
        skills = set()
        character = set()
        loyalty = set()
        lower_names = []

        for token in candidate.tokens:
            name = token.name
            lower_name = name.lower()
            lower_names.append(lower_name)

            if token.type == SBTType.SKILL:
                skills.add(name)
            elif token.type == SBTType.CHARACTER:
                character.add(name)
            elif token.type == SBTType.LOYALTY:
                loyalty.add(name)

        return {
            "skills": skills,
            "character": character,
            "loyalty": loyalty,
            "lower_names": lower_names,
        }
        
    def calculate_zk_proof_match(
        self, 
        candidate: Candidate, 
        query: HiringQuery,
        token_profile: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Simulate Zero-Knowledge Proof verification
        Returns True if candidate meets ALL criteria without revealing identity
        """
        profile = token_profile or self._build_token_profile(candidate)

        # Check skills
        if not all(skill in profile["skills"] for skill in query.required_skills):
            return False
        
        # Check character
        if not all(trait in profile["character"] for trait in query.required_character):
            return False
        
        # Check loyalty
        if not all(loyalty in profile["loyalty"] for loyalty in query.required_loyalty):
            return False
        
        return True
    
    def calculate_regime_adjusted_score(
        self,
        base_score: float,
        candidate: Candidate,
        market_regime: MarketRegime,
        token_profile: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Adjust candidate predictive score based on current market regime
        """
        score = base_score

        profile = token_profile or self._build_token_profile(candidate)
        lower_names = profile["lower_names"]
        
        # Get candidate's token profile
        has_loyalty = bool(profile["loyalty"])
        has_innovation = any("innovation" in name for name in lower_names)
        has_stability = any(
            "loyalty" in name or "mentor" in name
            for name in lower_names
        )
        
        # Regime-based adjustments
        if market_regime == MarketRegime.BEARISH:
            # Prioritize stability and proven performance
            if has_stability:
                score *= 1.15
            if has_loyalty:
                score *= 1.10
            if has_innovation and not has_stability:
                score *= 0.95
                
        elif market_regime == MarketRegime.BULLISH:
            # Prioritize growth potential and innovation
            if has_innovation:
                score *= 1.15
            if candidate.years_experience < 5:  # Growth potential
                score *= 1.08
            if has_loyalty and candidate.years_experience > 10:
                score *= 0.98  # Slight penalty for over-stability in growth mode
                
        # Cap at 100
        return min(score, 100.0)
    
    def match_candidates(
        self,
        candidates: List[Candidate],
        query: HiringQuery,
        gsti_metrics: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Main matching algorithm with ZK-proof simulation and GSTI integration
        """
        matches = []
        
        for candidate in candidates:
            token_profile = self._build_token_profile(candidate)
            # Step 1: ZK-Proof verification (binary pass/fail)
            if not self.calculate_zk_proof_match(candidate, query, token_profile):
                continue
            
            # Step 2: Base score check
            if candidate.base_predictive_score < query.min_predictive_score:
                continue
            
            # Step 3: Regime adjustment (if enabled and metrics available)
            final_score = candidate.base_predictive_score
            regime_adjustment = 0.0
            
            if query.consider_market_regime and gsti_metrics:
                regime = gsti_metrics.get("market_regime", MarketRegime.NEUTRAL)
                adjusted_score = self.calculate_regime_adjusted_score(
                    candidate.base_predictive_score,
                    candidate,
                    regime,
                    token_profile
                )
                regime_adjustment = adjusted_score - candidate.base_predictive_score
                final_score = adjusted_score
            
            matches.append({
                "wallet_address": candidate.wallet_address,
                "base_score": candidate.base_predictive_score,
                "regime_adjusted_score": final_score,
                "regime_adjustment": regime_adjustment,
                "token_count": len(candidate.tokens),
                "years_experience": candidate.years_experience,
                "zk_proof_verified": True
            })
        
        # Sort by final score descending
        matches.sort(key=lambda x: x["regime_adjusted_score"], reverse=True)
        return matches

# ============================================================================
# API APPLICATION
# RESTful Interface Layer
# ============================================================================

app = FastAPI(
    title="AMP-GSTI Unified Intelligence API",
    description="Production API for merit-based talent matching with macroeconomic intelligence",
    version="1.0.0"
)

# Initialize engines
gsti_engine = GSTIEngine()
amp_engine = AMPMatchingEngine(gsti_engine)

# ---------------------------------------------------------------------------
# STATE MANAGEMENT (SIMULATION LAYER)
# ---------------------------------------------------------------------------
# In-memory state is used intentionally in v1.0.0 to keep the system
# transparent, testable, and easy to reason about.
#
# Production deployments should replace these structures with:
# • PostgreSQL (long-term persistence)
# • Redis (ephemeral / real-time state)
# • Event streams (future intelligence extensions)
#
# The intelligence engines below are storage-agnostic by design.

CANDIDATE_DB: List[Candidate] = []
MARKET_STATE: Dict[str, Any] = {}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """API health check and info"""
    return {
        "status": "operational",
        "api": "AMP-GSTI Unified Intelligence",
        "version": "1.0.0",
        "endpoints": {
            "market": "/market/gsti",
            "candidates": "/candidates/query",
            "system": "/system/status"
        }
    }

@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

# ---------- MARKET INTELLIGENCE ----------

@app.post("/market/gsti/update")
def update_gsti(
    gold_price: float = Query(..., description="Current gold price (USD/oz)", gt=0),
    silver_price: float = Query(..., description="Current silver price (USD/oz)", gt=0),
    CR: float = Query(0.85, description="Customer Retention"),
    ES: float = Query(0.75, description="Employee Satisfaction"),
    BT: float = Query(0.80, description="Brand Trust"),
    RG: float = Query(1.05, description="Revenue Growth factor"),
    NCB: float = Query(0.1, description="Net Customer Backlash"),
    CS: float = Query(0.90, description="Customer Satisfaction"),
    BR: float = Query(0.85, description="Brand Reputation"),
    CA: float = Query(0.70, description="Customer Advocacy"),
    SS: float = Query(0.80, description="Service Speed"),
    NCB_consumer: float = Query(0.05, description="Consumer Backlash"),
    VIX: float = Query(20.0, description="Market volatility index"),
    M_A_Surges: bool = Query(False, description="M&A activity surge flag")
):
    """
    Update GSTI metrics with current market data
    Returns: Current market regime and intelligence
    """
    try:
        # Calculate goodwill components
        G = gsti_engine.calculate_general_goodwill(CR, ES, BT, RG, 1.0, NCB, 1.0)
        CG = gsti_engine.calculate_consumer_goodwill(CS, BR, CA, SS, NCB_consumer)
        UGS = gsti_engine.calculate_ugs(G, CG, 1.0)
        
        # Apply dynamic weighting
        gsti_engine.dynamic_weighting_adjustment(VIX, M_A_Surges)
        
        # Calculate GSTI
        metrics = gsti_engine.calculate_gsti(gold_price, silver_price)
        
        # Store in global state
        global MARKET_STATE
        MARKET_STATE = {
            **metrics,
            "gold_price": gold_price,
            "silver_price": silver_price,
            "general_goodwill": G,
            "consumer_goodwill": CG,
            "unified_goodwill_score": UGS,
            "vix": VIX
        }
        
        return {
            "status": "success",
            "message": "GSTI metrics updated",
            "data": MARKET_STATE
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GSTI calculation error: {str(e)}")

@app.get("/market/gsti")
def get_gsti_metrics():
    """Get current GSTI market intelligence"""
    if not MARKET_STATE:
        raise HTTPException(status_code=404, detail="No GSTI data available. Update market data first.")
    return {
        "status": "success",
        "data": MARKET_STATE
    }

@app.get("/market/regime")
def get_market_regime():
    """Get current market regime classification"""
    if not MARKET_STATE:
        raise HTTPException(status_code=404, detail="No market data available")
    
    regime = MARKET_STATE.get("market_regime", "unknown")
    gsti = MARKET_STATE.get("gsti_score", 0)
    
    recommendations = {
        MarketRegime.BULLISH: {
            "hiring_strategy": "aggressive_growth",
            "prioritize": ["innovation", "growth_potential", "risk_taking"],
            "rationale": "Market confidence high - invest in transformative talent"
        },
        MarketRegime.BEARISH: {
            "hiring_strategy": "defensive_stability",
            "prioritize": ["loyalty", "proven_performance", "crisis_management"],
            "rationale": "Market fear elevated - secure reliable, stable talent"
        },
        MarketRegime.NEUTRAL: {
            "hiring_strategy": "balanced",
            "prioritize": ["versatility", "adaptability", "core_competencies"],
            "rationale": "Market equilibrium - maintain strategic flexibility"
        }
    }
    
    return {
        "status": "success",
        "regime": regime,
        "gsti_score": gsti,
        "recommendations": recommendations.get(regime, {})
    }

# ---------- CANDIDATE MANAGEMENT ----------

@app.post("/candidates/register")
def register_candidate(candidate: Candidate):
    """Register a new candidate with SBT credentials"""
    global CANDIDATE_DB
    
    # Check for duplicate wallet
    if any(c.wallet_address == candidate.wallet_address for c in CANDIDATE_DB):
        raise HTTPException(status_code=400, detail="Wallet address already registered")
    
    CANDIDATE_DB.append(candidate)
    return {
        "status": "success",
        "message": "Candidate registered",
        "wallet_address": candidate.wallet_address,
        "token_count": len(candidate.tokens)
    }

@app.post("/candidates/query")
def query_candidates(query: HiringQuery):
    """
    Query candidates using Zero-Knowledge Proofs and GSTI-adjusted scoring
    Returns: Anonymous matched candidates ranked by regime-adjusted predictive score
    """
    if not CANDIDATE_DB:
        return {
            "status": "success",
            "message": "No candidates in database",
            "matches": []
        }
    
    # Get current GSTI metrics if available
    gsti_metrics = MARKET_STATE if MARKET_STATE else None
    
    # Execute matching
    matches = amp_engine.match_candidates(CANDIDATE_DB, query, gsti_metrics)
    
    return {
        "status": "success",
        "query": query.dict(),
        "market_regime": gsti_metrics.get("market_regime") if gsti_metrics else "unknown",
        "regime_adjustment_applied": query.consider_market_regime and gsti_metrics is not None,
        "total_candidates_screened": len(CANDIDATE_DB),
        "matches_found": len(matches),
        "matches": matches
    }

@app.get("/candidates/stats")
def get_candidate_stats():
    """Get aggregate candidate pool statistics (anonymized)"""
    if not CANDIDATE_DB:
        return {"status": "success", "total_candidates": 0}
    
    # Aggregate anonymous statistics
    token_distribution = defaultdict(int)
    avg_experience = np.mean([c.years_experience for c in CANDIDATE_DB])
    avg_score = np.mean([c.base_predictive_score for c in CANDIDATE_DB])
    
    for candidate in CANDIDATE_DB:
        for token in candidate.tokens:
            token_distribution[f"{token.type}:{token.name}"] += 1
    
    return {
        "status": "success",
        "total_candidates": len(CANDIDATE_DB),
        "average_experience": round(avg_experience, 2),
        "average_predictive_score": round(avg_score, 2),
        "token_distribution": dict(token_distribution),
        "privacy_note": "All data anonymized and aggregated"
    }

# ---------- SYSTEM MANAGEMENT ----------

@app.get("/system/status")
def system_status():
    """Get complete system status"""
    return {
        "status": "operational",
        "components": {
            "gsti_engine": {
                "initialized": True,
                "historical_data_points": len(gsti_engine._historical_ugs),
                "current_weights": {
                    "w_goodwill": gsti_engine.w_goodwill,
                    "w_gsr": gsti_engine.w_gsr
                }
            },
            "amp_engine": {
                "initialized": True,
                "candidates_registered": len(CANDIDATE_DB)
            },
            "market_intelligence": {
                "gsti_data_available": bool(MARKET_STATE),
                "current_regime": MARKET_STATE.get("market_regime", "unknown") if MARKET_STATE else "unknown"
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/system/reset")
def reset_system(confirm: bool = Query(False)):
    """Reset all system state (use with caution)"""
    if not confirm:
        raise HTTPException(status_code=400, detail="Must confirm reset with ?confirm=true")
    
    global CANDIDATE_DB, MARKET_STATE
    CANDIDATE_DB = []
    MARKET_STATE = {}
    gsti_engine._historical_ugs = []
    
    return {
        "status": "success",
        "message": "System reset complete",
        "timestamp": datetime.utcnow().isoformat()
    }

# ---------- INTELLIGENCE ENDPOINTS ----------

@app.get("/intelligence/hiring-forecast")
def hiring_forecast():
    """
    Generate hiring strategy forecast based on current market regime
    """
    if not MARKET_STATE:
        raise HTTPException(status_code=404, detail="No market data available")
    
    regime = MARKET_STATE.get("market_regime")
    gsti = MARKET_STATE.get("gsti_score", 0)
    gsr = MARKET_STATE.get("gsr", 0)
    
    # Generate forecast
    forecast = {
        "current_regime": regime,
        "gsti_score": gsti,
        "gold_silver_ratio": gsr,
        "forecast_horizon": "3-6 months",
        "confidence_level": "moderate"
    }
    
    if regime == MarketRegime.BULLISH:
        forecast["recommendation"] = "Accelerate hiring for growth roles"
        forecast["risk_factors"] = ["Potential overheating", "Wage inflation"]
        forecast["opportunity"] = "High - capture market share through talent acquisition"
        
    elif regime == MarketRegime.BEARISH:
        forecast["recommendation"] = "Defensive hiring - focus on retention and critical roles"
        forecast["risk_factors"] = ["Economic downturn", "Budget constraints"]
        forecast["opportunity"] = "Moderate - acquire undervalued senior talent"
        
    else:
        forecast["recommendation"] = "Maintain current hiring pace with strategic flexibility"
        forecast["risk_factors"] = ["Market uncertainty"]
        forecast["opportunity"] = "Moderate - balanced approach"
    
    return {
        "status": "success",
        "forecast": forecast
    }

@app.get("/intelligence/talent-flow")
def talent_flow_analysis():
    """
    Analyze aggregate talent flow patterns as economic indicator
    (All data anonymized)
    """
    if not CANDIDATE_DB:
        return {
            "status": "success",
            "message": "Insufficient data for analysis",
            "signals": []
        }
    
    # Aggregate signals
    total_loyalty_tokens = sum(
        1 for c in CANDIDATE_DB 
        for t in c.tokens 
        if t.type == SBTType.LOYALTY
    )
    
    total_skill_tokens = sum(
        1 for c in CANDIDATE_DB 
        for t in c.tokens 
        if t.type == SBTType.SKILL
    )
    
    avg_tokens_per_candidate = np.mean([len(c.tokens) for c in CANDIDATE_DB])
    
    # Generate signals
    signals = []
    
    loyalty_ratio = total_loyalty_tokens / len(CANDIDATE_DB) if CANDIDATE_DB else 0
    if loyalty_ratio < 0.3:
        signals.append({
            "signal": "LOW_LOYALTY_CONCENTRATION",
            "severity": "warning",
            "interpretation": "Potential workforce instability - increased churn risk"
        })
    
    skill_ratio = total_skill_tokens / len(CANDIDATE_DB) if CANDIDATE_DB else 0
    if skill_ratio > 3.0:
        signals.append({
            "signal": "HIGH_UPSKILLING_ACTIVITY",
            "severity": "positive",
            "interpretation": "Workforce adapting to market changes - resilience indicator"
        })
    
    return {
        "status": "success",
        "metrics": {
            "average_tokens_per_candidate": round(avg_tokens_per_candidate, 2),
            "loyalty_concentration": round(loyalty_ratio, 2),
            "skill_concentration": round(skill_ratio, 2)
        },
        "signals": signals,
        "economic_interpretation": "Aggregate talent metrics can predict labor market shifts"
    }

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/docs/examples")
def api_examples():
    """Get example API calls and workflows"""
    return {
        "workflow_1_update_market": {
            "description": "Update GSTI with current market data",
            "endpoint": "POST /market/gsti/update",
            "example": "?gold_price=2500&silver_price=25&VIX=30"
        },
        "workflow_2_register_candidate": {
            "description": "Register candidate with SBT credentials",
            "endpoint": "POST /candidates/register",
            "example_body": {
                "wallet_address": "0x1234...abcd",
                "tokens": [
                    {"type": "skill", "name": "Python Mastery", "issuer": "Tech Board", "issue_date": "2024-01"}
                ],
                "years_experience": 5,
                "base_predictive_score": 85
            }
        },
        "workflow_3_query_candidates": {
            "description": "Query candidates with ZK-proof matching",
            "endpoint": "POST /candidates/query",
            "example_body": {
                "required_skills": ["Python Mastery"],
                "min_predictive_score": 80,
                "consider_market_regime": True
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
