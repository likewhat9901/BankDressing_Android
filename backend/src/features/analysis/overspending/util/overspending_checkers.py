import pandas as pd
from src.features.analysis.overspending.model.overspending_response import OverspendingReason


def make_reason(type_: str, count: int, message: str) -> OverspendingReason:
    """reason 객체 생성"""
    return OverspendingReason(type=type_, count=count, message=message)


def check_weekly_count(df: pd.DataFrame, threshold: int, rule_name: str) -> OverspendingReason | None:
    """주별 빈도 체크"""
    weekly_counts = df.groupby("week").size()
    high_freq = weekly_counts[weekly_counts >= threshold]
    if len(high_freq) > 0:
        return make_reason(
            "high_frequency",
            int(weekly_counts.sum()),
            f"주 {threshold}회 이상 ({len(high_freq)}주)"
        )
    return None


def check_monthly_count(df: pd.DataFrame, threshold: int, rule_name: str) -> OverspendingReason | None:
    """월별 빈도 체크"""
    monthly_counts = df.groupby("month").size()
    high_freq = monthly_counts[monthly_counts >= threshold]
    if len(high_freq) > 0:
        return make_reason(
            "high_frequency",
            int(monthly_counts.sum()), 
            f"월 {threshold}회 이상 ({len(high_freq)}개월)"
        )
    return None


def check_monthly_total(df: pd.DataFrame, threshold: int, rule_name: str) -> OverspendingReason | None:
    """월별 총액 체크"""
    monthly_total = df.groupby("month")["금액"].sum()
    high_months = monthly_total[monthly_total >= threshold]
    if len(high_months) > 0:
        return make_reason(
            "high_monthly",
            len(df),
            f"월 총액 {threshold:,}원 초과 ({len(high_months)}개월)"
        )
    return None


def check_per_transaction(df: pd.DataFrame, threshold: int, rule_name: str) -> OverspendingReason | None:
    """건당 고액 체크"""
    expensive = df[df["금액"] >= threshold]
    if len(expensive) > 0:
        return make_reason(
            "high_amount",
            len(expensive),
            f"건당 {threshold:,}원 이상 ({len(expensive)}건)"
        )
    return None