import pandas as pd

import logging
from src.core.utils.date_utils import parse_date_params
from src.core.utils.dataframe_utils import (
    filter_by_date_range,
    filter_expense_only,
    validate_datetime_column,
)
from src.features.transaction.repository.transaction_repository import load_transactions

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------
# public functions
# ----------------------------------------------------------------
def analyze_time_based_spending(
    year: int | None = None,
    month: int | None = None,
) -> list[dict]:
    """시간대 소비 분석 (충동 지점 탐지)"""
    # 데이터 로드
    df = load_transactions()
    if df.empty:
        return []
    
    # 데이터 준비
    # 날짜 파라미터 파싱
    start_date, end_date = parse_date_params(year, month)
    # 날짜 필터링
    df = filter_by_date_range(df, start_date, end_date)
    if df.empty:
        return []
    
    # 지출 데이터만 필터링
    df = filter_expense_only(df)
    if df.empty:
        return []
    
    # 거래일시 데이터 타입 검증
    validate_datetime_column(df)
    # 시간, 요일, 일자, 주말 여부 데이터 추가
    df = _enrich_with_extended_time_data(df)
    
    # 시간대별 소비 패턴 분석
    patterns = []
    patterns.extend(_analyze_time_patterns(df))

    # 월초 패턴 분석
    early_month = _analyze_early_month_pattern(df)
    if early_month:
        patterns.append(early_month)
    
    # 주말 저녁 패턴 분석
    weekend = _analyze_weekend_pattern(df)
    if weekend:
        patterns.append(weekend)
    
    # 총액 기준 내림차순 정렬 (내림차순 정렬)
    patterns.sort(key=lambda x: x["total_amount"], reverse=True)
    
    logger.info(f"시간대 소비 패턴 {len(patterns)}건 감지")
    return patterns


# ----------------------------------------------------------------
# private functions - Data Enrichment
# ----------------------------------------------------------------
def _enrich_with_extended_time_data(df: pd.DataFrame) -> pd.DataFrame:
    """시간, 요일, 일자, 주말 여부 데이터 추가 (time_analysis 전용)"""
    df["hour"] = df["거래일시"].dt.hour
    df["day_of_week"] = df["거래일시"].dt.dayofweek
    df["day"] = df["거래일시"].dt.day
    df["is_weekend"] = df["day_of_week"].isin([5, 6])
    return df


# ----------------------------------------------------------------
# private functions - Pattern Analysis
# ----------------------------------------------------------------
def _analyze_time_patterns(df: pd.DataFrame) -> list[dict]:
    """시간대별 소비 패턴 분석"""
    # 시간대별 패턴 리스트
    time_ranges = [
        {"name": "새벽", "start": 0, "end": 6, "icon": "🌙"},
        {"name": "오전", "start": 6, "end": 12, "icon": "☀️"},
        {"name": "오후", "start": 12, "end": 18, "icon": "🌤️"},
        {"name": "저녁", "start": 18, "end": 22, "icon": "🌆"},
        {"name": "야간", "start": 22, "end": 24, "icon": "🌃"},
    ]
    
    patterns = []
    # 시간대별 패턴 리스트 순회
    for tr in time_ranges:
        # 시간대별 패턴 생성
        pattern = _create_time_range_pattern(df, tr)
        # 시간대별 패턴이 있으면 패턴 리스트에 추가
        if pattern:
            patterns.append(pattern)
    
    return patterns


def _create_time_range_pattern(df: pd.DataFrame, time_range: dict) -> dict | None:
    """시간대별 패턴 생성"""
    # 시간대별 패턴 시작 시간과 종료 시간
    start, end = time_range["start"], time_range["end"]
    
    # 시간대별 패턴 시작 시간과 종료 시간이 24시인 경우
    if end == 24:
        # 시간대별 패턴 시작 시간과 종료 시간이 24시인 경우
        filtered = df[(df["hour"] >= start) & (df["hour"] < 24)]
    else:
        # 시간대별 패턴 시작 시간과 종료 시간이 24시가 아닌 경우
        filtered = df[(df["hour"] >= start) & (df["hour"] < end)]
    
    # 시간대별 패턴 필터링 결과가 없으면 패턴 생성 실패 반환
    if filtered.empty:
        return None
    
    # 시간대별 패턴 필터링 결과 거래 횟수
    count = len(filtered)
    # 시간대별 패턴 필터링 결과 총 금액
    total_amount = int(filtered["금액"].sum())
    
    # 시간대별 패턴 반환
    return {
        "type": "time_range",
        "name": f"{time_range['icon']} {time_range['name']} ({start:02d}~{end:02d}시)",
        "description": f"{time_range['name']} 시간대 소비",
        "count": count,
        "total_amount": total_amount,
        "average_amount": int(total_amount / count) if count > 0 else 0,
        "time_range": f"{start:02d}~{end:02d}",
    }


def _analyze_early_month_pattern(df: pd.DataFrame) -> dict | None:
    """월 초 패턴 분석 (1~5일)"""
    # 월 초 패턴 필터링
    early_month = df[df["day"] <= 5]
    
    # 월 초 패턴 필터링 결과가 없으면 패턴 생성 실패 반환
    if early_month.empty:
        return None
    
    # 월 초 패턴 필터링 결과 거래 횟수
    count = len(early_month)
    # 월 초 패턴 필터링 결과 총 금액
    total_amount = int(early_month["금액"].sum())
    
    # 월 초 패턴 반환
    return {
        "type": "early_month",
        "name": "💰 월초 (1~5일)",
        "description": "월초 3~5일간의 소비 패턴",
        "count": count,
        "total_amount": total_amount,
        "average_amount": int(total_amount / count) if count > 0 else 0,
        "days": "1~5일",
    }


def _analyze_weekend_pattern(df: pd.DataFrame) -> dict | None:
    """주말 저녁 패턴 분석 (18시 이후)"""
    # 주말 저녁 패턴 필터링
    weekend_evening = df[(df["is_weekend"] == True) & (df["hour"] >= 18)]
    
    # 주말 저녁 패턴 필터링 결과가 없으면 패턴 생성 실패 반환
    if weekend_evening.empty:
        return None
    
    # 주말 저녁 패턴 필터링 결과 거래 횟수
    count = len(weekend_evening)
    # 주말 저녁 패턴 필터링 결과 총 금액
    total_amount = int(weekend_evening["금액"].sum())
    
    # 주말 저녁 패턴 반환
    return {
        "type": "weekend_evening",
        "name": "🎉 주말 저녁",
        "description": "주말 저녁 시간대 소비",
        "count": count,
        "total_amount": total_amount,
        "average_amount": int(total_amount / count) if count > 0 else 0,
        "time_range": "18시 이후",
    }