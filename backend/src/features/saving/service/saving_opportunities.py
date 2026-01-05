"""절약 기회 생성 로직"""
import pandas as pd
import logging
from typing import Dict, List

from src.features.analysis.overspending.model.overspending_response import OverspendingPattern
from src.core.utils.dataframe_utils import filter_by_date_range, filter_expense_only
from src.features.analysis.overspending.service.recurring_service import analyze_recurring
from src.features.analysis.overspending.service.overspending_service import analyze_overspending

logger = logging.getLogger(__name__)


# ============================================================
# 반복 소비 기회
# ============================================================
def analyze_recurring_opportunities(
    year: int | None,
    month: int | None,
    profile: Dict,
    thresholds: Dict
) -> List[dict]:
    """반복 소비 패턴 기반 절약 기회"""
    opportunities = []
    patterns = analyze_recurring(year=year, month=month, min_count=3)
    
    for pattern in patterns:
        opportunity = create_recurring_opportunity(pattern, profile, thresholds)
        if opportunity:
            opportunities.append(opportunity)
    
    return opportunities


def create_recurring_opportunity(
    pattern: dict,
    profile: Dict,
    thresholds: Dict
) -> dict | None:
    """반복 소비 패턴에서 절약 기회 생성"""
    count = pattern["count"]
    average_amount = pattern["average_amount"]
    
    # 동적 기준 적용
    if count < thresholds["recurring_min_frequency"]:
        return None
    
    user_avg_frequency = profile.get("avg_monthly_count", 10)
    recommended_frequency = min(
        max(2, int(user_avg_frequency * 0.8)),
        max(2, int(count * thresholds["recurring_reduction_ratio"]))
    )
    
    savings_amount = average_amount * (count - recommended_frequency)
    
    if savings_amount <= thresholds["min_savings_amount"]:
        return None
    
    return {
        "type": "recurring",
        "title": f"{pattern['merchant']} 반복 소비 줄이기",
        "description": f"월 {count}회 → 월 {recommended_frequency}회로 줄이면",
        "current_amount": pattern["total_amount"],
        "savings_amount": int(savings_amount),
        "category": pattern["category"],
        "merchant": pattern["merchant"],
        "current_frequency": count,
        "recommended_frequency": recommended_frequency,
    }


# ============================================================
# 과소비 기회
# ============================================================
def analyze_overspending_opportunities(
    start_date: str | None,
    end_date: str | None,
    profile: Dict,
    thresholds: Dict
) -> List[dict]:
    """과소비 패턴 기반 절약 기회"""
    opportunities = []
    patterns = analyze_overspending(start_date=start_date, end_date=end_date)
    
    for pattern in patterns:
        opportunity = create_overspending_opportunity(pattern, profile, thresholds)
        if opportunity:
            opportunities.append(opportunity)
    
    return opportunities


def create_overspending_opportunity(
    pattern: OverspendingPattern,
    profile: Dict,
    thresholds: Dict
) -> dict | None:
    """과소비 패턴에서 절약 기회 생성"""
    total_amount = pattern.total_amount
    savings_amount = int(total_amount * thresholds["overspending_savings_ratio"])
    
    if savings_amount <= thresholds["min_savings_amount"]:
        return None

    reasons_text = ", ".join([r.message for r in pattern.reasons])
    
    return {
        "type": "overspending",
        "title": f"{pattern.category} 과소비 줄이기",
        "description": "과소비 규칙을 지키면 ({reasons_text})",
        "current_amount": total_amount,
        "savings_amount": savings_amount,
        "category": pattern.category,
        "reasons": [{"type": r.type, "message": r.message} for r in pattern.reasons],
    }


# ============================================================
# 카테고리 기회
# ============================================================
def analyze_category_opportunities(
    df: pd.DataFrame,
    start_date: str | None,
    end_date: str | None,
    profile: Dict,
    thresholds: Dict
) -> List[dict]:
    """카테고리별 초과 지출 기반 절약 기회"""
    df = filter_by_date_range(df, start_date, end_date)
    if df.empty:
        return []
    
    df = filter_expense_only(df)
    
    category_stats = calculate_category_stats(df)
    overall_avg = df["금액"].abs().mean()
    
    opportunities = []
    for _, row in category_stats.iterrows():
        opportunity = create_category_opportunity(row, overall_avg, profile, thresholds)
        if opportunity:
            opportunities.append(opportunity)
    
    return opportunities


def calculate_category_stats(df: pd.DataFrame) -> pd.DataFrame:
    """카테고리별 통계 계산"""
    stats = df.groupby("대분류").agg({
        "금액": ["sum", "mean", "count"]
    }).reset_index()
    stats.columns = ["category", "total", "average", "count"]
    return stats


def create_category_opportunity(
    row: pd.Series,
    overall_avg: float,
    profile: Dict,
    thresholds: Dict
) -> dict | None:
    """카테고리 통계에서 절약 기회 생성"""
    category = row["category"]
    category_avg = row["average"]
    count = int(row["count"])
    
    # 사용자 카테고리 평균 가져오기
    user_category_avg = profile.get("category_avgs", {}).get(category, overall_avg)
    
    # 동적 기준 적용
    if category_avg <= user_category_avg * thresholds["category_multiplier"]:
        return None
    
    if count < thresholds["category_min_count"]:
        return None
    
    excess_amount = (category_avg - user_category_avg) * count
    savings_amount = int(excess_amount * thresholds["category_savings_ratio"])
    
    if savings_amount <= thresholds["min_savings_amount"]:
        return None
    
    return {
        "type": "category",
        "title": f"{category} 지출 줄이기",
        "description": f"평균 거래액을 {int(user_category_avg):,}원으로 줄이면",
        "current_amount": int(row["total"]),
        "savings_amount": savings_amount,
        "category": category,
        "current_avg": int(category_avg),
        "recommended_avg": int(user_category_avg),
    }