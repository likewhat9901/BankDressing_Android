import pandas as pd
import logging

from src.features.analysis.overspending.model.overspending_response import OverspendingPattern
from src.features.analysis.overspending.util.data_preparation import prepare_expense_data
from src.features.analysis.overspending.util.data_enrichment import enrich_with_analysis_data
from src.features.analysis.overspending.util.rule_filter import filter_by_rule
from src.features.analysis.overspending.util.overspending_checkers import (
    check_weekly_count,
    check_monthly_count,
    check_monthly_total,
    check_per_transaction,
)
from src.features.analysis.overspending.repository.rule_repository import load_rules_from_file


logger = logging.getLogger(__name__)


# --------------------------------
# public functions
# --------------------------------
def analyze_overspending(
    year: int | None = None,
    month: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[OverspendingPattern]:
    """과소비 패턴 분석"""
    # 공통 데이터 준비
    df = prepare_expense_data(year, month, start_date, end_date)
    if df.empty:
        return []

    # 시간, 주, 월 데이터 추가
    df = enrich_with_analysis_data(df)
    
    # 과소비 패턴 분석
    results = _analyze_overspending_patterns(df)
    
    logger.info(f"과소비 패턴 {len(results)}건 감지")
    return results


# --------------------------------
# private functions
# --------------------------------
def _analyze_overspending_patterns(df: pd.DataFrame) -> list[OverspendingPattern]:
    """과소비 패턴 분석"""
    # 과소비 규칙 조회
    rules = load_rules_from_file(include_disabled=False)
    # 과소비 패턴 리스트
    results = []
    for rule in rules:
        pattern = _check_overspending(df, rule)
        if pattern:
            results.append(pattern)
    
    return results


def _check_overspending(df: pd.DataFrame, rule: dict) -> OverspendingPattern | None:
    """범용 과소비 체크 함수"""
    # 데이터 필터링
    filtered_df = filter_by_rule(df, rule)
    if filtered_df.empty:
        return None

    # 총액 계산
    total_amount = int(filtered_df["금액"].sum())
    # 이유 리스트
    reasons = []
    
    # 조건 체크 함수들을 딕셔너리로 관리
    checkers = {
        'weekly_count': check_weekly_count,
        'monthly_count': check_monthly_count,
        'monthly_total': check_monthly_total,
        'per_transaction': check_per_transaction,
    }
    
    # 각 조건 체크
    for key, checker in checkers.items():
        if key in rule:
            reason = checker(filtered_df, rule[key], rule.get('name', ''))
            if reason:
                reasons.append(reason)

    if not reasons:
        return None
    
    # 과소비 패턴 반환
    return OverspendingPattern(
        category=rule["name"],
        total_amount=total_amount,
        reasons=reasons
    )
