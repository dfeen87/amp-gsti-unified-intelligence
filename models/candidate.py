from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class SBTType(str, Enum):
    SKILL = "skill"
    CHARACTER = "character"
    LOYALTY = "loyalty"
    PROJECT = "project"
    CERTIFICATION = "certification"

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
