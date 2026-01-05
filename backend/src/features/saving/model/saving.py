from pydantic import BaseModel
from typing import Optional


# ============================================================
# 도메인 모델 (비즈니스 로직용)
# ============================================================
class SavingsOpportunity(BaseModel):
    """절약 기회 모델"""
    type: str  # "recurring", "overspending", "category"
    title: str
    description: str
    current_amount: int
    savings_amount: int
    category: str
    merchant: Optional[str] = None
    current_frequency: Optional[int] = None
    recommended_frequency: Optional[int] = None


# ============================================================
# API 응답 모델
# ============================================================
class SavingsOpportunitiesResponse(BaseModel):
    """절약 기회 목록 응답"""
    count: int
    opportunities: list[dict]