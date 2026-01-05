from fastapi import APIRouter, Query

from src.features.analysis.overspending.model.overspending_response import (
    OverspendingPatternsResponse,
    RecurringPatternsResponse,
    TimeBasedPatternsResponse,
)

from src.features.analysis.overspending.service.overspending_service import analyze_overspending
from src.features.analysis.overspending.service.recurring_service import analyze_recurring
from src.features.analysis.overspending.service.time_analysis_service import analyze_time_based_spending


analysis_router = APIRouter(prefix="/analysis", tags=["과소비"])

@analysis_router.get("/overspending", response_model=OverspendingPatternsResponse)
def get_overspending_patterns(
    year: int | None = Query(None, description="조회할 연도"),
    month: int | None = Query(None, ge=1, le=12, description="조회할 월"),
    start_date: str | None = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="종료일 (YYYY-MM-DD)"),
):
    """과소비 패턴 분석"""
    patterns = analyze_overspending(year=year, month=month, start_date=start_date, end_date=end_date)
    return OverspendingPatternsResponse(count=len(patterns), patterns=patterns)

@analysis_router.get("/recurring", response_model=RecurringPatternsResponse)
def get_recurring_patterns(
    year: int | None = Query(None, description="조회할 연도"),
    month: int | None = Query(None, ge=1, le=12, description="조회할 월"),
    min_count: int = Query(3, ge=1, description="최소 반복 횟수"),
):
    """반복 소비 패턴 분석"""
    patterns = analyze_recurring(year=year, month=month, min_count=min_count)
    return RecurringPatternsResponse(count=len(patterns), patterns=patterns)


@analysis_router.get("/time-based", response_model=TimeBasedPatternsResponse)
def get_time_based_patterns(
    year: int | None = Query(None, description="조회할 연도"),
    month: int | None = Query(None, ge=1, le=12, description="조회할 월"),
):
    """시간대 소비 분석 (충동 지점)"""
    patterns = analyze_time_based_spending(year=year, month=month)
    return TimeBasedPatternsResponse(count=len(patterns), patterns=patterns)