from fastapi import APIRouter, Query

from src.features.saving.service.saving_service import analyze_savings_opportunities
from src.features.saving.model.saving import (
    SavingsOpportunitiesResponse,
)


saving_router = APIRouter(prefix="/saving", tags=["절약"])

# 절약 기회 분석 (Top 3)
@saving_router.get("/opportunities")
def get_savings_opportunities(
    year: int | None = Query(None, description="조회할 연도"),
    month: int | None = Query(None, ge=1, le=12, description="조회할 월"),
) -> SavingsOpportunitiesResponse:
    """절약 기회 분석 (Top 3)"""
    opportunities = analyze_savings_opportunities(
        year=year,
        month=month,
    )
    return SavingsOpportunitiesResponse(
        count=len(opportunities), 
        opportunities=opportunities
    )
