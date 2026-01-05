from fastapi import APIRouter, Query

from src.features.analysis.statistic.model.statistic import MonthlyStatsResponse
from src.features.analysis.statistic.service.statistic_service import get_monthly_stats

statistic_router = APIRouter(prefix="/analysis/statistic", tags=["통계"])


@statistic_router.get("/monthly", response_model=MonthlyStatsResponse)
def monthly_stats(
    year: int = Query(..., description="조회할 연도", examples=[2024]),
    month: int = Query(..., ge=1, le=12, description="조회할 월 (1~12)", examples=[12])
):
    """월별 통계 조회"""
    return get_monthly_stats(year, month)