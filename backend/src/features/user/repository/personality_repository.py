import pandas as pd
import logging


from src.core.utils.dataframe_utils import (
    filter_by_date_range,
    filter_expense_only,
)
from src.core.utils.date_utils import parse_date_params
from src.features.transaction.repository.transaction_repository import load_transactions
from src.features.user.model.personality import Personality
from src.features.user.data.personality_types import PERSONALITY_DATA


logger = logging.getLogger(__name__)

# ======================= personality type repository =======================
def get_personality(code: str) -> Personality:
    """코드로 성향 정보 조회"""
    data = PERSONALITY_DATA.get(code, PERSONALITY_DATA["Unknown"])
    return data

def get_all_personalities() -> list[Personality]:
    """모든 성향 타입 조회"""
    return list(PERSONALITY_DATA.values())


# ======================= transaction repository =======================
def load_expense_transactions(
    year: int | None = None,
    month: int | None = None
) -> pd.DataFrame:
    """지출 거래 데이터 로드 및 필터링"""
    # 날짜 파라미터 파싱
    start_date, end_date = parse_date_params(year, month, None, None)
    
    # 데이터 로드
    df = load_transactions()
    
    df = filter_by_date_range(df, start_date, end_date)
    df = filter_expense_only(df)
    
    return df
