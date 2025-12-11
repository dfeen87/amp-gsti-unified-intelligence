from pydantic import BaseModel, Field
from typing import List, Dict, Any

class HiringQuery(BaseModel):
    required_skills: List[str] = []
    required_character: List[str] = []
    required_loyalty: List[str] = []
    min_predictive_score: float = Field(default=70, ge=0, le=100)
    consider_market_regime: bool = Field(default=True)

class QueryResult(BaseModel):
    wallet_address: str
    base_score: float
    regime_adjusted_score: float
    regime_adjustment: float
    token_count: int
    years_experience: int
    zk_proof_verified: bool
