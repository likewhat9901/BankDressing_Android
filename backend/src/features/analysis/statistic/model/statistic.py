from pydantic import BaseModel
from typing import List


# ============================================================
# API 응답 모델
# ============================================================
class CategoryBreakdown(BaseModel):
    """카테고리별 breakdown 항목"""
    category: str
    amount: int
    percentage: float


class MonthlyStatsResponse(BaseModel):
    """월별 통계 응답"""
    month: str
    total_income: int
    total_expense: int
    balance: int
    income_count: int
    expense_count: int
    income_breakdown: List[CategoryBreakdown]
    expense_breakdown: List[CategoryBreakdown]