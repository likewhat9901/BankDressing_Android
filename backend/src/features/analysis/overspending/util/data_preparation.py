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


def prepare_expense_data(
    year: int | None = None,
    month: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """지출 데이터 준비"""
    # 거래내역 로드
    df = load_transactions()
    if df.empty:
        return df
    
    # 날짜 파라미터 파싱
    start_date, end_date = parse_date_params(year, month, start_date, end_date)
    
    # 날짜 필터링
    df = filter_by_date_range(df, start_date, end_date)
    if df.empty:
        return df
    
    # 지출 데이터만 필터링
    df = filter_expense_only(df)
    if df.empty:
        return df
    
    # 거래일시 데이터 타입 검증
    validate_datetime_column(df)
    
    return df