import logging

from src.core.utils.date_utils import parse_date_params
from src.core.utils.dataframe_utils import filter_by_date_range
from src.features.transaction.repository.transaction_repository import load_transactions
from src.features.saving.service.savings_profile import analyze_user_profile, calculate_dynamic_thresholds
from src.features.saving.service.saving_opportunities import (
    analyze_recurring_opportunities,
    analyze_overspending_opportunities,
    analyze_category_opportunities,
)

logger = logging.getLogger(__name__)


def analyze_savings_opportunities(
    year: int | None = None,
    month: int | None = None,
) -> list[dict]:
    """절약 기회 분석 (Top 3)"""
    # 거래내역 조회
    df = load_transactions()
    if df.empty:
        return []
    
    # 사용자 프로필 분석 및 동적 기준 계산
    profile = analyze_user_profile(df)
    thresholds = calculate_dynamic_thresholds(profile, df)
    
    # 날짜 파라미터 파싱
    start_date, end_date = parse_date_params(year, month)
    
    # 필터링된 데이터
    df_filtered = filter_by_date_range(df, start_date, end_date)
    if df_filtered.empty:
        return []
    
    opportunities = []
    
    # 1. 반복 소비 패턴 기반 절약 기회
    opportunities.extend(
        analyze_recurring_opportunities(year, month, profile, thresholds)
    )
    
    # 2. 과소비 패턴 기반 절약 기회
    opportunities.extend(
        analyze_overspending_opportunities(start_date, end_date, profile, thresholds)
    )
    
    # 3. 카테고리별 초과 지출 기반 절약 기회
    opportunities.extend(
        analyze_category_opportunities(df_filtered, start_date, end_date, profile, thresholds)
    )
    
    # 절약 가능 금액 기준 내림차순 정렬 후 Top 3
    opportunities.sort(key=lambda x: x["savings_amount"], reverse=True)
    top3 = opportunities[:3]
    
    logger.info(f"절약 기회 {len(top3)}건 추천")
    return top3
