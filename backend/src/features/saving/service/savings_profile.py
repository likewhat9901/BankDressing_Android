"""사용자 소비 프로필 분석 및 동적 기준 계산"""
import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def analyze_user_profile(df: pd.DataFrame) -> Dict:
    """사용자 소비 프로필 분석"""\
    # 지출 데이터만 필터링
    expense_df = df[df["금액"] < 0].copy()
    if expense_df.empty:
        return {}

    # 금액을 절댓값으로 변환한 Series 생성
    expense_df_abs = expense_df["금액"].abs()
    
    profile = {
        # 금액 통계
        "avg_amount": expense_df_abs.mean(),                  # 평균 금액
        "median_amount": expense_df_abs.median(),             # 중앙값 금액
        "std_amount": expense_df_abs.std(),                   # 표준편차
        "p75_amount": expense_df_abs.quantile(0.75),          # 상위 25% 금액
        "p90_amount": expense_df_abs.quantile(0.90),          # 상위 10% 금액
        
        # 빈도 통계
        "avg_monthly_count": int(
            len(expense_df) / max(1, (expense_df["거래일시"].max() - expense_df["거래일시"].min()).days / 30)
        ),      # 월 평균 거래횟수
        "avg_daily_count": int(
            len(expense_df) / max(1, (expense_df["거래일시"].max() - expense_df["거래일시"].min()).days)
        ),      # 일 평균 거래횟수
        
        # 카테고리별 통계 - 수정: abs()를 먼저 적용한 후 groupby
        "category_medians": expense_df_abs.groupby(expense_df["대분류"]).median().to_dict(),      # 카테고리별 중앙값
        "category_avgs": expense_df_abs.groupby(expense_df["대분류"]).mean().to_dict(),           # 카테고리별 평균
    }
    
    return profile


def calculate_dynamic_thresholds(profile: Dict, df: pd.DataFrame) -> Dict:
    """사용자 데이터 기반 동적 기준 계산"""
    if not profile:
        # 기본값 반환
        return {
            "min_savings_amount": 10000,
            "recurring_min_frequency": 4,
            "category_multiplier": 1.5,
        }
    
    # 최소 절약 금액: 사용자 중앙값의 20% 또는 평균의 10% 중 큰값
    min_savings = max(
        5000,
        int(profile["median_amount"] * 0.2),
        int(profile["avg_amount"] * 0.1)
    )
    
    # 반복 소비 최소 빈도: 사용자 월 평균의 5%
    recurring_min = max(
        3,
        int(profile["avg_monthly_count"] * 0.05)
    )
    
    # 카테고리 배수: 분산에 따라 조정
    std_ratio = profile["std_amount"] / max(profile["avg_amount"], 1)
    if std_ratio > 1.5:
        category_multiplier = 1.3
    elif std_ratio > 1.0:
        category_multiplier = 1.4
    else:
        category_multiplier = 1.5
    
    return {
        "min_savings_amount": min_savings,
        "recurring_min_frequency": recurring_min,
        "recurring_reduction_ratio": 0.5,
        "overspending_savings_ratio": 0.3,
        "category_multiplier": category_multiplier,
        "category_min_count": 3,
        "category_savings_ratio": 0.2,
    }