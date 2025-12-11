from pydantic import BaseModel
from enum import Enum

class MarketRegime(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class MarketUpdate(BaseModel):
    gold_price: float
    silver_price: float
    CR: float = 0.85
    ES: float = 0.75
    BT: float = 0.80
    RG: float = 1.05
    NCB: float = 0.1
    CS: float = 0.90
    BR: float = 0.85
    CA: float = 0.70
    SS: float = 0.80
    NCB_consumer: float = 0.05
    VIX: float = 20.0
    M_A_Surges: bool = False

class GSTIMetrics(BaseModel):
    gold_price: float
    silver_price: float
    gsr: float
    goodwill_momentum: float
    gsti_score: float
    market_regime: MarketRegime
    timestamp: str
