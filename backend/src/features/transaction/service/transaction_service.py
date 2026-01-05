import pandas as pd
import logging

from src.features.transaction.model.transaction import TransactionQuery
from src.features.transaction.repository.transaction_repository import load_transactions, find_transaction_by_id, save_transactions
from src.features.transaction.service.transaction_filters import filter_transactions

logger = logging.getLogger(__name__)


# ============================================================
# Public Functions
# ============================================================
def fetch_transactions_data(query: TransactionQuery) -> tuple[list[dict], int]:
    """거래내역 조회"""
    logger.info(f"거래내역 조회 요청 - {query.model_dump_json()}")
    
    # 거래내역 조회
    df = load_transactions()
    # 거래내역이 없으면 빈 리스트 반환
    if df.empty:
        return [], 0
    
    # 거래내역 필터링
    df = filter_transactions(df, query)
    # 거래내역 전체 개수
    total_count = len(df)
    # 거래내역 페이지 조회
    df_page = paginate_transactions(df, query)
    # 거래내역 포맷팅
    result = _to_transaction_list(df_page)
    logger.info(f"거래내역 조회 완료 - 전체: {total_count}건, 반환: {len(result)}건")
    return result, total_count


def modify_transaction(transaction_id: int, update_data: dict) -> dict:
    """거래내역 수정""" 
    # 거래내역 조회
    df = load_transactions()
    # 거래내역이 없으면 예외 발생
    if df.empty:
        raise ValueError("거래내역 파일이 없습니다")
    
    # 거래내역 조회
    row_index, _ = find_transaction_by_id(df, transaction_id)

     # 필드 업데이트
    for key, value in update_data.items():
        if value is not None:
            df.loc[row_index, key] = value

    # 거래내역 저장
    save_transactions(df)
    logger.info(f"거래내역 수정 완료: ID {transaction_id}")

    # 거래내역 포맷팅
    row_dict = df.loc[row_index].to_dict()
    if '거래일시' in row_dict:
        row_dict['거래일시'] = pd.to_datetime(row_dict['거래일시']).strftime("%Y-%m-%d %H:%M:%S")
    return row_dict


def paginate_transactions(df: pd.DataFrame, query: TransactionQuery) -> pd.DataFrame:
    """거래내역 정렬 및 페이지네이션"""
    df_sorted = df.sort_values("거래일시", ascending=False)
    return df_sorted.iloc[query.offset:query.offset + query.limit].copy()


# ============================================================
# Private Functions
# ============================================================
def _to_transaction_list(df: pd.DataFrame) -> list[dict]:
    """DataFrame을 딕셔너리 리스트로 변환 (날짜 포맷팅 포함)"""
    df_formatted = df.copy()
    if '거래일시' in df_formatted.columns:
        df_formatted['거래일시'] = df_formatted['거래일시'].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df_formatted.to_dict('records')

