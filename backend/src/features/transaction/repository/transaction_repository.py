import pandas as pd
import logging

from src.core.config.paths import PROCESSED_DATA_DIR

logger = logging.getLogger(__name__)

TRANSACTIONS_PARQUET_PATH = PROCESSED_DATA_DIR / "transactions.parquet"

def load_transactions() -> pd.DataFrame:
    """거래내역 parquet 파일 로드"""
    if not TRANSACTIONS_PARQUET_PATH.exists():
        logger.warning(f"파일 없음: {TRANSACTIONS_PARQUET_PATH}")
        return pd.DataFrame()
    
    try:
        return pd.read_parquet(TRANSACTIONS_PARQUET_PATH)
    except Exception as e:
        logger.error(f"파일 로드 실패: {TRANSACTIONS_PARQUET_PATH}, {e}")
        raise

def save_transactions(df: pd.DataFrame) -> None:
    """거래내역 parquet 파일 저장"""
    TRANSACTIONS_PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        df.to_parquet(TRANSACTIONS_PARQUET_PATH, index=False)
        logger.info(f"거래내역 저장 완료: {TRANSACTIONS_PARQUET_PATH}")
    except Exception as e:
        logger.error(f"파일 저장 실패: {TRANSACTIONS_PARQUET_PATH}, {e}")
        raise


def find_transaction_by_id(df: pd.DataFrame, transaction_id: int) -> tuple[int, pd.Series]:
    """ID로 거래내역 찾기"""
    mask = df['id'] == transaction_id
    matching_count = mask.sum()
    
    # ID로 거래내역이 없으면 예외 발생
    if matching_count == 0:
        raise ValueError(f"거래내역을 찾을 수 없습니다: ID {transaction_id}")
    
    # ID로 거래내역이 중복되면 경고 메시지 출력
    if matching_count > 1:
        logger.warning(f"중복된 ID 발견: {transaction_id} ({matching_count}개 행)")
    
    # ID로 거래내역 인덱스 찾기
    row_index = df[mask].index[0]
    # ID로 거래내역 데이터 반환
    return row_index, df.loc[row_index]
