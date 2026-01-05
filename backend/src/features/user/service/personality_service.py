"""
소비 성향 분석 서비스

분석 흐름:
1. 거래 데이터 로드
2. 점수 계산 (2개 축: planning, saving) - df만으로 계산
3. 유형 결정 (4개 유형: ANT, FOX, SQUIRREL, LION)
4. 응답 구성
"""
import pandas as pd
import logging

from src.features.user.repository.personality_repository import (
    load_expense_transactions,
    get_personality,
)

logger = logging.getLogger(__name__)


# ============================================================
# Public API
# ============================================================
def analyze_spending_personality(
    year: int | None = None,
    month: int | None = None,
) -> dict:
    """소비 성향 분석"""
    try:
        # 1. 거래 데이터 로드
        df = load_expense_transactions(year, month)
        if df.empty:
            logger.warning("거래 데이터 없음 - 기본 유형 반환")
            return _build_default_response()
        
        # 2. 점수 계산 (df만으로)
        scores = _calculate_scores(df)
        
        # 3. 유형 결정
        personality_type = _determine_type(scores)
        
        # 4. 응답 구성
        personality = get_personality(personality_type)
        result = personality.to_response(scores)
        
        logger.info(f"소비 성향 분석 완료: {personality_type}")
        return result
        
    except Exception as e:
        logger.error(f"소비 성향 분석 실패: {e}", exc_info=True)
        return _build_default_response()

def _build_default_response() -> dict:
    """기본 응답"""
    default_scores = {"planning": 0.5, "saving": 0.5}
    return get_personality("Unknown").to_response(default_scores)

# ============================================================
# 점수 계산
# ============================================================
def _calculate_scores(df: pd.DataFrame) -> dict:
    """2개 축 점수 계산"""
    return {
        "planning": _calc_planning_score(df),
        "saving": _calc_saving_score(df),
    }


def _calc_planning_score(df: pd.DataFrame) -> float:
    """
    계획성 점수 (0.0 ~ 1.0)  
        높을수록 계획적, 낮을수록 충동적
    산정 기준:
        1. 시간 규칙성 (50%)
            - 거래 시간대의 표준편차로 측정
            - 표준편차 낮음 = 특정 시간대에 집중 = 규칙적
        2. 거래처 반복성 (50%)
            - 3회 이상 방문한 거래처 비율
            - 같은 곳 자주 방문 = 습관적 = 계획적
    """
    if df.empty:
        return 0.5
    
    df = df.copy()
    
    # 1. 시간 규칙성 (표준편차 낮을수록 규칙적)
    df["hour"] = df["거래일시"].dt.hour
    hour_std = df["hour"].std()
    
    if pd.isna(hour_std) or hour_std == 0:
        time_score = 1.0  # 모두 같은 시간 → 매우 규칙적
    else:
        time_score = 1.0 - min(1.0, hour_std / 12.0)
    
    # 2. 거래처 반복성 (3회 이상 방문한 거래처 비율)
    if "거래처" in df.columns:
        merchant_counts = df["거래처"].value_counts()
        total_merchants = len(merchant_counts)
        repeat_merchants = (merchant_counts >= 3).sum()
        repeat_score = repeat_merchants / max(total_merchants, 1)
    else:
        repeat_score = 0.5
    
    # 가중 평균
    score = time_score * 0.5 + repeat_score * 0.5
    return _clamp(score)


def _calc_saving_score(df: pd.DataFrame) -> float:
    """
    절약성 점수 (0.0 ~ 1.0)
        높을수록 절약형, 낮을수록 소비형
    산정 기준:
        1. 평균 거래액 (10만원 기준)
            - 평균 거래액 낮을수록 절약형
        2. 월 거래 빈도 (100건/월 기준)
            - 월 거래 빈도 낮을수록 절약형
    """
    if df.empty:
        return 0.5
    
    # 1. 평균 거래액 (10만원 기준)
    avg_amount = df["금액"].abs().mean()
    amount_score = 1.0 - min(1.0, avg_amount / 100000)
    
    # 2. 월 거래 빈도 (100건/월 기준)
    date_range = (df["거래일시"].max() - df["거래일시"].min()).days
    if date_range > 0:
        monthly_count = len(df) / (date_range / 30)
        frequency_score = 1.0 - min(1.0, monthly_count / 100)
    else:
        frequency_score = 0.5
    
    # 가중 평균
    score = amount_score * 0.6 + frequency_score * 0.4
    return _clamp(score)


def _clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))


# ============================================================
# 유형 결정
# ============================================================
def _determine_type(scores: dict) -> str:
    """2개 축 기반 4가지 소비 성향 유형 결정"""
    is_planner = scores["planning"] >= 0.5
    is_saver = scores["saving"] >= 0.5
    
    if is_planner and is_saver:
        return "ANT"
    elif is_planner and not is_saver:
        return "FOX"
    elif not is_planner and is_saver:
        return "SQUIRREL"
    else:
        return "LION"

