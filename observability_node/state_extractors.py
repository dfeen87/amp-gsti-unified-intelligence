"""
Intelligence Engine State Extractors for Observability Node
============================================================

Provides read-only access to GSTI, AMP, and Forecast engine state.

All functions are read-only and do not trigger any scoring, matching,
or forecasting operations.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np


def get_gsti_state(db) -> Dict[str, Any]:
    """
    Extract current GSTI (Gold-Silver Trust Index) state.
    
    Args:
        db: Database instance
        
    Returns:
        Dictionary with current GSTI metrics
    """
    try:
        latest_metrics = db.get_latest_gsti_metrics()
        
        if not latest_metrics:
            return {
                "status": "no_data",
                "message": "No GSTI metrics available",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Extract key metrics
        return {
            "status": "available",
            "gold_silver_ratio": latest_metrics.get("gsr"),
            "volatility_index": "N/A",  # Would need VIX data from market state
            "economic_regime": latest_metrics.get("market_regime"),
            "confidence_score": latest_metrics.get("gsti_score"),
            "last_update": latest_metrics.get("timestamp"),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def get_amp_state(db) -> Dict[str, Any]:
    """
    Extract current AMP (Anonymous Merit Protocol) state.
    
    Args:
        db: Database instance
        
    Returns:
        Dictionary with AMP metrics (aggregated and anonymized)
    """
    try:
        stats = db.get_candidate_statistics()
        
        if stats.get("total_candidates", 0) == 0:
            return {
                "status": "no_data",
                "message": "No candidates registered",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get token distribution for credential weighting
        talent_metrics = db.get_talent_flow_metrics()
        token_dist = talent_metrics.get("token_distribution", {})
        
        # Calculate distribution of merit scores (aggregated)
        # This is anonymized - no individual scores
        all_candidates = db.get_all_candidates()
        scores = [c.base_predictive_score for c in all_candidates]
        
        score_distribution = {
            "min": round(float(np.min(scores)), 2),
            "max": round(float(np.max(scores)), 2),
            "mean": round(float(np.mean(scores)), 2),
            "median": round(float(np.median(scores)), 2),
            "std_dev": round(float(np.std(scores)), 2)
        } if scores else None
        
        # Credential weighting statistics (anonymized)
        credential_stats = _calculate_credential_stats(token_dist)
        
        return {
            "status": "available",
            "candidates_evaluated": stats.get("total_candidates"),
            "merit_score_distribution": score_distribution,
            "credential_weighting": credential_stats,
            "last_evaluation": "N/A",  # Would track from activity logs
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def get_forecast_state(db) -> Dict[str, Any]:
    """
    Extract forecast engine state and outlook.
    
    Args:
        db: Database instance
        
    Returns:
        Dictionary with hiring outlook and forecast indicators
    """
    try:
        # Get latest GSTI for regime context
        latest_gsti = db.get_latest_gsti_metrics()
        
        if not latest_gsti:
            return {
                "status": "no_data",
                "message": "No GSTI data for forecast generation",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        regime = latest_gsti.get("market_regime", "unknown")
        gsti_score = latest_gsti.get("gsti_score", 0)
        
        # Generate hiring outlook based on regime
        outlook = _generate_hiring_outlook(regime, gsti_score)
        
        # Get talent flow indicators
        talent_metrics = db.get_talent_flow_metrics()
        talent_flow = _analyze_talent_flow(talent_metrics)
        
        # Macroeconomic signals (from GSTI)
        macro_signals = {
            "gold_silver_ratio": latest_gsti.get("gsr"),
            "market_regime": regime,
            "goodwill_momentum": latest_gsti.get("goodwill_momentum", 0)
        }
        
        return {
            "status": "available",
            "hiring_outlook": outlook,
            "talent_flow_indicators": talent_flow,
            "macroeconomic_signals": macro_signals,
            "model_confidence": _calculate_model_confidence(latest_gsti),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def get_audit_summary(db, limit: int = 50) -> Dict[str, Any]:
    """
    Extract audit log summaries (anonymized, no PII).
    
    Args:
        db: Database instance
        limit: Number of recent audit entries to return
        
    Returns:
        Dictionary with audit summaries
    """
    try:
        logs = db.get_activity_logs(limit=limit)
        
        if not logs:
            return {
                "status": "no_data",
                "message": "No audit logs available",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Anonymize and summarize
        summaries = []
        mutation_counts = {}
        
        for log in logs:
            action = log.get("action", "unknown")
            
            # Count mutations
            if action in ["candidate_register", "gsti_update", "system_reset"]:
                mutation_counts[action] = mutation_counts.get(action, 0) + 1
            
            # Create summary (no PII)
            summaries.append({
                "action": action,
                "timestamp": log.get("timestamp"),
                "user_role": "admin" if log.get("user_id") else "anonymous"  # Simplified
            })
        
        return {
            "status": "available",
            "total_entries": len(logs),
            "recent_entries": summaries[:limit],
            "mutation_summary": mutation_counts,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _calculate_credential_stats(token_dist: Dict[str, int]) -> Dict[str, Any]:
    """Calculate aggregated credential statistics."""
    if not token_dist:
        return {"total_credential_types": 0}
    
    # Count by type
    type_counts = {}
    for key, count in token_dist.items():
        if ":" in key:
            cred_type = key.split(":")[0]
            type_counts[cred_type] = type_counts.get(cred_type, 0) + count
    
    return {
        "total_credential_types": len(token_dist),
        "credentials_by_type": type_counts,
        "most_common": max(token_dist.items(), key=lambda x: x[1])[0] if token_dist else None
    }


def _generate_hiring_outlook(regime: str, gsti_score: float) -> Dict[str, Any]:
    """Generate hiring outlook based on market regime."""
    outlooks = {
        "bullish": {
            "strategy": "aggressive_growth",
            "recommendation": "Accelerate hiring for growth roles",
            "risk_level": "moderate"
        },
        "bearish": {
            "strategy": "defensive_stability",
            "recommendation": "Focus on retention and critical roles",
            "risk_level": "elevated"
        },
        "neutral": {
            "strategy": "balanced",
            "recommendation": "Maintain current hiring pace",
            "risk_level": "low"
        }
    }
    
    return outlooks.get(regime, {
        "strategy": "unknown",
        "recommendation": "Insufficient data",
        "risk_level": "unknown"
    })


def _analyze_talent_flow(talent_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze talent flow indicators from aggregated metrics."""
    total_candidates = talent_metrics.get("total_candidates", 0)
    token_dist = talent_metrics.get("token_distribution", {})
    
    if total_candidates == 0:
        return {
            "signal": "insufficient_data",
            "interpretation": "Not enough candidates for flow analysis"
        }
    
    # Count loyalty tokens
    loyalty_count = sum(
        count for key, count in token_dist.items()
        if "loyalty:" in key
    )
    
    loyalty_ratio = loyalty_count / total_candidates if total_candidates > 0 else 0
    
    if loyalty_ratio < 0.3:
        signal = "potential_instability"
        interpretation = "Low loyalty concentration may indicate workforce churn risk"
    elif loyalty_ratio > 0.6:
        signal = "high_retention"
        interpretation = "Strong loyalty signals indicate stable workforce"
    else:
        signal = "balanced"
        interpretation = "Balanced loyalty distribution"
    
    return {
        "signal": signal,
        "interpretation": interpretation,
        "loyalty_ratio": round(loyalty_ratio, 2)
    }


def _calculate_model_confidence(gsti_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate model confidence based on data recency and completeness."""
    try:
        timestamp_str = gsti_metrics.get("timestamp")
        if not timestamp_str:
            return {"level": "low", "reason": "No timestamp available"}
        
        # Parse timestamp
        last_update = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        time_since_update = (datetime.utcnow() - last_update).total_seconds() / 3600  # hours
        
        if time_since_update < 1:
            confidence = "high"
        elif time_since_update < 24:
            confidence = "moderate"
        else:
            confidence = "low"
        
        return {
            "level": confidence,
            "hours_since_update": round(time_since_update, 2),
            "reason": f"Data is {round(time_since_update, 1)} hours old"
        }
    except Exception:
        return {"level": "unknown", "reason": "Could not assess data recency"}
