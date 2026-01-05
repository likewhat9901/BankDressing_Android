from fastapi import APIRouter, Query, HTTPException
import logging

from src.features.user.service.personality_service import analyze_spending_personality

logger = logging.getLogger(__name__)

personality_router = APIRouter(prefix="/user/personality", tags=["소비 성향"])

@personality_router.get("")
def get_spending_personality(
    year: int | None = Query(None, description="조회할 연도"),
    month: int | None = Query(None, ge=1, le=12, description="조회할 월"),
):
    """소비 성향 분석"""
    try:
        personality = analyze_spending_personality(year=year, month=month)
        return personality
    except Exception as e:
        logger.error(f"소비 성향 분석 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"소비 성향 분석 중 오류가 발생했습니다: {str(e)}")